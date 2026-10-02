# X-Plane Web API & WebSocket Specification

X-Plane (v12.1.1+) includes a built-in HTTP and WebSocket server running locally on port **8086** by default. It provides a modern, structured JSON interface for telemetry, datarefs, commands, and complete flight initialization.

---

## 1. Server Configuration & Ports

- **Default Port**: `8086`
- **CLI Startup Arguments**:
  - `--web_server_port=<port>`: Overrides the default listening port (e.g. `--web_server_port=8088`).
  - `--no_web_server`: Completely disables the web server.
- **Base REST URL**: `http://localhost:8086/api/v3`
- **Base WebSocket URL**: `ws://localhost:8086/api/v3`

---

## 2. API Version History & Capabilities

| Version | Introduced In | Key Capabilities Added |
|---|---|---|
| **v1** | X-Plane 12.1.1 | Dataref listing, count, GET/PATCH value, WebSocket dataref subscriptions (10Hz). |
| **v2** | X-Plane 12.4.0 | Capabilities discovery, Command listing, REST command activation (`duration`), WebSocket continuous command activation. |
| **v3** | X-Plane 12.4.0 | Flight Initialization API (`POST /flight`, `PATCH /flight`) for full scenario dispatch. |

### Capability Detection
Query available endpoints and API versions dynamically:
```http
GET http://localhost:8086/api/capabilities
```
**Example Response**:
```json
{
  "api_versions": ["v1", "v2", "v3"],
  "endpoints": [
    "/api/v3/datarefs",
    "/api/v3/commands",
    "/api/v3/flight"
  ]
}
```

---

## 3. Critical Invariant: Session-Bound Numeric IDs

> [!WARNING]
> **Dynamic ID Invariant**: Dataref and Command numeric IDs (e.g. `id: 4210`) are assigned dynamically when X-Plane initializes.
> - **Stable**: IDs remain stable throughout an active X-Plane session, even when changing aircraft or loading new scenarios.
> - **Unstable**: IDs change between simulator restarts.
> **Rule**: Never hardcode numeric IDs in automation scripts or configuration files. Always query and resolve IDs dynamically by name (`filter[name]=...`).

---

## 4. REST Endpoints Reference

### 4.1. Datarefs

#### List / Search Datarefs
```http
GET /api/v3/datarefs?filter[name]=sim/flightmodel/position&limit=50&offset=0
```
**Response**:
```json
{
  "data": [
    {
      "id": 1420,
      "name": "sim/flightmodel/position/latitude",
      "type": "double",
      "writable": false,
      "value": 47.4502
    },
    {
      "id": 1421,
      "name": "sim/flightmodel/position/longitude",
      "type": "double",
      "writable": false,
      "value": -122.3088
    }
  ],
  "total": 2
}
```

#### Get Dataref by ID
```http
GET /api/v3/datarefs/{id}
```

#### Read Dataref Value
```http
GET /api/v3/datarefs/{id}/value
```
**Response**:
```json
{
  "value": 47.4502
}
```

#### Set / Modify Dataref Value
```http
PATCH /api/v3/datarefs/{id}/value
Content-Type: application/json

{
  "value": 0.75
}
```
**Response**: `200 OK` with updated value representation.

---

### 4.2. Commands

Commands trigger discrete actions in the simulator (e.g. toggling gear, deploying speedbrakes, cycling autopilot modes).

#### Search Commands
```http
GET /api/v3/commands?filter[name]=sim/flight_controls/flaps&limit=20
```
**Response**:
```json
{
  "data": [
    {
      "id": 810,
      "name": "sim/flight_controls/flaps_down",
      "description": "Flaps down a notch"
    },
    {
      "id": 811,
      "name": "sim/flight_controls/flaps_up",
      "description": "Flaps up a notch"
    }
  ],
  "total": 2
}
```

#### Activate Command (Instant or Duration)
```http
POST /api/v3/command/{id}/activate
Content-Type: application/json

{
  "duration": 0.5
}
```
- If `duration` is omitted or `0`, the command fires as a momentary impulse (`XPLMCommandOnce`).
- If `duration` is specified (in seconds), the command is held active for that length of time before releasing (`XPLMCommandBegin` then `XPLMCommandEnd`).

---

### 4.3. Flight Scenario Management

#### Initialize New Flight
```http
POST /api/v3/flight
Content-Type: application/json

{
  "aircraft": { "path": "Aircraft/Laminar Research/Cessna 172SP/Cessna_172SP.acf" },
  "location": {
    "type": "ramp_start",
    "airport": "KSEA",
    "ramp_name": "Cargo Ramp 1"
  }
}
```

#### Modify Running Flight
```http
PATCH /api/v3/flight
Content-Type: application/json

{
  "weather": {
    "preset": "clear"
  }
}
```

---

## 5. WebSocket API Reference

The WebSocket interface provides high-throughput, low-overhead event streaming.

- **URL**: `ws://localhost:8086/api/v3`
- **Sub-protocols**: standard JSON text frames.

### 5.1. Subscribing to Dataref Values

1. **Client Sends Subscribe Request**:
```json
{
  "action": "dataref_subscribe_values",
  "parameters": {
    "datarefs": [1420, 1421, 2301]
  }
}
```

2. **Server Streams Changes (10Hz max rate)**:
When values change, the server pushes:
```json
{
  "event": "dataref_update_values",
  "values": {
    "1420": 47.45031,
    "1421": -122.30875,
    "2301": 138.4
  }
}
```

3. **Unsubscribing**:
```json
{
  "action": "dataref_unsubscribe_values",
  "parameters": {
    "datarefs": [1420, 1421]
  }
}
```

---

### 5.2. Batch Setting Datarefs over WebSocket

To set multiple dataref values in a single atomic transmission:
```json
{
  "action": "dataref_set_values",
  "parameters": {
    "values": {
      "3101": 0.85,
      "3102": 1
    }
  }
}
```

---

### 5.3. Continuous Command Control over WebSocket

Hold down a command (e.g. starter switch or manual pitch trim) and release it when desired:
```json
{
  "action": "command_set_is_active",
  "parameters": {
    "command": 810,
    "is_active": true
  }
}
```
When finished, send with `"is_active": false`.

---

## 6. Error Handling & Status Codes

| HTTP Status | Meaning | Typical Cause | Remediation |
|---|---|---|---|
| `200 OK` | Success | Request succeeded. | Process payload. |
| `400 Bad Request` | Malformed JSON or invalid value | Setting string on float dataref, out of range value. | Check dataref type and ranges. |
| `404 Not Found` | Unknown ID or Endpoint | Stale session ID or invalid URL. | Re-resolve ID by dataref name. |
| `500 Server Error` | Simulator internal failure | Aircraft model loading crash, invalid ACF path. | Check `Log.txt` in X-Plane root. |
| `503 Unavailable` | Simulator loading / paused | X-Plane is loading scenery or initializing. | Retry with exponential backoff. |
