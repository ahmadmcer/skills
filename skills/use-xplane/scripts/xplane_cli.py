#!/usr/bin/env python3
"""
X-Plane Automation CLI (xplane_cli.py)
Unified tool for interacting with Laminar Research X-Plane 11 & 12
via Web API (REST/WebSocket), UDP binary protocol, offline Dataref lookup,
and Flight Initialization scenario dispatch.

Zero external dependencies - uses standard library only.
"""

import sys
import os
import re
import json
import time
import socket
import struct
import argparse
import base64
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Union
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Curated offline database of flight-critical Datarefs and Commands
CURATED_DATAREFS = [
    # Flight dynamics & position
    {"name": "sim/flightmodel/position/latitude", "type": "double", "writable": False, "units": "deg", "desc": "Aircraft latitude"},
    {"name": "sim/flightmodel/position/longitude", "type": "double", "writable": False, "units": "deg", "desc": "Aircraft longitude"},
    {"name": "sim/flightmodel/position/elevation", "type": "double", "writable": False, "units": "meters", "desc": "True altitude above sea level"},
    {"name": "sim/flightmodel/position/y_agl", "type": "float", "writable": False, "units": "meters", "desc": "Radio altitude above ground level"},
    {"name": "sim/flightmodel/position/theta", "type": "float", "writable": False, "units": "deg", "desc": "Pitch attitude (-90 to +90)"},
    {"name": "sim/flightmodel/position/phi", "type": "float", "writable": False, "units": "deg", "desc": "Roll angle (-180 to +180)"},
    {"name": "sim/flightmodel/position/psi", "type": "float", "writable": False, "units": "deg", "desc": "True heading (0 to 360)"},
    {"name": "sim/flightmodel/position/mag_psi", "type": "float", "writable": False, "units": "deg", "desc": "Magnetic heading (0 to 360)"},
    {"name": "sim/flightmodel/position/indicated_airspeed", "type": "float", "writable": False, "units": "kts", "desc": "Indicated airspeed (KIAS)"},
    {"name": "sim/flightmodel/position/true_airspeed", "type": "float", "writable": False, "units": "kts", "desc": "True airspeed (KTAS)"},
    {"name": "sim/flightmodel/position/groundspeed", "type": "float", "writable": False, "units": "m/s", "desc": "Ground speed"},
    {"name": "sim/flightmodel/position/vh_ind", "type": "float", "writable": False, "units": "m/s", "desc": "Vertical velocity (VVI)"},
    {"name": "sim/flightmodel/position/alpha", "type": "float", "writable": False, "units": "deg", "desc": "Angle of attack"},
    {"name": "sim/flightmodel/position/beta", "type": "float", "writable": False, "units": "deg", "desc": "Sideslip angle"},

    # Flight controls & surfaces
    {"name": "sim/joystick/yoke_pitch_ratio", "type": "float", "writable": True, "units": "-1.0..1.0", "desc": "Elevator yoke pitch deflection"},
    {"name": "sim/joystick/yoke_roll_ratio", "type": "float", "writable": True, "units": "-1.0..1.0", "desc": "Aileron yoke roll deflection"},
    {"name": "sim/joystick/yoke_heading_ratio", "type": "float", "writable": True, "units": "-1.0..1.0", "desc": "Rudder pedal deflection"},
    {"name": "sim/flightmodel/controls/flaprqst", "type": "float", "writable": True, "units": "0.0..1.0", "desc": "Flap handle position request"},
    {"name": "sim/flightmodel/controls/sbrkrqst", "type": "float", "writable": True, "units": "0.0..1.0", "desc": "Speedbrake handle request"},
    {"name": "sim/cockpit2/controls/gear_handle_down", "type": "int", "writable": True, "units": "0=Up,1=Down", "desc": "Landing gear handle"},
    {"name": "sim/cockpit2/controls/parking_brake_ratio", "type": "float", "writable": True, "units": "0.0..1.0", "desc": "Parking brake position"},

    # Engine & Powerplant
    {"name": "sim/flightmodel/engine/ENGN_thro", "type": "float[8]", "writable": True, "units": "0.0..1.0", "desc": "Throttle ratio per engine"},
    {"name": "sim/flightmodel/engine/ENGN_mixt", "type": "float[8]", "writable": True, "units": "0.0..1.0", "desc": "Mixture ratio per engine"},
    {"name": "sim/flightmodel/engine/ENGN_prop", "type": "float[8]", "writable": False, "units": "RPM", "desc": "Propeller shaft RPM"},
    {"name": "sim/flightmodel/engine/ENGN_N1_", "type": "float[8]", "writable": False, "units": "percent", "desc": "Turbine N1 compressor speed"},
    {"name": "sim/flightmodel/engine/ENGN_EGT", "type": "float[8]", "writable": False, "units": "deg C", "desc": "Exhaust gas temperature"},
    {"name": "sim/flightmodel/engine/ENGN_oil_press", "type": "float[8]", "writable": False, "units": "PSI", "desc": "Oil pressure per engine"},
    {"name": "sim/cockpit2/engine/actuators/throttle_ratio_all", "type": "float", "writable": True, "units": "0.0..1.0", "desc": "Master all-engine throttle"},

    # Autopilot & MCP
    {"name": "sim/cockpit/autopilot/autopilot_mode", "type": "int", "writable": True, "units": "0=Off,1=FD,2=On", "desc": "Master autopilot servos status"},
    {"name": "sim/cockpit/autopilot/heading_mag", "type": "float", "writable": True, "units": "deg", "desc": "Autopilot heading bug"},
    {"name": "sim/cockpit/autopilot/altitude", "type": "float", "writable": True, "units": "feet", "desc": "Autopilot selected altitude"},
    {"name": "sim/cockpit/autopilot/airspeed", "type": "float", "writable": True, "units": "kts", "desc": "Autopilot target airspeed"},
    {"name": "sim/cockpit/autopilot/vertical_velocity", "type": "float", "writable": True, "units": "fpm", "desc": "Autopilot vertical speed setting"},
    {"name": "sim/cockpit2/autopilot/heading_mode", "type": "int", "writable": True, "units": "0=Off,1=HDG,2=NAV", "desc": "Lateral guidance mode"},
    {"name": "sim/cockpit2/autopilot/altitude_mode", "type": "int", "writable": True, "units": "0=Pitch,1=VVI,2=Alt", "desc": "Vertical guidance mode"},
    {"name": "sim/cockpit2/autopilot/glideslope_armed", "type": "int", "writable": False, "units": "0=No,1=Armed", "desc": "ILS Glideslope armed"},
    {"name": "sim/cockpit2/autopilot/glideslope_active", "type": "int", "writable": False, "units": "0=No,1=Active", "desc": "ILS Glideslope captured"},

    # Radios & Avionics
    {"name": "sim/cockpit/radios/com1_freq_hz", "type": "int", "writable": True, "units": "100ths MHz", "desc": "COM1 active frequency"},
    {"name": "sim/cockpit/radios/com1_stdby_freq_hz", "type": "int", "writable": True, "units": "100ths MHz", "desc": "COM1 standby frequency"},
    {"name": "sim/cockpit/radios/nav1_freq_hz", "type": "int", "writable": True, "units": "100ths MHz", "desc": "NAV1 active frequency"},
    {"name": "sim/cockpit/radios/nav1_obs_degm", "type": "float", "writable": True, "units": "deg", "desc": "NAV1 OBS radial"},
    {"name": "sim/cockpit/radios/transponder_code", "type": "int", "writable": True, "units": "octal", "desc": "Transponder squawk code"},
    {"name": "sim/cockpit/radios/transponder_mode", "type": "int", "writable": True, "units": "0=Off..3=Alt", "desc": "Transponder operating mode"},

    # Systems & Environment
    {"name": "sim/cockpit2/switches/battery_on", "type": "int", "writable": True, "units": "0=Off,1=On", "desc": "Master battery switch"},
    {"name": "sim/cockpit2/switches/avionics_power_on", "type": "int", "writable": True, "units": "0=Off,1=On", "desc": "Avionics master power"},
    {"name": "sim/cockpit2/switches/navigation_lights_on", "type": "int", "writable": True, "units": "0=Off,1=On", "desc": "Navigation lights"},
    {"name": "sim/cockpit2/switches/beacon_lights_on", "type": "int", "writable": True, "units": "0=Off,1=On", "desc": "Anti-collision beacon"},
    {"name": "sim/cockpit2/switches/landing_lights_on", "type": "int", "writable": True, "units": "0=Off,1=On", "desc": "Landing lights"},
    {"name": "sim/time/zulu_time_sec", "type": "float", "writable": True, "units": "seconds", "desc": "UTC Zulu time since midnight"},
    {"name": "sim/time/sim_speed", "type": "int", "writable": True, "units": "multiplier", "desc": "Simulation speed multiplier"},
    {"name": "sim/time/paused", "type": "int", "writable": True, "units": "0=No,1=Paused", "desc": "Master simulation pause"},
    {"name": "sim/weather/barometer_sealevel_inhg", "type": "float", "writable": True, "units": "inHg", "desc": "Sea level altimeter baro setting"}
]

CURATED_COMMANDS = [
    {"name": "sim/flight_controls/flaps_down", "desc": "Extend flaps by one notch"},
    {"name": "sim/flight_controls/flaps_up", "desc": "Retract flaps by one notch"},
    {"name": "sim/flight_controls/landing_gear_toggle", "desc": "Toggle landing gear up/down"},
    {"name": "sim/flight_controls/landing_gear_down", "desc": "Extend landing gear"},
    {"name": "sim/flight_controls/landing_gear_up", "desc": "Retract landing gear"},
    {"name": "sim/flight_controls/brakes_toggle_regular", "desc": "Toggle parking / regular brakes"},
    {"name": "sim/flight_controls/brakes_toggle_max", "desc": "Toggle maximum braking effort"},
    {"name": "sim/autopilot/servos_on", "desc": "Engage autopilot servos"},
    {"name": "sim/autopilot/servos_off", "desc": "Disengage autopilot servos"},
    {"name": "sim/autopilot/servos_toggle", "desc": "Toggle autopilot master engagement"},
    {"name": "sim/autopilot/heading", "desc": "Engage Heading Select (HDG SEL)"},
    {"name": "sim/autopilot/nav", "desc": "Engage Navigation mode (NAV / VOR / LOC)"},
    {"name": "sim/autopilot/approach", "desc": "Arm ILS / RNAV Approach mode"},
    {"name": "sim/autopilot/altitude_hold", "desc": "Hold current barometric altitude"},
    {"name": "sim/autopilot/vertical_speed", "desc": "Engage Vertical Speed (V/S) mode"},
    {"name": "sim/radios/com1_standy_flip", "desc": "Swap COM1 active and standby frequencies"},
    {"name": "sim/radios/nav1_standy_flip", "desc": "Swap NAV1 active and standby frequencies"},
    {"name": "sim/transponder/transponder_ident", "desc": "Trigger transponder IDENT flash to ATC"},
    {"name": "sim/engines/throttle_up", "desc": "Step throttle levers forward"},
    {"name": "sim/engines/throttle_down", "desc": "Step throttle levers back"},
    {"name": "sim/engines/engage_starters", "desc": "Engage engine starter motors"}
]


# ============================================================================
# HTTP & REST Client Utilities
# ============================================================================

def make_http_request(url: str, method: str = "GET", payload: Optional[Any] = None, timeout: float = 5.0) -> Tuple[int, Any]:
    """Execute an HTTP request against X-Plane REST API using urllib."""
    headers = {"Accept": "application/json"}
    data_bytes = None
    if payload is not None:
        data_bytes = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.status
            content = resp.read().decode("utf-8")
            if content.strip():
                try:
                    return status, json.loads(content)
                except json.JSONDecodeError:
                    return status, content
            return status, None
    except HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = body
        return e.code, parsed
    except URLError as e:
        raise ConnectionError(f"Failed to connect to X-Plane at {url}: {e.reason}")
    except socket.timeout:
        raise TimeoutError(f"Connection timed out requesting {url}")


def resolve_dataref_id(base_url: str, name_or_id: Union[str, int]) -> int:
    """Resolve a dataref string name to its session-bound numeric ID, or return int directly."""
    if isinstance(name_or_id, int) or (isinstance(name_or_id, str) and name_or_id.isdigit()):
        return int(name_or_id)

    name = str(name_or_id).strip()
    query_url = f"{base_url}/datarefs?filter[name]={name}&limit=10"
    status, result = make_http_request(query_url)
    if status != 200 or not isinstance(result, dict) or "data" not in result:
        raise ValueError(f"Failed to search for dataref '{name}'. Response: {result}")

    for item in result["data"]:
        if item.get("name") == name:
            return int(item["id"])

    # If exact match not found, take first match if available
    if result.get("data"):
        return int(result["data"][0]["id"])

    raise LookupError(f"Dataref '{name}' not found in X-Plane session.")


def resolve_command_id(base_url: str, name_or_id: Union[str, int]) -> int:
    """Resolve a command string name to its session-bound numeric ID, or return int directly."""
    if isinstance(name_or_id, int) or (isinstance(name_or_id, str) and name_or_id.isdigit()):
        return int(name_or_id)

    name = str(name_or_id).strip()
    query_url = f"{base_url}/commands?filter[name]={name}&limit=10"
    status, result = make_http_request(query_url)
    if status != 200 or not isinstance(result, dict) or "data" not in result:
        raise ValueError(f"Failed to search for command '{name}'. Response: {result}")

    for item in result["data"]:
        if item.get("name") == name:
            return int(item["id"])

    if result.get("data"):
        return int(result["data"][0]["id"])

    raise LookupError(f"Command '{name}' not found in X-Plane session.")


# ============================================================================
# Minimal Standard-Library WebSocket Client (RFC 6455)
# ============================================================================

class SimpleWebSocketClient:
    """Minimal WebSocket client implementation using socket and standard library."""
    def __init__(self, host: str, port: int, path: str = "/api/v3", timeout: float = 5.0):
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.sock: Optional[socket.socket] = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

        key = base64.b64encode(os.urandom(16)).decode('ascii')
        headers = [
            f"GET {self.path} HTTP/1.1",
            f"Host: {self.host}:{self.port}",
            "Upgrade: websocket",
            "Connection: Upgrade",
            f"Sec-WebSocket-Key: {key}",
            "Sec-WebSocket-Version: 13",
            "\r\n"
        ]
        self.sock.sendall("\r\n".join(headers).encode("ascii"))

        # Read handshake response
        handshake = b""
        while b"\r\n\r\n" not in handshake:
            chunk = self.sock.recv(1024)
            if not chunk:
                raise ConnectionError("Server closed connection during WebSocket handshake")
            handshake += chunk

        lines = handshake.split(b"\r\n")
        status_line = lines[0].decode("latin1", errors="replace")
        if " 101 " not in status_line:
            raise ConnectionError(f"WebSocket handshake rejected: {status_line}")

    def send_json(self, data: Any):
        payload = json.dumps(data).encode("utf-8")
        length = len(payload)
        header = bytearray()
        # FIN=1, Opcode=1 (text frame)
        header.append(0x81)
        # Client frames MUST be masked (mask bit = 0x80)
        if length <= 125:
            header.append(0x80 | length)
        elif length <= 65535:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))

        mask = os.urandom(4)
        header.extend(mask)

        # Apply XOR mask
        masked_payload = bytearray(length)
        for i in range(length):
            masked_payload[i] = payload[i] ^ mask[i % 4]

        self.sock.sendall(header + masked_payload)

    def recv_json(self, timeout: Optional[float] = None) -> Optional[Any]:
        if timeout is not None:
            self.sock.settimeout(timeout)
        try:
            head = self._recv_exact(2)
            if not head:
                return None
            b1, b2 = head[0], head[1]
            opcode = b1 & 0x0F
            is_masked = bool(b2 & 0x80)
            payload_len = b2 & 0x7F

            if payload_len == 126:
                payload_len = struct.unpack("!H", self._recv_exact(2))[0]
            elif payload_len == 127:
                payload_len = struct.unpack("!Q", self._recv_exact(8))[0]

            mask_key = None
            if is_masked:
                mask_key = self._recv_exact(4)

            payload_data = self._recv_exact(payload_len)
            if is_masked and mask_key:
                unmasked = bytearray(payload_len)
                for i in range(payload_len):
                    unmasked[i] = payload_data[i] ^ mask_key[i % 4]
                payload_data = bytes(unmasked)

            # Opcode 1 = text frame
            if opcode == 1:
                return json.loads(payload_data.decode("utf-8"))
            elif opcode == 8: # Close frame
                return None
            return None
        except socket.timeout:
            return None

    def _recv_exact(self, num_bytes: int) -> bytes:
        data = bytearray()
        while len(data) < num_bytes:
            packet = self.sock.recv(num_bytes - len(data))
            if not packet:
                break
            data.extend(packet)
        return bytes(data)

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


# ============================================================================
# UDP Packet Builders & Decoders
# ============================================================================

def pack_dref_packet(dataref: str, value: float) -> bytes:
    """Pack 509-byte DREF packet. Format: '<5sf500s'"""
    dref_bytes = dataref.encode("utf-8").ljust(500, b"\x00")
    if len(dref_bytes) > 500:
        dref_bytes = dref_bytes[:500]
    return struct.pack("<5sf500s", b"DREF\x00", float(value), dref_bytes)


def pack_cmnd_packet(command: str) -> bytes:
    """Pack CMND packet. Format: 'CMND\0' + command string + '\0'"""
    return b"CMND\x00" + command.strip().encode("utf-8") + b"\x00"


def pack_rref_packet(dataref: str, frequency_hz: int, client_id: int) -> bytes:
    """Pack 413-byte RREF subscribe packet. Format: '<5sii400s'"""
    dref_bytes = dataref.encode("utf-8").ljust(400, b"\x00")
    if len(dref_bytes) > 400:
        dref_bytes = dref_bytes[:400]
    return struct.pack("<5sii400s", b"RREF\x00", int(frequency_hz), int(client_id), dref_bytes)


def pack_posi_packet(lat: float, lon: float, alt_m: float,
                     pitch: float = 0.0, roll: float = 0.0, heading: float = 0.0,
                     gear: float = 1.0, acf_index: int = 0) -> bytes:
    """Pack 48-byte POSI packet. Format: '<5sb2sdddffff'"""
    return struct.pack(
        "<5sb2sdddffff",
        b"POSI\x00",
        int(acf_index),
        b"\x00\x00",
        float(lat),
        float(lon),
        float(alt_m),
        float(pitch),
        float(roll),
        float(heading),
        float(gear)
    )


def decode_udp_packet(packet: bytes) -> Dict[str, Any]:
    """Decode incoming X-Plane UDP datagram (DATA or RREF)."""
    if len(packet) < 5:
        return {"error": "Packet too short"}

    header = packet[:5]
    if header == b"RREF\x00":
        results = {}
        offset = 5
        while offset + 8 <= len(packet):
            client_id, val = struct.unpack("<if", packet[offset:offset+8])
            results[client_id] = val
            offset += 8
        return {"type": "RREF", "values": results}

    elif header == b"DATA\x00":
        groups = {}
        offset = 5
        while offset + 36 <= len(packet):
            idx = struct.unpack("<i", packet[offset:offset+4])[0]
            floats = struct.unpack("<8f", packet[offset+4:offset+36])
            groups[idx] = list(floats)
            offset += 36
        return {"type": "DATA", "groups": groups}

    return {"type": "UNKNOWN", "raw_header": header.decode("latin1", errors="replace")}


# ============================================================================
# Scenario Validation & Templates
# ============================================================================

SCENARIO_TEMPLATES = {
    "cold-dark-ramp": {
        "$schema": "https://developer.x-plane.com/article/flight-initialization-api/",
        "title": "Cessna 172SP Cold & Dark Ramp Start",
        "aircraft": {
            "path": "Aircraft/Laminar Research/Cessna 172SP/Cessna_172SP.acf",
            "livery": "Default",
            "engine_status": "cold_and_dark"
        },
        "location": {
            "type": "ramp_start",
            "airport": "KSEA",
            "ramp_name": "Cargo Ramp 1"
        },
        "weight_and_balance": {"fuel_ratio": 0.50, "payload_weight_kg": 160.0, "cg_ratio": 0.25},
        "time": {"zulu_time_sec": 50400, "day_of_year": 180},
        "weather": {"preset": "clear", "barometer_sealevel_inhg": 29.92},
        "failures": [],
        "ai_traffic": []
    },
    "ils-final-approach": {
        "$schema": "https://developer.x-plane.com/article/flight-initialization-api/",
        "title": "Boeing 737-800 3nm ILS Final Approach",
        "aircraft": {
            "path": "Aircraft/Laminar Research/Boeing B737-800/b737800.acf",
            "livery": "Default",
            "engine_status": "running"
        },
        "location": {
            "type": "runway_start",
            "airport": "KSEA",
            "runway": "16L",
            "approach_distance_nm": 3.0,
            "approach_glideslope_deg": 3.0
        },
        "weight_and_balance": {"fuel_ratio": 0.40, "payload_weight_kg": 12500.0, "cg_ratio": 0.28},
        "time": {"zulu_time_sec": 43200, "day_of_year": 210},
        "weather": {"preset": "scattered", "barometer_sealevel_inhg": 29.92},
        "failures": [],
        "ai_traffic": []
    },
    "engine-out-emergency": {
        "$schema": "https://developer.x-plane.com/article/flight-initialization-api/",
        "title": "Boeing 737-800 Engine #1 Failure Drill in Flight",
        "aircraft": {
            "path": "Aircraft/Laminar Research/Boeing B737-800/b737800.acf",
            "livery": "Default",
            "engine_status": "running"
        },
        "location": {
            "type": "lle_air_start",
            "latitude": 47.4502,
            "longitude": -122.3088,
            "altitude_msl_ft": 5000.0,
            "heading_deg": 340.0,
            "airspeed_kts": 210.0
        },
        "weight_and_balance": {"fuel_ratio": 0.35, "payload_weight_kg": 11000.0, "cg_ratio": 0.27},
        "time": {"zulu_time_sec": 57600, "day_of_year": 150},
        "weather": {"preset": "broken", "barometer_sealevel_inhg": 29.85},
        "failures": [{"system": "sim/operation/failures/rel_engfai0", "status": "failed"}],
        "ai_traffic": []
    },
    "crosswind-landing": {
        "$schema": "https://developer.x-plane.com/article/flight-initialization-api/",
        "title": "Cessna 172SP 25-knot Crosswind Final Approach",
        "aircraft": {
            "path": "Aircraft/Laminar Research/Cessna 172SP/Cessna_172SP.acf",
            "livery": "Default",
            "engine_status": "running"
        },
        "location": {
            "type": "runway_start",
            "airport": "KSEA",
            "runway": "16L",
            "approach_distance_nm": 2.0,
            "approach_glideslope_deg": 3.0
        },
        "weight_and_balance": {"fuel_ratio": 0.50, "payload_weight_kg": 170.0, "cg_ratio": 0.26},
        "time": {"zulu_time_sec": 64800, "day_of_year": 240},
        "weather": {
            "preset": "broken",
            "barometer_sealevel_inhg": 29.75,
            "winds": [{"altitude_m": 0.0, "direction_deg": 250.0, "speed_kts": 25.0, "gust_kts": 35.0}]
        },
        "failures": [],
        "ai_traffic": []
    }
}


def validate_scenario_dict(scenario: Dict[str, Any]) -> List[str]:
    """Validate scenario schema and return list of errors (empty list if valid)."""
    errors = []
    if "aircraft" not in scenario or not isinstance(scenario["aircraft"], dict):
        errors.append("Missing required top-level object: 'aircraft'")
    else:
        acf = scenario["aircraft"]
        if "path" not in acf or not isinstance(acf["path"], str) or not acf["path"].endswith(".acf"):
            errors.append("aircraft.path must be a string ending with '.acf'")

    if "location" not in scenario or not isinstance(scenario["location"], dict):
        errors.append("Missing required top-level object: 'location'")
    else:
        loc = scenario["location"]
        valid_types = {"runway_start", "ramp_start", "lle_ground_start", "lle_air_start", "boat_start"}
        loc_type = loc.get("type")
        if loc_type not in valid_types:
            errors.append(f"location.type must be one of {valid_types}, got '{loc_type}'")
        elif loc_type == "runway_start":
            if "airport" not in loc or not isinstance(loc["airport"], str):
                errors.append("runway_start requires 'airport' (ICAO code)")
            if "runway" not in loc:
                errors.append("runway_start requires 'runway' identifier")
        elif loc_type == "ramp_start":
            if "airport" not in loc or not isinstance(loc["airport"], str):
                errors.append("ramp_start requires 'airport' (ICAO code)")
        elif loc_type in {"lle_ground_start", "lle_air_start"}:
            if "latitude" not in loc or not (-90.0 <= loc["latitude"] <= 90.0):
                errors.append("Location requires valid latitude (-90 to +90)")
            if "longitude" not in loc or not (-180.0 <= loc["longitude"] <= 180.0):
                errors.append("Location requires valid longitude (-180 to +180)")

    return errors


# ============================================================================
# CLI Command Handlers
# ============================================================================

def handle_web_status(args):
    url = f"http://{args.host}:{args.port}/api/capabilities"
    try:
        status, data = make_http_request(url, timeout=args.timeout)
        print(f"[SUCCESS] Connected to X-Plane Web API (Status {status})")
        print(json.dumps(data, indent=2))
        return 0
    except Exception as e:
        print(f"[ERROR] Could not connect to X-Plane at {url}: {e}", file=sys.stderr)
        print("Tip: Ensure X-Plane 12 is running and Web API server is active on port 8086.", file=sys.stderr)
        return 1


def handle_web_list_datarefs(args):
    base_url = f"http://{args.host}:{args.port}/api/v3"
    params = [f"limit={args.limit}", f"offset={args.offset}"]
    if args.filter:
        params.append(f"filter[name]={args.filter}")
    url = f"{base_url}/datarefs?{'&'.join(params)}"
    try:
        status, data = make_http_request(url, timeout=args.timeout)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            total = data.get("total", len(data.get("data", [])))
            print(f"Datarefs (Total: {total}, showing {len(data.get('data', []))}):")
            for item in data.get("data", []):
                print(f"  [{item.get('id')}] {item.get('name')} ({item.get('type')}) = {item.get('value')} (writable={item.get('writable')})")
        return 0
    except Exception as e:
        print(f"[ERROR] Failed to query datarefs: {e}", file=sys.stderr)
        return 1


def handle_web_get_dataref(args):
    base_url = f"http://{args.host}:{args.port}/api/v3"
    try:
        dref_id = resolve_dataref_id(base_url, args.name_or_id)
        url = f"{base_url}/datarefs/{dref_id}/value"
        status, val_data = make_http_request(url, timeout=args.timeout)
        if args.json:
            print(json.dumps({"id": dref_id, "query": args.name_or_id, "response": val_data}, indent=2))
        else:
            val = val_data.get("value") if isinstance(val_data, dict) else val_data
            print(f"{args.name_or_id} (ID {dref_id}) = {val}")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


def handle_web_set_dataref(args):
    base_url = f"http://{args.host}:{args.port}/api/v3"
    try:
        dref_id = resolve_dataref_id(base_url, args.name_or_id)
        # Parse value as int, float, bool, or json structure
        val_str = args.value
        try:
            val = json.loads(val_str)
        except Exception:
            try:
                val = float(val_str)
            except ValueError:
                val = val_str

        patch_url = f"{base_url}/datarefs/{dref_id}/value"
        status, resp = make_http_request(patch_url, method="PATCH", payload={"value": val}, timeout=args.timeout)
        if status in {200, 204}:
            print(f"[SUCCESS] Set {args.name_or_id} (ID {dref_id}) to {val}")
            return 0
        else:
            print(f"[ERROR] Failed to set dataref (Status {status}): {resp}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


def handle_web_activate_command(args):
    base_url = f"http://{args.host}:{args.port}/api/v3"
    try:
        cmd_id = resolve_command_id(base_url, args.name_or_id)
        url = f"{base_url}/command/{cmd_id}/activate"
        payload = {}
        if args.duration is not None and args.duration > 0:
            payload["duration"] = float(args.duration)

        status, resp = make_http_request(url, method="POST", payload=payload, timeout=args.timeout)
        if status in {200, 204}:
            dur_msg = f" for {args.duration}s" if args.duration else " momentarily"
            print(f"[SUCCESS] Activated command {args.name_or_id} (ID {cmd_id}){dur_msg}")
            return 0
        else:
            print(f"[ERROR] Failed to activate command (Status {status}): {resp}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


def handle_web_subscribe(args):
    base_url = f"http://{args.host}:{args.port}/api/v3"
    # Resolve dataref names to IDs
    id_map = {}
    for name in args.datarefs:
        try:
            d_id = resolve_dataref_id(base_url, name)
            id_map[d_id] = name
        except Exception as e:
            print(f"[WARNING] Could not resolve dataref '{name}': {e}", file=sys.stderr)

    if not id_map:
        print("[ERROR] No valid datarefs resolved.", file=sys.stderr)
        return 1

    print(f"Connecting WebSocket to ws://{args.host}:{args.port}/api/v3 to stream {list(id_map.values())}...")
    ws = SimpleWebSocketClient(args.host, args.port, path="/api/v3")
    try:
        ws.connect()
        # Send subscription request
        sub_req = {
            "action": "dataref_subscribe_values",
            "parameters": {"datarefs": list(id_map.keys())}
        }
        ws.send_json(sub_req)
        print("[CONNECTED] Streaming live telemetry (Press Ctrl+C to stop)...")

        count = 0
        while True:
            msg = ws.recv_json(timeout=2.0)
            if msg:
                event = msg.get("event")
                if event == "dataref_update_values":
                    vals = msg.get("values", {})
                    formatted = {id_map.get(int(k), k): v for k, v in vals.items()}
                    if args.json:
                        print(json.dumps(formatted))
                    else:
                        line = " | ".join(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}" for k, v in formatted.items())
                        print(f"[{time.strftime('%H:%M:%S')}] {line}")
                    count += 1
                    if args.count and count >= args.count:
                        break
    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")
    except Exception as e:
        print(f"[ERROR] WebSocket streaming error: {e}", file=sys.stderr)
        return 1
    finally:
        ws.close()
    return 0


# ============================================================================
# UDP Handlers
# ============================================================================

def handle_udp_send_dref(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = pack_dref_packet(args.name, args.value)
    sock.sendto(packet, (args.host, args.port))
    sock.close()
    print(f"[UDP SENT] DREF -> {args.host}:{args.port} | {args.name} = {args.value}")
    return 0


def handle_udp_send_cmnd(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = pack_cmnd_packet(args.command)
    sock.sendto(packet, (args.host, args.port))
    sock.close()
    print(f"[UDP SENT] CMND -> {args.host}:{args.port} | {args.command}")
    return 0


def handle_udp_send_posi(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = pack_posi_packet(
        lat=args.lat, lon=args.lon, alt_m=args.alt_m,
        pitch=args.pitch, roll=args.roll, heading=args.heading,
        gear=args.gear, acf_index=args.index
    )
    sock.sendto(packet, (args.host, args.port))
    sock.close()
    print(f"[UDP SENT] POSI -> {args.host}:{args.port} | Lat={args.lat}, Lon={args.lon}, Alt={args.alt_m}m, Hdg={args.heading}°")
    return 0


def handle_udp_subscribe_rref(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = pack_rref_packet(args.name, args.hz, args.client_id)
    sock.sendto(packet, (args.host, args.port))
    sock.close()
    print(f"[UDP SENT] RREF Subscribe -> {args.host}:{args.port} | {args.name} at {args.hz}Hz (ID: {args.client_id})")
    return 0


def handle_udp_listen(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(("", args.port))
    except Exception as e:
        print(f"[ERROR] Could not bind to UDP port {args.port}: {e}", file=sys.stderr)
        return 1

    sock.settimeout(args.timeout)
    print(f"[UDP LISTENING] On port {args.port} (Timeout: {args.timeout}s)...")
    count = 0
    try:
        while True:
            try:
                data, addr = sock.recvfrom(2048)
                decoded = decode_udp_packet(data)
                if args.json:
                    print(json.dumps({"from": addr[0], "packet": decoded}))
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] From {addr[0]}: {decoded}")
                count += 1
                if args.count and count >= args.count:
                    break
            except socket.timeout:
                print(f"[TIMEOUT] No UDP packets received in {args.timeout}s.")
                break
    except KeyboardInterrupt:
        print("\nStopped listening.")
    finally:
        sock.close()
    return 0


# ============================================================================
# Dataref Offline Reference Handlers
# ============================================================================

def handle_dataref_search(args):
    query = args.query.lower()
    matches = []
    for d in CURATED_DATAREFS:
        if query in d["name"].lower() or query in d["desc"].lower():
            matches.append({"kind": "dataref", **d})

    for c in CURATED_COMMANDS:
        if query in c["name"].lower() or query in c["desc"].lower():
            matches.append({"kind": "command", **c})

    if args.json:
        print(json.dumps(matches, indent=2))
        return 0

    print(f"Found {len(matches)} matching Datarefs/Commands for '{args.query}':\n")
    for m in matches:
        if m["kind"] == "dataref":
            writable_str = "R/W" if m.get("writable") else "RO"
            print(f"  [DATAREF] {m['name']}")
            print(f"            Type: {m['type']} | Access: {writable_str} | Units: {m.get('units', 'n/a')}")
            print(f"            Description: {m['desc']}\n")
        else:
            print(f"  [COMMAND] {m['name']}")
            print(f"            Description: {m['desc']}\n")
    return 0


def handle_dataref_validate(args):
    name = args.name.strip()
    pattern = r"^[a-zA-Z0-9_\-]+(/[a-zA-Z0-9_\-\.\[\]]+)+$"
    is_valid = bool(re.match(pattern, name))
    starts_with_sim = name.startswith("sim/")

    if is_valid:
        print(f"[VALID] Dataref path format conforms to X-Plane standard: '{name}'")
        if not starts_with_sim:
            print(f"  Notice: Path does not start with 'sim/'. Custom plugin or third-party aircraft dataref.")
        return 0
    else:
        print(f"[INVALID] Dataref path does not conform to standard naming: '{name}'", file=sys.stderr)
        return 1


# ============================================================================
# Scenario Handlers
# ============================================================================

def handle_scenario_validate(args):
    if not os.path.exists(args.file):
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Invalid JSON file: {e}", file=sys.stderr)
        return 1

    errors = validate_scenario_dict(data)
    if errors:
        print(f"[INVALID] Scenario validation failed with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"[VALID] Scenario '{args.file}' conforms to X-Plane Flight Initialization schema.")
    print(f"  Aircraft: {data['aircraft']['path']}")
    print(f"  Location: {data['location']['type']} ({data['location'].get('airport', 'coordinates')})")
    print(f"  Weather:  {data.get('weather', {}).get('preset', 'custom')}")
    return 0


def handle_scenario_generate(args):
    preset = args.preset.lower()
    if preset not in SCENARIO_TEMPLATES:
        valid_presets = ", ".join(SCENARIO_TEMPLATES.keys())
        print(f"[ERROR] Unknown preset '{preset}'. Choose from: {valid_presets}", file=sys.stderr)
        return 1

    content = json.dumps(SCENARIO_TEMPLATES[preset], indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"[SUCCESS] Written scenario preset '{preset}' to {args.output}")
    else:
        print(content)
    return 0


def handle_scenario_dispatch(args):
    if not os.path.exists(args.file):
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1
    with open(args.file, "r", encoding="utf-8") as f:
        scenario_data = json.load(f)

    errors = validate_scenario_dict(scenario_data)
    if errors:
        print(f"[ERROR] Scenario validation failed before dispatch:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    url = f"http://{args.host}:{args.port}/api/v3/flight"
    print(f"Dispatching flight scenario to {url}...")
    try:
        status, resp = make_http_request(url, method="POST", payload=scenario_data, timeout=args.timeout)
        if status in {200, 201, 202}:
            print(f"[SUCCESS] Flight scenario successfully dispatched! (Status {status})")
            if resp:
                print(json.dumps(resp, indent=2))
            return 0
        else:
            print(f"[ERROR] X-Plane rejected flight scenario (Status {status}): {resp}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"[ERROR] Failed to dispatch scenario: {e}", file=sys.stderr)
        return 1


# ============================================================================
# Argument Parser Architecture
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xplane_cli.py",
        description="Unified X-Plane Automation CLI: Web API (REST/WebSocket), UDP, Dataref lookup, and Flight Initialization."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommand to execute")

    # 1. Web API Subcommand
    web_parser = subparsers.add_parser("web", help="Interact via X-Plane Web API (REST & WebSocket)")
    web_sub = web_parser.add_subparsers(dest="web_action", required=True)

    # web status
    ws_status = web_sub.add_parser("status", help="Test connectivity and query capabilities")
    ws_status.add_argument("--host", default="localhost", help="X-Plane host (default: localhost)")
    ws_status.add_argument("--port", type=int, default=8086, help="Web API port (default: 8086)")
    ws_status.add_argument("--timeout", type=float, default=5.0, help="Request timeout (sec)")
    ws_status.set_defaults(func=handle_web_status)

    # web list-datarefs
    ws_list = web_sub.add_parser("list-datarefs", help="List or filter datarefs")
    ws_list.add_argument("--filter", help="Dataref name substring to filter")
    ws_list.add_argument("--limit", type=int, default=20, help="Pagination limit")
    ws_list.add_argument("--offset", type=int, default=0, help="Pagination offset")
    ws_list.add_argument("--host", default="localhost")
    ws_list.add_argument("--port", type=int, default=8086)
    ws_list.add_argument("--timeout", type=float, default=5.0)
    ws_list.add_argument("--json", action="store_true", help="Output raw JSON")
    ws_list.set_defaults(func=handle_web_list_datarefs)

    # web get-dataref
    ws_get = web_sub.add_parser("get-dataref", help="Read dataref value by name or ID")
    ws_get.add_argument("name_or_id", help="Dataref path or numeric ID")
    ws_get.add_argument("--host", default="localhost")
    ws_get.add_argument("--port", type=int, default=8086)
    ws_get.add_argument("--timeout", type=float, default=5.0)
    ws_get.add_argument("--json", action="store_true")
    ws_get.set_defaults(func=handle_web_get_dataref)

    # web set-dataref
    ws_set = web_sub.add_parser("set-dataref", help="Modify dataref value")
    ws_set.add_argument("name_or_id", help="Dataref path or numeric ID")
    ws_set.add_argument("value", help="Target value (number, boolean, or JSON array)")
    ws_set.add_argument("--host", default="localhost")
    ws_set.add_argument("--port", type=int, default=8086)
    ws_set.add_argument("--timeout", type=float, default=5.0)
    ws_set.set_defaults(func=handle_web_set_dataref)

    # web activate-command
    ws_cmd = web_sub.add_parser("activate-command", help="Trigger command via REST")
    ws_cmd.add_argument("name_or_id", help="Command path or numeric ID")
    ws_cmd.add_argument("--duration", type=float, default=None, help="Hold duration in seconds")
    ws_cmd.add_argument("--host", default="localhost")
    ws_cmd.add_argument("--port", type=int, default=8086)
    ws_cmd.add_argument("--timeout", type=float, default=5.0)
    ws_cmd.set_defaults(func=handle_web_activate_command)

    # web subscribe
    ws_sub = web_sub.add_parser("subscribe", help="Stream live datarefs via WebSocket")
    ws_sub.add_argument("datarefs", nargs="+", help="Dataref paths or IDs to subscribe")
    ws_sub.add_argument("--count", type=int, default=None, help="Stop after N message frames")
    ws_sub.add_argument("--host", default="localhost")
    ws_sub.add_argument("--port", type=int, default=8086)
    ws_sub.add_argument("--json", action="store_true")
    ws_sub.set_defaults(func=handle_web_subscribe)

    # 2. UDP Subcommand
    udp_parser = subparsers.add_parser("udp", help="Binary UDP datagram commands (DREF, CMND, POSI, RREF, DATA)")
    udp_sub = udp_parser.add_subparsers(dest="udp_action", required=True)

    # udp send-dref
    us_dref = udp_sub.add_parser("send-dref", help="Send DREF datagram to set dataref value")
    us_dref.add_argument("name", help="Dataref path string")
    us_dref.add_argument("value", type=float, help="Floating-point value")
    us_dref.add_argument("--host", default="localhost")
    us_dref.add_argument("--port", type=int, default=49000, help="Inbound UDP port (default: 49000)")
    us_dref.set_defaults(func=handle_udp_send_dref)

    # udp send-cmnd
    us_cmnd = udp_sub.add_parser("send-cmnd", help="Send CMND datagram to trigger command")
    us_cmnd.add_argument("command", help="Command string")
    us_cmnd.add_argument("--host", default="localhost")
    us_cmnd.add_argument("--port", type=int, default=49000)
    us_cmnd.set_defaults(func=handle_udp_send_cmnd)

    # udp send-posi
    us_posi = udp_sub.add_parser("send-posi", help="Send POSI datagram to position aircraft")
    us_posi.add_argument("lat", type=float, help="Latitude (deg)")
    us_posi.add_argument("lon", type=float, help="Longitude (deg)")
    us_posi.add_argument("alt_m", type=float, help="Altitude MSL (meters)")
    us_posi.add_argument("--pitch", type=float, default=0.0, help="Pitch (deg)")
    us_posi.add_argument("--roll", type=float, default=0.0, help="Roll (deg)")
    us_posi.add_argument("--heading", type=float, default=0.0, help="True heading (deg)")
    us_posi.add_argument("--gear", type=float, default=1.0, help="Gear position (0.0 to 1.0)")
    us_posi.add_argument("--index", type=int, default=0, help="Aircraft index (0=user)")
    us_posi.add_argument("--host", default="localhost")
    us_posi.add_argument("--port", type=int, default=49000)
    us_posi.set_defaults(func=handle_udp_send_posi)

    # udp subscribe-rref
    us_rref = udp_sub.add_parser("subscribe-rref", help="Send RREF subscription packet")
    us_rref.add_argument("name", help="Dataref path string")
    us_rref.add_argument("--hz", type=int, default=10, help="Update frequency in Hz (0 to unsubscribe)")
    us_rref.add_argument("--client-id", type=int, default=1, help="Arbitrary client integer ID")
    us_rref.add_argument("--host", default="localhost")
    us_rref.add_argument("--port", type=int, default=49000)
    us_rref.set_defaults(func=handle_udp_subscribe_rref)

    # udp listen
    us_listen = udp_sub.add_parser("listen", help="Listen for outgoing DATA/RREF packets")
    us_listen.add_argument("--port", type=int, default=49001, help="Outbound listening port (default: 49001)")
    us_listen.add_argument("--timeout", type=float, default=10.0, help="Socket timeout (sec)")
    us_listen.add_argument("--count", type=int, default=None, help="Stop after N packets")
    us_listen.add_argument("--json", action="store_true")
    us_listen.set_defaults(func=handle_udp_listen)

    # 3. Dataref Offline Reference Subcommand
    dref_parser = subparsers.add_parser("dataref", help="Offline Dataref & Command search and validation")
    dref_sub = dref_parser.add_subparsers(dest="dref_action", required=True)

    # dataref search
    ds_search = dref_sub.add_parser("search", help="Search curated flight-critical Datarefs/Commands")
    ds_search.add_argument("query", help="Search substring (e.g. 'throttle', 'gear', 'heading', 'altitude')")
    ds_search.add_argument("--json", action="store_true")
    ds_search.set_defaults(func=handle_dataref_search)

    # dataref validate
    ds_valid = dref_sub.add_parser("validate", help="Validate dataref naming format")
    ds_valid.add_argument("name", help="Dataref string path")
    ds_valid.set_defaults(func=handle_dataref_validate)

    # 4. Scenario Subcommand
    scen_parser = subparsers.add_parser("scenario", help="Flight Initialization API scenario generator and dispatcher")
    scen_sub = scen_parser.add_subparsers(dest="scen_action", required=True)

    # scenario validate
    sc_val = scen_sub.add_parser("validate", help="Validate scenario JSON schema")
    sc_val.add_argument("file", help="Path to scenario JSON file")
    sc_val.set_defaults(func=handle_scenario_validate)

    # scenario generate
    sc_gen = scen_sub.add_parser("generate", help="Generate scenario JSON from preset template")
    sc_gen.add_argument("preset", choices=list(SCENARIO_TEMPLATES.keys()), help="Template preset name")
    sc_gen.add_argument("--output", "-o", help="Output file path (default: stdout)")
    sc_gen.set_defaults(func=handle_scenario_generate)

    # scenario dispatch
    sc_disp = scen_sub.add_parser("dispatch", help="Dispatch scenario JSON to X-Plane (POST /flight)")
    sc_disp.add_argument("file", help="Path to scenario JSON file")
    sc_disp.add_argument("--host", default="localhost")
    sc_disp.add_argument("--port", type=int, default=8086)
    sc_disp.add_argument("--timeout", type=float, default=15.0)
    sc_disp.set_defaults(func=handle_scenario_dispatch)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        sys.exit(args.func(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
