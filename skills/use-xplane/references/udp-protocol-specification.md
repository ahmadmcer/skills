# X-Plane UDP Protocol Specification

For low-latency, high-frequency telemetry (up to 100Hz) or legacy compatibility with X-Plane 10 and 11, X-Plane provides a binary UDP protocol.

---

## 1. Network Ports & Transport

- **Inbound to X-Plane**: Port `49000` (UDP). External scripts send control commands, position updates, and dataref subscriptions here.
- **Outbound from X-Plane**: Port `49001` (UDP). X-Plane broadcasts telemetry streams and responses here.
- **Endianness**: Standard Little-Endian (`<` in Python `struct`).
- **Header**: Every datagram starts with a **5-byte ASCII header** consisting of a 4-character tag followed by a single null byte (`\0`).

---

## 2. Packet Structures & Struct Layouts

### 2.1. `DREF` - Set Dataref Value
Sets any writable floating-point or integer dataref in X-Plane.

- **Total Packet Length**: Exactly **509 bytes**.
- **Python Struct Format**: `'<5sf500s'`

| Byte Offset | Size | Type | Content |
|---|---|---|---|
| `0 - 4` | 5 bytes | String | `b"DREF\0"` |
| `5 - 8` | 4 bytes | Float (`<f`) | Target value (IEEE 754 32-bit float) |
| `9 - 508` | 500 bytes | Char array | Null-padded dataref path string |

#### Python Packing Example:
```python
import struct
import socket

def send_dref(ip: str, port: int, dataref: str, value: float):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Pad string to 500 bytes with null bytes
    dref_bytes = dataref.encode('utf-8').ljust(500, b'\x00')
    packet = struct.pack('<5sf500s', b'DREF\x00', float(value), dref_bytes)
    sock.sendto(packet, (ip, port))
```

---

### 2.2. `CMND` - Trigger Command
Fires an X-Plane command impulse (e.g. toggle gear, flap notch, autopilot disconnect).

- **Total Packet Length**: 5 bytes header + length of command string + 1 null terminator.
- **Header**: `b"CMND\0"`

#### Python Packing Example:
```python
def send_cmnd(ip: str, port: int, command: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = b'CMND\x00' + command.encode('utf-8') + b'\x00'
    sock.sendto(packet, (ip, port))
```

---

### 2.3. `RREF` - Request / Stream Dataref Subscriptions
Subscribes to specific dataref telemetry at a specified frequency (e.g. 10Hz, 20Hz).

#### Subscription Request (Client -> X-Plane Port 49000):
- **Total Packet Length**: Exactly **413 bytes**.
- **Python Struct Format**: `'<5sii400s'`

| Byte Offset | Size | Type | Content |
|---|---|---|---|
| `0 - 4` | 5 bytes | String | `b"RREF\0"` |
| `5 - 8` | 4 bytes | Int32 (`<i`) | Frequency in times per second (e.g. `10` = 10Hz, `0` = unsubscribe) |
| `9 - 12` | 4 bytes | Int32 (`<i`) | Client ID (custom user integer index to identify value in responses) |
| `13 - 412` | 400 bytes | Char array | Null-padded dataref path string |

#### Subscription Stream Response (X-Plane -> Client Port 49001):
- **Header**: `b"RREF\0"` (5 bytes)
- **Payload**: Repeating 8-byte blocks:
  - 4 bytes: `<i` Client ID
  - 4 bytes: `<f` Current float value

```python
def decode_rref(packet: bytes):
    if not packet.startswith(b'RREF\x00'):
        return {}
    results = {}
    offset = 5
    while offset + 8 <= len(packet):
        client_id, value = struct.unpack('<if', packet[offset:offset+8])
        results[client_id] = value
        offset += 8
    return results
```

---

### 2.4. `POSI` - Position Aircraft
Instantly positions the user aircraft or AI aircraft in 3D world space.

- **Total Packet Length**: **48 bytes**.
- **Python Struct Format**: `'<5sb2sdddffff'`

| Byte Offset | Size | Type | Content |
|---|---|---|---|
| `0 - 4` | 5 bytes | String | `b"POSI\0"` |
| `5` | 1 byte | Int8 (`<b`) | Aircraft index (`0` for user aircraft) |
| `6 - 7` | 2 bytes | Padding | `b"\x00\x00"` |
| `8 - 15` | 8 bytes | Double (`<d`) | Latitude (degrees) |
| `16 - 23` | 8 bytes | Double (`<d`) | Longitude (degrees) |
| `24 - 31` | 8 bytes | Double (`<d`) | Elevation (meters MSL) |
| `32 - 35` | 4 bytes | Float (`<f`) | Pitch (degrees, nose up positive) |
| `36 - 39` | 4 bytes | Float (`<f`) | Roll (degrees, right wing down positive) |
| `40 - 43` | 4 bytes | Float (`<f`) | Heading (degrees true) |
| `44 - 47` | 4 bytes | Float (`<f`) | Gear position (`0.0` = retracted, `1.0` = down) |

---

### 2.5. `DATA` - Legacy Grouped Telemetry Output
X-Plane outputs telemetry in 36-byte data groups configured in the *Settings > Data Output* screen.

- **Total Packet Length**: 5 bytes header + `N * 36` bytes.
- **Python Struct Format**: Group record is `'<i8f'` (Group Index + 8 Floats).

Common Group Indices:
- **Group 3**: Speeds (`Vind_kias`, `Vtrue_ktas`, `Vground_kts`, etc.)
- **Group 4**: Mach, VVI (`vvi_fpm`, `mach`)
- **Group 17**: Pitch, Roll, Heading (`pitch_deg`, `roll_deg`, `hding_true`, `hding_mag`)
- **Group 20**: Latitude, Longitude, Altitude (`lat_deg`, `lon_deg`, `alt_ftmsl`, `alt_ftagl`)
- **Group 25**: Engine Throttle / Mixture command
- **Group 37**: Engine RPM

---

## 3. Web API vs. UDP Comparison

| Dimension | Web API (REST & WebSocket) | UDP Binary Protocol |
|---|---|---|
| **Port** | 8086 (HTTP/WS) | 49000 (In) / 49001 (Out) |
| **Data Format** | Standard JSON | Packed binary structs |
| **Max Rate** | ~10Hz (WebSocket) | 60Hz - 100Hz (Per flight loop) |
| **Connection State** | Persistent HTTP/WS | Connectionless UDP datagrams |
| **Flight Reset** | Full `POST /flight` support | Only repositioning via `POSI` |
| **Dataref Discovery** | Dynamic search endpoint | Static lookup required |
| **Supported In** | X-Plane 12.1.1+ | X-Plane 10, 11, 12 |
