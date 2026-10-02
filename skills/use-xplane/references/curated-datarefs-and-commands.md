# Curated X-Plane Datarefs and Commands Reference

This document catalogs the most essential, flight-critical Datarefs and Commands in X-Plane 11 and 12, organized by avionics and systems domains.

---

## 1. Flight Dynamics & Navigation Telemetry

| Dataref Path | Type | Writable | Units / Range | Description |
|---|---|---|---|---|
| `sim/flightmodel/position/latitude` | `double` | No | Degrees (-90 to +90) | Aircraft geographic latitude. |
| `sim/flightmodel/position/longitude` | `double` | No | Degrees (-180 to +180) | Aircraft geographic longitude. |
| `sim/flightmodel/position/elevation` | `double` | No | Meters MSL | True altitude above mean sea level. |
| `sim/flightmodel/position/y_agl` | `float` | No | Meters AGL | Radio height above terrain/runway. |
| `sim/flightmodel/position/theta` | `float` | No | Degrees (-90 to +90) | Pitch attitude (positive nose-up). |
| `sim/flightmodel/position/phi` | `float` | No | Degrees (-180 to +180) | Roll angle (positive right-wing down). |
| `sim/flightmodel/position/psi` | `float` | No | Degrees (0 to 360) | True heading. |
| `sim/flightmodel/position/mag_psi` | `float` | No | Degrees (0 to 360) | Magnetic heading. |
| `sim/flightmodel/position/indicated_airspeed` | `float` | No | Knots (KIAS) | Indicated airspeed from pitot-static system. |
| `sim/flightmodel/position/true_airspeed` | `float` | No | Knots (KTAS) | True airspeed. |
| `sim/flightmodel/position/groundspeed` | `float` | No | Meters/second | Ground speed vector. |
| `sim/flightmodel/position/vh_ind` | `float` | No | Meters/second | Vertical velocity (VVI) indicated. |
| `sim/flightmodel/position/alpha` | `float` | No | Degrees | Angle of attack (AoA). |
| `sim/flightmodel/position/beta` | `float` | No | Degrees | Sideslip angle. |

---

## 2. Flight Controls & Trim

| Dataref Path | Type | Writable | Units / Range | Description |
|---|---|---|---|---|
| `sim/joystick/yoke_pitch_ratio` | `float` | Yes | `-1.0` to `+1.0` | Elevator yoke deflection. |
| `sim/joystick/yoke_roll_ratio` | `float` | Yes | `-1.0` to `+1.0` | Aileron yoke deflection. |
| `sim/joystick/yoke_heading_ratio` | `float` | Yes | `-1.0` to `+1.0` | Rudder pedal deflection. |
| `sim/flightmodel/controls/flaprqst` | `float` | Yes | `0.0` to `1.0` | Flap handle deployment request ratio. |
| `sim/flightmodel/controls/sbrkrqst` | `float` | Yes | `0.0` to `1.0` | Speedbrake handle request ratio. |
| `sim/cockpit2/controls/gear_handle_down` | `int` | Yes | `0` = Up, `1` = Down | Landing gear handle position. |
| `sim/cockpit2/controls/parking_brake_ratio` | `float` | Yes | `0.0` to `1.0` | Parking brake engagement ratio. |

### Control Commands
- `sim/flight_controls/flaps_down`: Extend flaps by one detent/notch.
- `sim/flight_controls/flaps_up`: Retract flaps by one detent/notch.
- `sim/flight_controls/landing_gear_toggle`: Toggle landing gear up/down.
- `sim/flight_controls/landing_gear_down`: Force landing gear down.
- `sim/flight_controls/landing_gear_up`: Force landing gear up.
- `sim/flight_controls/brakes_toggle_regular`: Toggle parking/toe brake application.
- `sim/flight_controls/brakes_toggle_max`: Maximum braking application.

---

## 3. Engines & Powerplant

| Dataref Path | Type | Writable | Units / Range | Description |
|---|---|---|---|---|
| `sim/flightmodel/engine/ENGN_thro` | `float[8]` | Yes | `0.0` to `1.0` | Throttle lever ratio per engine. |
| `sim/flightmodel/engine/ENGN_mixt` | `float[8]` | Yes | `0.0` to `1.0` | Fuel mixture lever ratio per engine. |
| `sim/flightmodel/engine/ENGN_prop` | `float[8]` | No | RPM | Propeller or fan shaft RPM per engine. |
| `sim/flightmodel/engine/ENGN_N1_` | `float[8]` | No | Percent RPM | Turbine compressor stage 1 (N1%). |
| `sim/flightmodel/engine/ENGN_EGT` | `float[8]` | No | Celsius | Exhaust gas temperature. |
| `sim/flightmodel/engine/ENGN_oil_press`| `float[8]` | No | PSI | Engine oil pressure. |
| `sim/cockpit2/engine/actuators/throttle_ratio_all` | `float` | Yes | `0.0` to `1.0` | Master gang throttle across all engines. |

### Engine Commands
- `sim/engines/throttle_up`: Step throttle forward.
- `sim/engines/throttle_down`: Step throttle back.
- `sim/engines/engage_starters`: Engage engine electric starter motors.
- `sim/engines/thrust_reverse_toggle`: Toggle thrust reverser deployment.

---

## 4. Autopilot & Mode Control Panel (MCP)

| Dataref Path | Type | Writable | Range | Description |
|---|---|---|---|---|
| `sim/cockpit/autopilot/autopilot_mode` | `int` | Yes | `0` = Off, `1` = FD, `2` = On | Master autopilot servos state. |
| `sim/cockpit/autopilot/heading_mag` | `float` | Yes | Degrees (`0` to `360`) | Autopilot heading bug setting. |
| `sim/cockpit/autopilot/altitude` | `float` | Yes | Feet MSL | Autopilot target altitude window. |
| `sim/cockpit/autopilot/airspeed` | `float` | Yes | Knots (KIAS) | Autopilot target airspeed window. |
| `sim/cockpit/autopilot/vertical_velocity` | `float` | Yes | FPM (`-6000` to `+6000`) | Autopilot vertical speed selection. |
| `sim/cockpit2/autopilot/heading_mode` | `int` | Yes | `0`=Off, `1`=HDG, `2`=NAV | Lateral guidance mode. |
| `sim/cockpit2/autopilot/altitude_mode` | `int` | Yes | `0`=Pitch, `1`=VVI, `2`=Alt Hold | Vertical guidance mode. |
| `sim/cockpit2/autopilot/glideslope_armed`| `int` | No | `0`=Disarmed, `1`=Armed | ILS Glideslope armed status. |
| `sim/cockpit2/autopilot/glideslope_active`| `int` | No | `0`=Inactive, `1`=Captured | ILS Glideslope captured and tracking. |

### Autopilot Commands
- `sim/autopilot/servos_on`: Engage autopilot servos.
- `sim/autopilot/servos_off`: Disengage autopilot servos.
- `sim/autopilot/servos_toggle`: Toggle autopilot servos.
- `sim/autopilot/heading`: Toggle Heading Select (HDG SEL) mode.
- `sim/autopilot/nav`: Toggle Navigation (VOR/LOC/LNAV) mode.
- `sim/autopilot/approach`: Arm/activate ILS/RNAV Approach (APP) mode.
- `sim/autopilot/altitude_hold`: Hold current barometric altitude.
- `sim/autopilot/altitude_arm`: Arm pre-selected altitude capture.
- `sim/autopilot/vertical_speed`: Activate Vertical Speed (V/S) mode.

---

## 5. Radios, Transponder & Avionics

| Dataref Path | Type | Writable | Format | Description |
|---|---|---|---|---|
| `sim/cockpit/radios/com1_freq_hz` | `int` | Yes | `11800` to `13697` | COM1 active frequency in 100ths MHz (e.g. 121.50 MHz = `12150`). |
| `sim/cockpit/radios/com1_stdby_freq_hz` | `int` | Yes | `11800` to `13697` | COM1 standby frequency. |
| `sim/cockpit/radios/nav1_freq_hz` | `int` | Yes | `10800` to `11795` | NAV1 active frequency in 100ths MHz (e.g. 110.30 MHz = `11030`). |
| `sim/cockpit/radios/nav1_obs_degm` | `float` | Yes | `0` to `360` | NAV1 Omni Bearing Selector (OBS) radial. |
| `sim/cockpit/radios/transponder_code` | `int` | Yes | Octal `0000` to `7777` | Transponder squawk code (e.g. `1200`, `7000`, `7700`). |
| `sim/cockpit/radios/transponder_mode` | `int` | Yes | `0`=Off, `1`=Stby, `2`=On, `3`=Alt | Transponder mode selector. |

### Radio Commands
- `sim/radios/com1_standy_flip`: Swap COM1 active and standby frequencies.
- `sim/radios/nav1_standy_flip`: Swap NAV1 active and standby frequencies.
- `sim/transponder/transponder_ident`: Push transponder IDENT button for ATC.

---

## 6. Systems, Power & Environment

| Dataref Path | Type | Writable | Range | Description |
|---|---|---|---|---|
| `sim/cockpit2/switches/battery_on` | `int` | Yes | `0` = Off, `1` = On | Master battery switch. |
| `sim/cockpit2/switches/avionics_power_on` | `int` | Yes | `0` = Off, `1` = On | Master avionics power bus. |
| `sim/cockpit2/switches/navigation_lights_on` | `int` | Yes | `0` = Off, `1` = On | Nav position lights switch. |
| `sim/cockpit2/switches/beacon_lights_on` | `int` | Yes | `0` = Off, `1` = On | Anti-collision strobe/beacon. |
| `sim/cockpit2/switches/landing_lights_on`| `int` | Yes | `0` = Off, `1` = On | Main landing lights switch. |
| `sim/time/zulu_time_sec` | `float` | Yes | `0` to `86400` | Universal time (seconds from midnight). |
| `sim/time/sim_speed` | `int` | Yes | `1`, `2`, `4`, `8` | Simulation rate multiplier. |
| `sim/time/paused` | `int` | Yes | `0` = Running, `1` = Paused | Master simulation pause flag. |
| `sim/weather/barometer_sealevel_inhg` | `float` | Yes | inHg (e.g. `29.92`) | Sea level barometric altimeter setting. |
