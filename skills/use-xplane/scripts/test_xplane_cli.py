#!/usr/bin/env python3
"""
Test Suite for xplane_cli.py
Includes offline mock HTTP and UDP servers to verify all functions without a live X-Plane instance.
"""

import sys
import os
import unittest
import json
import struct
import socket
import threading
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import tested module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xplane_cli


class MockXPlaneHTTPHandler(BaseHTTPRequestHandler):
    """Mock handler simulating X-Plane 12 Web API endpoints."""

    def log_message(self, format, *args):
        # Suppress noisy HTTP server logs during tests
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/capabilities":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "api_versions": ["v1", "v2", "v3"],
                "endpoints": ["/api/v3/datarefs", "/api/v3/commands", "/api/v3/flight"]
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        if path == "/api/v3/datarefs":
            filter_name = query.get("filter[name]", [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = [
                {"id": 1420, "name": "sim/flightmodel/position/latitude", "type": "double", "value": 47.4502, "writable": False},
                {"id": 1421, "name": "sim/flightmodel/position/longitude", "type": "double", "value": -122.3088, "writable": False},
                {"id": 1850, "name": "sim/cockpit2/controls/gear_handle_down", "type": "int", "value": 1, "writable": True}
            ]
            if filter_name:
                data = [d for d in data if filter_name in d["name"]]
            resp = {"data": data, "total": len(data)}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        if path == "/api/v3/datarefs/1420/value":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"value": 47.4502}).encode("utf-8"))
            return

        if path == "/api/v3/commands":
            filter_name = query.get("filter[name]", [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = [
                {"id": 810, "name": "sim/flight_controls/flaps_down", "description": "Flaps down a notch"},
                {"id": 811, "name": "sim/flight_controls/flaps_up", "description": "Flaps up a notch"}
            ]
            if filter_name:
                data = [c for c in data if filter_name in c["name"]]
            resp = {"data": data, "total": len(data)}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_PATCH(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8")
        payload = json.loads(body)

        if parsed.path.startswith("/api/v3/datarefs/") and parsed.path.endswith("/value"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "set": payload.get("value")}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        payload = json.loads(body) if body.strip() else {}

        if parsed.path.startswith("/api/v3/command/") and parsed.path.endswith("/activate"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"activated": True, "duration": payload.get("duration", 0)}).encode("utf-8"))
            return

        if parsed.path == "/api/v3/flight":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "scenario_loaded", "aircraft": payload.get("aircraft", {}).get("path")}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


class TestXPlaneCLI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start mock HTTP server on an available localhost port
        cls.http_server = HTTPServer(("127.0.0.1", 0), MockXPlaneHTTPHandler)
        cls.mock_host, cls.mock_port = cls.http_server.server_address
        cls.http_thread = threading.Thread(target=cls.http_server.serve_forever, daemon=True)
        cls.http_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.http_server.shutdown()
        cls.http_server.server_close()

    # ------------------------------------------------------------------------
    # UDP Packing & Decoding Tests
    # ------------------------------------------------------------------------
    def test_udp_dref_packing(self):
        dataref = "sim/cockpit2/controls/gear_handle_down"
        val = 1.0
        packet = xplane_cli.pack_dref_packet(dataref, val)
        self.assertEqual(len(packet), 509)
        header, unpacked_val, dref_raw = struct.unpack("<5sf500s", packet)
        self.assertEqual(header, b"DREF\x00")
        self.assertAlmostEqual(unpacked_val, 1.0, places=4)
        self.assertTrue(dref_raw.startswith(dataref.encode("utf-8")))

    def test_udp_cmnd_packing(self):
        cmd = "sim/flight_controls/flaps_down"
        packet = xplane_cli.pack_cmnd_packet(cmd)
        self.assertEqual(packet[:5], b"CMND\x00")
        self.assertEqual(packet[5:], cmd.encode("utf-8") + b"\x00")

    def test_udp_rref_packing(self):
        dataref = "sim/flightmodel/position/latitude"
        packet = xplane_cli.pack_rref_packet(dataref, frequency_hz=10, client_id=42)
        self.assertEqual(len(packet), 413)
        header, hz, cid, dref_raw = struct.unpack("<5sii400s", packet)
        self.assertEqual(header, b"RREF\x00")
        self.assertEqual(hz, 10)
        self.assertEqual(cid, 42)
        self.assertTrue(dref_raw.startswith(dataref.encode("utf-8")))

    def test_udp_posi_packing(self):
        packet = xplane_cli.pack_posi_packet(
            lat=47.45, lon=-122.30, alt_m=100.0,
            pitch=2.5, roll=-1.0, heading=164.0, gear=1.0, acf_index=0
        )
        self.assertEqual(len(packet), 48)
        header, idx, pad, lat, lon, alt, pitch, roll, hdg, gear = struct.unpack("<5sb2sdddffff", packet)
        self.assertEqual(header, b"POSI\x00")
        self.assertEqual(idx, 0)
        self.assertAlmostEqual(lat, 47.45, places=3)
        self.assertAlmostEqual(lon, -122.30, places=3)
        self.assertAlmostEqual(alt, 100.0, places=3)
        self.assertAlmostEqual(pitch, 2.5, places=2)
        self.assertAlmostEqual(roll, -1.0, places=2)
        self.assertAlmostEqual(hdg, 164.0, places=2)
        self.assertAlmostEqual(gear, 1.0, places=2)

    def test_udp_decode_rref(self):
        # Synthetic RREF packet with 2 data points (client_id 1 = 120.5, client_id 2 = 3500.0)
        packet = b"RREF\x00" + struct.pack("<if", 1, 120.5) + struct.pack("<if", 2, 3500.0)
        decoded = xplane_cli.decode_udp_packet(packet)
        self.assertEqual(decoded["type"], "RREF")
        self.assertIn(1, decoded["values"])
        self.assertAlmostEqual(decoded["values"][1], 120.5, places=2)
        self.assertIn(2, decoded["values"])
        self.assertAlmostEqual(decoded["values"][2], 3500.0, places=1)

    def test_udp_decode_data(self):
        # Synthetic DATA packet with group 3 (indicated airspeed)
        floats = [140.0, 142.0, 145.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        packet = b"DATA\x00" + struct.pack("<i8f", 3, *floats)
        decoded = xplane_cli.decode_udp_packet(packet)
        self.assertEqual(decoded["type"], "DATA")
        self.assertIn(3, decoded["groups"])
        self.assertAlmostEqual(decoded["groups"][3][0], 140.0, places=2)

    # ------------------------------------------------------------------------
    # Scenario Schema Validation Tests
    # ------------------------------------------------------------------------
    def test_builtin_scenario_presets_validity(self):
        for name, template in xplane_cli.SCENARIO_TEMPLATES.items():
            errors = xplane_cli.validate_scenario_dict(template)
            self.assertEqual(errors, [], f"Template '{name}' failed validation: {errors}")

    def test_scenario_validation_errors(self):
        invalid_scenario = {
            "aircraft": {"path": "invalid_path.txt"},
            "location": {"type": "unknown_type"}
        }
        errors = xplane_cli.validate_scenario_dict(invalid_scenario)
        self.assertGreater(len(errors), 0)

    # ------------------------------------------------------------------------
    # Mock HTTP REST Endpoint Tests
    # ------------------------------------------------------------------------
    def test_web_status(self):
        url = f"http://{self.mock_host}:{self.mock_port}/api/capabilities"
        status, data = xplane_cli.make_http_request(url)
        self.assertEqual(status, 200)
        self.assertIn("v3", data.get("api_versions", []))

    def test_resolve_dataref_id(self):
        base_url = f"http://{self.mock_host}:{self.mock_port}/api/v3"
        dref_id = xplane_cli.resolve_dataref_id(base_url, "sim/flightmodel/position/latitude")
        self.assertEqual(dref_id, 1420)

    def test_resolve_command_id(self):
        base_url = f"http://{self.mock_host}:{self.mock_port}/api/v3"
        cmd_id = xplane_cli.resolve_command_id(base_url, "sim/flight_controls/flaps_down")
        self.assertEqual(cmd_id, 810)

    def test_web_patch_dataref(self):
        base_url = f"http://{self.mock_host}:{self.mock_port}/api/v3"
        patch_url = f"{base_url}/datarefs/1420/value"
        status, resp = xplane_cli.make_http_request(patch_url, method="PATCH", payload={"value": 48.0})
        self.assertEqual(status, 200)
        self.assertEqual(resp.get("status"), "ok")

    def test_web_post_command(self):
        base_url = f"http://{self.mock_host}:{self.mock_port}/api/v3"
        url = f"{base_url}/command/810/activate"
        status, resp = xplane_cli.make_http_request(url, method="POST", payload={"duration": 0.5})
        self.assertEqual(status, 200)
        self.assertTrue(resp.get("activated"))
        self.assertEqual(resp.get("duration"), 0.5)

    def test_scenario_dispatch_http(self):
        url = f"http://{self.mock_host}:{self.mock_port}/api/v3/flight"
        preset = xplane_cli.SCENARIO_TEMPLATES["cold-dark-ramp"]
        status, resp = xplane_cli.make_http_request(url, method="POST", payload=preset)
        self.assertEqual(status, 200)
        self.assertEqual(resp.get("status"), "scenario_loaded")

    # ------------------------------------------------------------------------
    # Dataref Offline Search & Validation Tests
    # ------------------------------------------------------------------------
    def test_dataref_offline_search(self):
        matches = []
        for d in xplane_cli.CURATED_DATAREFS:
            if "heading" in d["name"].lower() or "heading" in d["desc"].lower():
                matches.append(d)
        self.assertGreater(len(matches), 0)
        names = [m["name"] for m in matches]
        self.assertIn("sim/flightmodel/position/psi", names)
        self.assertIn("sim/cockpit/autopilot/heading_mag", names)

    def test_dataref_path_syntax_validation(self):
        self.assertEqual(xplane_cli.handle_dataref_validate(argparse.Namespace(name="sim/flightmodel/position/latitude")), 0)
        self.assertEqual(xplane_cli.handle_dataref_validate(argparse.Namespace(name="custom/plugin/my_variable")), 0)
        self.assertEqual(xplane_cli.handle_dataref_validate(argparse.Namespace(name="invalid name with spaces")), 1)


if __name__ == "__main__":
    unittest.main()
