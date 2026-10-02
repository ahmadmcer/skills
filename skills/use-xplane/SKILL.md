---
name: use-xplane
description: Operate, inspect, automate, and control Laminar Research X-Plane 11 and 12 flight simulators via modern Web API (REST & WebSocket v1/v2/v3), UDP binary protocols, flight scenario initialization, and Dataref/Command telemetry. Use when interacting with X-Plane, reading flight instruments, triggering cockpit commands, dispatching flight scenarios, or building flight sim automation scripts.
---

# `use-xplane`: Flight Simulator Automation & Telemetry

The `use-xplane` skill enables AI agents and developers to interact with, control, and automate **Laminar Research X-Plane 11 and 12** flight simulators.

The skill employs a **Hybrid Protocol Strategy**:
1. **Modern Web API (REST & WebSocket v1/v2/v3 - X-Plane 12.1.1+)**: High-level telemetry, live dataref streaming, command execution with duration, and complete flight scenario dispatch via the Flight Initialization API (`POST /flight`, `PATCH /flight`).
2. **UDP Binary Network Protocol (X-Plane 10/11/12)**: Binary datagram communication on ports `49000` (inbound) and `49001` (outbound) for low-latency, high-frequency telemetry loops (`DREF`, `RREF`, `CMND`, `POSI`, `DATA`).
3. **Zero-Dependency Python Automation Tooling (`xplane_cli.py`)**: A unified cross-platform CLI built strictly on the Python standard library.

---

## 1. Core Invariants & Architecture Rules

### Invariant 1: Dynamic Session-Bound IDs
In X-Plane's Web API, dataref and command numeric IDs (e.g. `id: 1420`) are assigned dynamically when the simulator boots.
- **Stable**: IDs remain stable throughout an active simulator session (even across aircraft reloads).
- **Unstable**: IDs reset and change when X-Plane restarts.
- **Mandate**: **Never hardcode numeric IDs** in scripts or configuration files. Always query and resolve IDs dynamically by path name (`filter[name]=...`) or use the CLI wrappers.

### Invariant 2: Protocol Selection Guide
- Use **Web API (REST / WebSocket)** on port `8086` for:
  - X-Plane 12.1.1+ environments
  - Automated scenario dispatch and aircraft loading (`POST /flight`)
  - Human-readable JSON telemetry and event subscriptions (up to 10Hz)
  - Timed command activation (`duration: 0.5` seconds)
- Use **UDP Binary Protocol** on port `49000` for:
  - X-Plane 10 or 11 compatibility
  - High-frequency autopilot control loops or physics sampling (>60Hz)
  - Instantaneous 3D aircraft repositioning via `POSI`

### Invariant 3: Safe Flight Scenario Dispatch
Before dispatching a flight scenario to `POST /api/v3/flight`, always validate that:
- The aircraft path points to an existing `.acf` file inside the X-Plane directory structure.
- The `location` block contains valid coordinates or a valid 4-character ICAO code.
- Run `python scripts/xplane_cli.py scenario validate <file.json>` prior to transmission.

---

## 2. Ports & Network Reference

| Service | Port | Protocol | Direction | Config Argument / Settings |
|---|---|---|---|---|
| **Web API & WebSocket** | `8086` | HTTP / WS | Inbound to X-Plane | `--web_server_port=<port>`, `--no_web_server` |
| **X-Plane UDP Receiver** | `49000` | UDP | Inbound to X-Plane | *Settings > Network > UDP In* |
| **X-Plane UDP Broadcast** | `49001` | UDP | Outbound from X-Plane | *Settings > Data Output > UDP Out* |

---

## 3. Automation Tooling: `xplane_cli.py`

The skill includes a production-grade, zero-dependency CLI located at:
`skills/use-xplane/scripts/xplane_cli.py`

### 3.1. Web API Subcommands

```bash
# 1. Check simulator connectivity & API capabilities
python scripts/xplane_cli.py web status --host localhost --port 8086

# 2. Query dataref by string name (automatically resolves session ID)
python scripts/xplane_cli.py web get-dataref sim/flightmodel/position/latitude

# 3. Read raw JSON output for scripting/piping
python scripts/xplane_cli.py web get-dataref sim/flightmodel/position/indicated_airspeed --json

# 4. Modify / write a dataref value
python scripts/xplane_cli.py web set-dataref sim/cockpit2/controls/gear_handle_down 1

# 5. Activate a command momentarily or with duration
python scripts/xplane_cli.py web activate-command sim/flight_controls/flaps_down
python scripts/xplane_cli.py web activate-command sim/engines/engage_starters --duration 3.0

# 6. Stream live telemetry over WebSocket (10Hz)
python scripts/xplane_cli.py web subscribe sim/flightmodel/position/latitude sim/flightmodel/position/longitude --count 20
```

### 3.2. UDP Subcommands

```bash
# 1. Send DREF datagram (509 bytes) to set floating point dataref
python scripts/xplane_cli.py udp send-dref sim/cockpit2/controls/parking_brake_ratio 1.0

# 2. Send CMND datagram to trigger discrete command
python scripts/xplane_cli.py udp send-cmnd sim/flight_controls/landing_gear_toggle

# 3. Send POSI datagram (48 bytes) to reposition aircraft instantly
python scripts/xplane_cli.py udp send-posi 47.4502 -122.3088 150.0 --heading 164.0

# 4. Subscribe to dataref telemetry via UDP RREF
python scripts/xplane_cli.py udp subscribe-rref sim/flightmodel/position/indicated_airspeed --hz 10 --client-id 1

# 5. Listen for broadcast UDP telemetry packets (DATA or RREF)
python scripts/xplane_cli.py udp listen --port 49001 --count 10
```

### 3.3. Offline Dataref Search & Path Validation

```bash
# Fast offline search across curated flight-critical Datarefs and Commands
python scripts/xplane_cli.py dataref search "flaps"
python scripts/xplane_cli.py dataref search "autopilot"
python scripts/xplane_cli.py dataref search "heading" --json

# Validate Dataref path syntax
python scripts/xplane_cli.py dataref validate sim/flightmodel/position/elevation
```

### 3.4. Flight Scenario Initialization & Dispatch

```bash
# 1. Validate scenario file schema
python scripts/xplane_cli.py scenario validate examples/scenarios/cold-dark-ramp.json

# 2. Generate a new scenario file from built-in preset
python scripts/xplane_cli.py scenario generate ils-final-approach --output my_approach.json

# 3. Dispatch flight scenario to running X-Plane simulator
python scripts/xplane_cli.py scenario dispatch examples/scenarios/ils-final-approach.json --host localhost --port 8086
```

---

## 4. Built-in Scenario Presets

Production-ready scenario templates are provided in `examples/scenarios/`:

1. **[`cold-dark-ramp.json`](file:///C:/Users/Personal/.agents/skills/use-xplane/examples/scenarios/cold-dark-ramp.json)**:
   - Aircraft: Cessna 172SP (`Aircraft/Laminar Research/Cessna 172SP/Cessna_172SP.acf`)
   - Location: Ramp start at Seattle-Tacoma (KSEA), Cargo Ramp 1
   - State: `cold_and_dark` (engines off, master switches off)
2. **[`ils-final-approach.json`](file:///C:/Users/Personal/.agents/skills/use-xplane/examples/scenarios/ils-final-approach.json)**:
   - Aircraft: Boeing 737-800 (`Aircraft/Laminar Research/Boeing B737-800/b737800.acf`)
   - Location: Runway 16L at KSEA, 3.0nm final approach on 3.0° glideslope
   - State: `running`, flaps/gear configured, airspeed stabilized
3. **[`engine-out-emergency.json`](file:///C:/Users/Personal/.agents/skills/use-xplane/examples/scenarios/engine-out-emergency.json)**:
   - Aircraft: Boeing 737-800 at 5,000ft MSL, 210 KIAS
   - Injected Failure: Engine #1 failure (`sim/operation/failures/rel_engfai0`)
4. **[`crosswind-landing.json`](file:///C:/Users/Personal/.agents/skills/use-xplane/examples/scenarios/crosswind-landing.json)**:
   - Aircraft: Cessna 172SP on 2.0nm final approach to Runway 16L
   - Weather: 25kt gusting 35kt crosswind from 250° (direct 90° crosswind component)

---

## 5. Detailed References Guide

For deep technical specifications, consult the reference documents in `references/`:
- **[Web API & WebSocket Reference](file:///C:/Users/Personal/.agents/skills/use-xplane/references/web-api-and-websocket.md)**: REST endpoints table, WebSocket frame specifications, batch sets, error codes.
- **[Flight Initialization API Reference](file:///C:/Users/Personal/.agents/skills/use-xplane/references/flight-initialization-api.md)**: Complete JSON schemas for `POST /flight` and `PATCH /flight`, start modes, weight & balance, and failure definitions.
- **[UDP Protocol Specification](file:///C:/Users/Personal/.agents/skills/use-xplane/references/udp-protocol-specification.md)**: Binary struct layouts (`<5sf500s`, `<5sii400s`, `<5sb2sdddffff`, `<i8f`), padding rules, and packet headers.
- **[Curated Datarefs & Commands](file:///C:/Users/Personal/.agents/skills/use-xplane/references/curated-datarefs-and-commands.md)**: Top flight-critical Datarefs and Commands organized by flight dynamics, controls, powerplant, autopilot, avionics, and systems.

---

## 6. Testing & Quality Verification

Run the automated test suite with built-in mock HTTP and UDP servers:
```bash
python skills/use-xplane/scripts/test_xplane_cli.py
```
This tests mock REST capabilities, dynamic ID resolution, PATCH value modification, command activation with duration, scenario dispatching, UDP struct packing and unpacking, and offline schema validation without requiring X-Plane to be running.
