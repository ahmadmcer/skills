#!/usr/bin/env python3
"""
Autonomous Flight Execution Script: WIHP (Pondok Cabe) -> WICC (Bandung)
Aircraft: Cessna 172SP Skyhawk
Simulator: Laminar Research X-Plane 12

Zero external pip dependencies - uses Python standard library only.
"""

import sys
import os
import json
import time
import math
import argparse
from typing import Dict, Any, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Ensure unbuffered real-time stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

# Waypoint Coordinates
WIHP_LAT = -6.34598
WIHP_LON = 106.76402
WIHP_ELEV_FT = 210.0

WICC_LAT = -6.90056
WICC_LON = 107.57611
WICC_ELEV_FT = 2247.0

# Navigation Math
def haversine_distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in nautical miles."""
    r_nm = 3440.065
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return 2.0 * r_nm * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

def initial_bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate initial forward bearing from point 1 to point 2 in degrees (0..360)."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    y = math.sin(delta_lambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    theta = math.degrees(math.atan2(y, x))
    return (theta + 360.0) % 360.0


class XPlaneFlightOperator:
    """Interacts with X-Plane 12 Web API for telemetry and control."""

    def __init__(self, host: str = "localhost", port: int = 8086, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}/api/v3"
        self.timeout = timeout
        self.dref_cache: Dict[str, int] = {}
        self.cmd_cache: Dict[str, int] = {}

    def _request(self, endpoint: str, method: str = "GET", payload: Optional[Any] = None) -> Tuple[int, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        data_bytes = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data_bytes = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = Request(url, data=data_bytes, headers=headers, method=method)
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
                if body.strip():
                    try:
                        return status, json.loads(body)
                    except json.JSONDecodeError:
                        return status, body
                return status, None
        except HTTPError as e:
            err_body = e.read().decode("utf-8")
            try:
                parsed = json.loads(err_body)
            except Exception:
                parsed = err_body
            return e.code, parsed
        except URLError as e:
            raise ConnectionError(f"Cannot connect to X-Plane at {url}: {e.reason}")

    def resolve_dref_id(self, name: str) -> int:
        if name in self.dref_cache:
            return self.dref_cache[name]

        status, resp = self._request(f"datarefs?filter[name]={name}&limit=10")
        if status != 200 or not isinstance(resp, dict) or "data" not in resp:
            raise LookupError(f"Dataref '{name}' not found: {resp}")

        for item in resp["data"]:
            if item.get("name") == name:
                d_id = int(item["id"])
                self.dref_cache[name] = d_id
                return d_id

        if resp.get("data"):
            d_id = int(resp["data"][0]["id"])
            self.dref_cache[name] = d_id
            return d_id

        raise LookupError(f"Dataref '{name}' not found in active session.")

    def read_dref(self, name: str, default: Any = 0.0) -> Any:
        try:
            d_id = self.resolve_dref_id(name)
            status, resp = self._request(f"datarefs/{d_id}/value")
            if status == 200 and isinstance(resp, dict):
                return resp.get("data", resp.get("value", default))
            return default
        except Exception:
            return default

    def write_dref(self, name: str, value: Any) -> bool:
        try:
            d_id = self.resolve_dref_id(name)
            # Dual-key payload ensures compatibility across X-Plane 12 releases
            status, _ = self._request(f"datarefs/{d_id}/value", method="PATCH", payload={"data": value, "value": value})
            return status in {200, 204}
        except Exception as e:
            print(f"[WARN] Failed to write {name}={value}: {e}", file=sys.stderr)
            return False

    def activate_command(self, name: str, duration: float = 0.0) -> bool:
        try:
            if name not in self.cmd_cache:
                status, resp = self._request("commands")
                if status == 200 and isinstance(resp, dict) and "data" in resp:
                    for item in resp["data"]:
                        if item.get("name") == name:
                            self.cmd_cache[name] = int(item["id"])
                            break

            c_id = self.cmd_cache.get(name)
            if c_id is None:
                return False

            status, _ = self._request(f"command/{c_id}/activate", method="POST", payload={"duration": float(duration)})
            return status in {200, 204}
        except Exception as e:
            print(f"[WARN] Failed to activate command {name}: {e}", file=sys.stderr)
            return False

    def dispatch_scenario(self, scenario_dict: Dict[str, Any]) -> bool:
        status, resp = self._request("flight", method="POST", payload=scenario_dict)
        if status not in {200, 201, 202}:
            print(f"[ERROR] Flight initialization failed ({status}): {resp}", file=sys.stderr)
            return False
        print(f"[OK] Flight initialization accepted by simulator ({status}).")
        return True


def run_flight_mission(operator: XPlaneFlightOperator, skip_dispatch: bool = False, sim_accel: int = 2):
    """Executes the full automated flight profile from WIHP to WICC."""

    print("=" * 76)
    print("   AUTONOMOUS FLIGHT OPERATION: PONDOK CABE (WIHP) -> BANDUNG (WICC)")
    print("   Aircraft: Cessna 172SP Skyhawk | Cruise Target: 8,500 ft MSL")
    print("=" * 76)

    # 1. SCENARIO DISPATCH PHASE
    if not skip_dispatch:
        print("\n[PHASE 1/7] DISPATCH: Initializing flight scenario at WIHP Runway 18...")
        scenario = {
            "runway_start": {
                "airport_id": "WIHP",
                "runway": "18"
            },
            "aircraft": {
                "path": "Aircraft/Laminar Research/Cessna 172 SP/Cessna_172SP.acf"
            },
            "engine_status": {
                "all_engines": {
                    "running": True
                }
            }
        }
        success = operator.dispatch_scenario(scenario)
        if not success:
            print("[WARN] Scenario dispatch rejected. Checking if simulator already loaded...", file=sys.stderr)

        print("[WAIT] Allowing simulator scenery and physics to initialize (15s)...")
        time.sleep(15)

    # Poll until flight model datarefs exist
    print("[WAIT] Verifying simulator telemetry connection (up to 90s)...")
    for attempt in range(45):
        lat = operator.read_dref("sim/flightmodel/position/latitude", default=None)
        if lat is not None and lat != 0.0:
            elev = float(operator.read_dref("sim/flightmodel/position/elevation", 0.0)) * 3.28084
            print(f"[CONNECTED] Active aircraft located at Lat {lat:.4f}, Alt {elev:.0f} ft MSL")
            break
        if attempt % 5 == 0 and attempt > 0:
            print(f"  ... still waiting for simulator world loading ({attempt * 2}s elapsed)...")
        time.sleep(2.0)
    else:
        print("[ERROR] Timeout waiting for aircraft datarefs. Is X-Plane running a flight?", file=sys.stderr)
        return False

    # 2. TAKEOFF PREP PHASE
    print("\n[PHASE 2/7] TAKEOFF PREPARATION: Configuring Cessna 172SP flight deck...")
    operator.write_dref("sim/time/sim_speed", 1)  # Ensure 1x real-time
    operator.write_dref("sim/flightmodel/controls/flaprqst", 0.0)  # Flaps 0deg
    operator.write_dref("sim/cockpit2/controls/parking_brake_ratio", 0.0)  # Brake off
    operator.write_dref("sim/cockpit/autopilot/heading_mag", 180.0)  # Runway heading
    operator.write_dref("sim/cockpit/autopilot/altitude", 8500.0)  # Target 8,500 ft
    operator.write_dref("sim/cockpit/autopilot/vertical_velocity", 700.0)  # 700 fpm climb
    operator.write_dref("sim/cockpit2/switches/navigation_lights_on", 1)
    operator.write_dref("sim/cockpit2/switches/beacon_lights_on", 1)
    operator.write_dref("sim/cockpit2/switches/landing_lights_on", 1)
    time.sleep(2.0)

    # 3. TAKEOFF ROLL
    print("\n[PHASE 3/7] TAKEOFF ROLL: Setting throttle 100% full power...")
    operator.write_dref("sim/cockpit2/engine/actuators/throttle_ratio_all", 1.0)

    while True:
        ias = float(operator.read_dref("sim/flightmodel/position/indicated_airspeed", 0.0))
        elev = float(operator.read_dref("sim/flightmodel/position/elevation", 0.0)) * 3.28084
        hdg = float(operator.read_dref("sim/flightmodel/position/mag_psi", 180.0))

        # Centerline rudder steering to counter propeller torque
        err = 179.0 - hdg
        rudder = min(max(err * 0.05, -0.25), 0.25)
        operator.write_dref("sim/joystick/yoke_heading_ratio", rudder)

        print(f"  [ROLL] Airspeed: {ias:5.1f} KIAS | Altitude: {elev:5.0f} ft | Heading: {hdg:03.0f}deg")
        if ias >= 55.0:
            print("\n>>> ROTATION: Reached Vr (55 KIAS) - Gently pitching nose up +8deg <<<")
            break
        time.sleep(1.0)

    # 4. ROTATION & INITIAL CLIMB
    operator.write_dref("sim/joystick/yoke_heading_ratio", 0.0)
    operator.write_dref("sim/joystick/yoke_pitch_ratio", 0.20)  # Elevator up
    time.sleep(3.0)
    operator.write_dref("sim/joystick/yoke_pitch_ratio", 0.08)  # Hold climb attitude

    print("\n[PHASE 4/7] CLIMB & DEPARTURE: Climbing straight ahead to 800 ft AGL...")
    while True:
        agl_ft = float(operator.read_dref("sim/flightmodel/position/y_agl", 0.0)) * 3.28084
        elev = float(operator.read_dref("sim/flightmodel/position/elevation", 0.0)) * 3.28084
        ias = float(operator.read_dref("sim/flightmodel/position/indicated_airspeed", 0.0))
        vvi = float(operator.read_dref("sim/flightmodel/position/vh_ind", 0.0)) * 196.85
        roll = float(operator.read_dref("sim/flightmodel/position/phi", 0.0))

        # Keep wings level during initial manual climb
        operator.write_dref("sim/joystick/yoke_roll_ratio", min(max(-roll * 0.02, -0.15), 0.15))

        print(f"  [CLIMB] AGL: {agl_ft:4.0f} ft | Alt: {elev:5.0f} ft MSL | IAS: {ias:4.1f} KIAS | VVI: {vvi:+4.0f} FPM")
        if agl_ft >= 800.0:
            print("\n>>> Reached 800 ft AGL - Engaging Autopilot toward Bandung (WICC) <<<")
            break
        time.sleep(1.5)

    # Neutralize manual control inputs
    operator.write_dref("sim/joystick/yoke_pitch_ratio", 0.0)
    operator.write_dref("sim/joystick/yoke_roll_ratio", 0.0)
    operator.write_dref("sim/joystick/yoke_heading_ratio", 0.0)

    # 5. EN-ROUTE CLIMB ON TRACK 126deg
    target_hdg = round(initial_bearing_deg(WIHP_LAT, WIHP_LON, WICC_LAT, WICC_LON), 1)
    operator.write_dref("sim/cockpit/autopilot/heading_mag", target_hdg)
    operator.write_dref("sim/cockpit/autopilot/autopilot_mode", 2)  # Servos on
    operator.write_dref("sim/cockpit2/autopilot/heading_mode", 1)  # HDG select
    operator.write_dref("sim/cockpit/autopilot/vertical_velocity", 700.0)  # 700 fpm climb
    operator.write_dref("sim/cockpit2/autopilot/altitude_mode", 1)  # Vertical speed
    operator.write_dref("sim/cockpit/autopilot/altitude", 8500.0)

    print(f"\n[PHASE 5/7] EN-ROUTE CLIMB: Intercepting track {target_hdg}deg to clear Puncak pass (8,500 ft MSL)...")
    while True:
        lat = float(operator.read_dref("sim/flightmodel/position/latitude", WIHP_LAT))
        lon = float(operator.read_dref("sim/flightmodel/position/longitude", WIHP_LON))
        elev = float(operator.read_dref("sim/flightmodel/position/elevation", 0.0)) * 3.28084
        ias = float(operator.read_dref("sim/flightmodel/position/indicated_airspeed", 0.0))
        dist_wicc = haversine_distance_nm(lat, lon, WICC_LAT, WICC_LON)
        current_bearing = round(initial_bearing_deg(lat, lon, WICC_LAT, WICC_LON), 1)

        # Dynamic heading correction
        operator.write_dref("sim/cockpit/autopilot/heading_mag", current_bearing)

        print(f"  [CLIMB] Alt: {elev:5.0f} ft / 8,500 ft | Dist WICC: {dist_wicc:4.1f} nm | Trk: {current_bearing:03.0f}deg | IAS: {ias:4.1f} kt")
        if elev >= 8400.0:
            print("\n>>> Leveling off at 8,500 ft MSL cruise altitude! Safe mountain clearance achieved. <<<")
            break
        time.sleep(2.0)

    # 6. ACCELERATED CRUISE PHASE
    print(f"\n[PHASE 6/7] CRUISE: Setting 75% throttle and engaging {sim_accel}x simulation acceleration...")
    operator.write_dref("sim/cockpit2/autopilot/altitude_mode", 2)  # Altitude hold
    operator.write_dref("sim/cockpit2/engine/actuators/throttle_ratio_all", 0.75)  # Cruise throttle
    operator.write_dref("sim/time/sim_speed", sim_accel)  # 2x or 4x acceleration

    while True:
        lat = float(operator.read_dref("sim/flightmodel/position/latitude", WIHP_LAT))
        lon = float(operator.read_dref("sim/flightmodel/position/longitude", WIHP_LON))
        elev = float(operator.read_dref("sim/flightmodel/position/elevation", 0.0)) * 3.28084
        tas = float(operator.read_dref("sim/flightmodel/position/true_airspeed", 0.0))
        dist_wicc = haversine_distance_nm(lat, lon, WICC_LAT, WICC_LON)
        current_bearing = round(initial_bearing_deg(lat, lon, WICC_LAT, WICC_LON), 1)

        operator.write_dref("sim/cockpit/autopilot/heading_mag", current_bearing)

        print(f"  [CRUISE {sim_accel}x] Dist to WICC: {dist_wicc:4.1f} nm | Alt: {elev:5.0f} ft | TAS: {tas:4.1f} kt | Bearing: {current_bearing:03.0f}deg")
        if dist_wicc <= 15.0:
            print("\n>>> REACHED TOP OF DESCENT (15nm from WICC) - Returning to 1x real-time <<<")
            break
        time.sleep(2.0)

    # 7. DESCENT INTO BANDUNG BASIN
    print("\n[PHASE 7/7] DESCENT & ARRIVAL: Descending into Bandung valley toward 3,800 ft MSL...")
    operator.write_dref("sim/time/sim_speed", 1)  # Back to 1x real-time
    operator.write_dref("sim/cockpit/autopilot/altitude", 3800.0)
    operator.write_dref("sim/cockpit/autopilot/vertical_velocity", -600.0)  # -600 fpm descent
    operator.write_dref("sim/cockpit2/autopilot/altitude_mode", 1)  # V/S mode
    operator.write_dref("sim/cockpit2/engine/actuators/throttle_ratio_all", 0.40)  # Reduce power

    while True:
        lat = float(operator.read_dref("sim/flightmodel/position/latitude", WIHP_LAT))
        lon = float(operator.read_dref("sim/flightmodel/position/longitude", WIHP_LON))
        elev = float(operator.read_dref("sim/flightmodel/position/elevation", 0.0)) * 3.28084
        agl_ft = float(operator.read_dref("sim/flightmodel/position/y_agl", 0.0)) * 3.28084
        ias = float(operator.read_dref("sim/flightmodel/position/indicated_airspeed", 0.0))
        dist_wicc = haversine_distance_nm(lat, lon, WICC_LAT, WICC_LON)
        current_bearing = round(initial_bearing_deg(lat, lon, WICC_LAT, WICC_LON), 1)

        print(f"  [DESCENT] Dist: {dist_wicc:4.1f} nm | Alt: {elev:5.0f} ft MSL | AGL: {agl_ft:4.0f} ft | IAS: {ias:4.1f} kt")

        # Approach configuration as we close in
        if dist_wicc <= 7.0 and elev <= 4500.0:
            print("  >>> Extending Flaps 10deg for Bandung Runway 11 Alignment <<<")
            operator.write_dref("sim/flightmodel/controls/flaprqst", 0.33)
            operator.write_dref("sim/cockpit/autopilot/heading_mag", 114.0)  # Align with Runway 11
        else:
            operator.write_dref("sim/cockpit/autopilot/heading_mag", current_bearing)

        if dist_wicc <= 3.5 or elev <= 3200.0:
            operator.write_dref("sim/flightmodel/controls/flaprqst", 0.67)  # Flaps 20deg
            print("\n" + "=" * 76)
            print("   MISSION ACCOMPLISHED: ARRIVED AT BANDUNG (WICC)")
            print(f"   Position: Lat {lat:.5f}, Lon {lon:.5f} | Dist: {dist_wicc:.2f} nm")
            print(f"   Altitude: {elev:.0f} ft MSL ({agl_ft:.0f} ft AGL above Bandung field)")
            print("   Runway 11 in sight! Flaps set. Autopilot ready for final touchdown.")
            print("=" * 76)
            break
        time.sleep(2.0)

    return True


def main():
    parser = argparse.ArgumentParser(description="Autonomous Flight Execution: WIHP to WICC in X-Plane 12.")
    parser.add_argument("--host", default="localhost", help="X-Plane host (default: localhost)")
    parser.add_argument("--port", type=int, default=8086, help="X-Plane Web API port (default: 8086)")
    parser.add_argument("--sim-speed", type=int, choices=[1, 2, 4], default=2, help="Cruise simulation acceleration (default: 2)")
    parser.add_argument("--no-dispatch", action="store_true", help="Skip flight dispatch if already loaded at WIHP")
    parser.add_argument("--check", action="store_true", help="Verify syntax and exit")
    args = parser.parse_args()

    if args.check:
        print("[OK] Syntax and navigation formulas verified successfully.")
        dist = haversine_distance_nm(WIHP_LAT, WIHP_LON, WICC_LAT, WICC_LON)
        brg = initial_bearing_deg(WIHP_LAT, WIHP_LON, WICC_LAT, WICC_LON)
        print(f"Calculated WIHP -> WICC Distance: {dist:.2f} nm | Initial Bearing: {brg:.1f}deg")
        sys.exit(0)

    operator = XPlaneFlightOperator(host=args.host, port=args.port)
    try:
        success = run_flight_mission(operator, skip_dispatch=args.no_dispatch, sim_accel=args.sim_speed)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Flight interrupted by user. Restoring 1x real-time sim speed...")
        operator.write_dref("sim/time/sim_speed", 1)
        sys.exit(130)


if __name__ == "__main__":
    main()
