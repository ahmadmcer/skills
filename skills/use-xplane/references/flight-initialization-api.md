# X-Plane Flight Initialization API Reference

Introduced in **X-Plane 12.4.0 (API v3)**, the Flight Initialization API allows automated systems to reset, configure, and spawn arbitrary flight scenarios via HTTP `POST /api/v3/flight` and update the live flight state via `PATCH /api/v3/flight`.

---

## 1. Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v3/flight` | `POST` | Dispatches a completely new flight scenario (loads aircraft, scenery, weather, location). |
| `/api/v3/flight` | `PATCH` | Updates the live flight state without a full reload (weather changes, time jump, failure injection). |

Headers:
```http
Content-Type: application/json
```

---

## 2. Payload Structure (JSON Schema)

```json
{
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
  "weight_and_balance": {
    "fuel_ratio": 0.45,
    "payload_weight_kg": 14200.0,
    "cg_ratio": 0.28
  },
  "time": {
    "zulu_time_sec": 50400,
    "day_of_year": 200
  },
  "weather": {
    "preset": "clear",
    "barometer_sealevel_inhg": 29.92
  },
  "failures": [
    {
      "system": "sim/operation/failures/rel_engfir0",
      "status": "failed"
    }
  ],
  "ai_traffic": []
}
```

---

## 3. Parameter Specifications

### 3.1. `aircraft`
- **`path`** *(string, required)*: Relative path from X-Plane root directory to the aircraft `.acf` file. Forward slashes `/` are required across all operating systems.
  - Cessna 172SP: `Aircraft/Laminar Research/Cessna 172SP/Cessna_172SP.acf`
  - Boeing 737-800: `Aircraft/Laminar Research/Boeing B737-800/b737800.acf`
  - Cirrus Vision SF50: `Aircraft/Laminar Research/Cirrus Vision SF50/Cirrus SF50.acf`
  - Airbus A330-300: `Aircraft/Laminar Research/Airbus A330-300/A330-300.acf`
- **`livery`** *(string, optional)*: Folder name of the livery under the aircraft's `liveries/` directory. If omitted or `"Default"`, default livery is used.
- **`engine_status`** *(string, optional)*:
  - `"running"`: Aircraft initializes on the runway/air with engines running, avionics configured, systems pressurized.
  - `"cold_and_dark"`: Aircraft initializes powered down with master switches off, mixtures cut, engines off. Recommended for ramp starts.

---

### 3.2. `location`
The `location` object supports 5 distinct initialization modes determined by `"type"`:

#### Mode 1: Runway Start (`runway_start`)
Positions the aircraft on the runway threshold or on final approach.
```json
{
  "type": "runway_start",
  "airport": "KSEA",
  "runway": "16L",
  "approach_distance_nm": 0.0,
  "approach_glideslope_deg": 3.0
}
```
- `airport`: 4-character ICAO code.
- `runway`: Runway identifier (e.g. `"16L"`, `"34R"`, `"09"`).
- `approach_distance_nm`:
  - `0.0`: Placed on runway centerline ready for takeoff roll.
  - `> 0.0`: In-flight final approach (e.g. `3.0` for a 3nm final approach). In this mode, airspeed and trim are automatically stabilized by the simulator.
- `approach_glideslope_deg`: Descent path angle in degrees (default `3.0`).

#### Mode 2: Ramp / Gate Start (`ramp_start`)
Positions the aircraft at a parking gate, tie-down, or hangar.
```json
{
  "type": "ramp_start",
  "airport": "KPDX",
  "ramp_name": "Gate C12"
}
```
- `ramp_name`: Exact ramp name matching airport apt.dat definition. If omitted, X-Plane selects the best available parking spot for the aircraft size.

#### Mode 3: Exact Ground Coordinate (`lle_ground_start`)
Positions the aircraft on ground at exact geographic coordinates.
```json
{
  "type": "lle_ground_start",
  "latitude": 47.4502,
  "longitude": -122.3088,
  "heading_deg": 164.0
}
```

#### Mode 4: Exact Air Coordinate (`lle_air_start`)
Spawns the aircraft in flight with precise vectors.
```json
{
  "type": "lle_air_start",
  "latitude": 47.5000,
  "longitude": -122.3000,
  "altitude_msl_ft": 5000.0,
  "heading_deg": 180.0,
  "airspeed_kts": 160.0
}
```

#### Mode 5: Carrier / Seaplane Boat Start (`boat_start`)
Positions the aircraft on an aircraft carrier or water vessel.
```json
{
  "type": "boat_start",
  "boat_name": "USS Nimitz",
  "deck_position": "catapult_1"
}
```

---

### 3.3. `weight_and_balance`
- **`fuel_ratio`** *(float, 0.0 to 1.0)*: Fuel tank filling percentage across all tanks.
- **`fuel_weight_kg`** / **`fuel_weight_lbs`** *(float, optional)*: Explicit fuel mass.
- **`payload_weight_kg`** / **`payload_weight_lbs`** *(float, optional)*: Passengers, cargo, baggage total.
- **`cg_ratio`** *(float, 0.0 to 1.0)*: Longitudinal center of gravity placement.

---

### 3.4. `time`
- **`zulu_time_sec`** *(integer, 0 to 86399)*: Universal Time Coordinated (UTC) in seconds from midnight.
  - `0`: 00:00:00Z (Midnight)
  - `21600`: 06:00:00Z (Dawn)
  - `43200`: 12:00:00Z (Noon)
  - `64800`: 18:00:00Z (Dusk)
- **`day_of_year`** *(integer, 1 to 365)*: Calendar day (e.g. 1 = Jan 1, 180 = Jun 29). Determines solar elevation and seasonal lighting.

---

### 3.5. `weather`
Can specify either a high-level preset or granular atmospheric parameters:

#### Presets
Available strings for `"preset"`:
- `"clear"`: CAVOK, unlimited visibility, light variable winds.
- `"scattered"`: Few cumulus clouds, high visibility.
- `"broken"`: 5/8 to 7/8 cloud ceiling, moderate turbulence.
- `"overcast"`: Solid stratus overcast deck.
- `"cirrus"`: High-altitude thin cirrus layers.
- `"stormy"`: Severe convective thunderstorms, windshear, heavy rain.
- `"low_visibility"`: CAT III ILS conditions, fog, RVR < 300m.

#### Granular Weather Settings
```json
{
  "barometer_sealevel_inhg": 29.85,
  "visibility_m": 8000.0,
  "precipitation_ratio": 0.4,
  "thermal_rate_m_s": 1.5,
  "clouds": [
    {
      "coverage": "bkn",
      "base_m": 900.0,
      "top_m": 2200.0
    }
  ],
  "winds": [
    {
      "altitude_m": 0.0,
      "direction_deg": 240.0,
      "speed_kts": 18.0,
      "gust_kts": 28.0
    },
    {
      "altitude_m": 3000.0,
      "direction_deg": 270.0,
      "speed_kts": 45.0,
      "gust_kts": 55.0
    }
  ]
}
```

---

### 3.6. `failures`
Inject system malfunctions immediately upon flight dispatch:
```json
"failures": [
  { "system": "sim/operation/failures/rel_engfir0", "status": "failed" },
  { "system": "sim/operation/failures/rel_vacuum", "status": "failed" },
  { "system": "sim/operation/failures/rel_pitot_0", "status": "failed" }
]
```
`status` values:
- `"operational"`: System working normally.
- `"failed"`: Instant catastrophic failure.
- `"intermittent"`: Intermittent dropout.

---

## 4. Dispatching Scenarios via CLI

Using the `xplane_cli.py` tool:

```bash
# Validate scenario file syntax
python scripts/xplane_cli.py scenario validate examples/scenarios/ils-final-approach.json

# Dispatch scenario to running X-Plane simulator
python scripts/xplane_cli.py scenario dispatch examples/scenarios/ils-final-approach.json --host localhost --port 8086
```
