# PLANE_DETECTION_COMPACT

Local StableKite MAVLink 2 message ID **61000**, CRC_EXTRA **152**.
ID 61000 was unused in every XML message definition in this repository when
introduced. This is a local dialect choice, not a global MAVLink allocation.
Legacy messages and their wire layouts are unchanged.

The logical payload is exactly four uint8 fields in this order:

| Byte | Field | Meaning |
| --- | --- | --- |
| 0 | `record_index` | Cyclic record counter 1..255; 0 cancels `track_id` |
| 1 | `track_id` | Persistent ID 1..255; 0 clears all detections |
| 2 | `center_x` | Box center, normalized 0..255 from the left |
| 3 | `center_y` | Box center, normalized 0..255 from the top |

A normal observation refreshes one active ID. Repeated observations of that ID
do not increase the count. `(0, id, 0, 0)` immediately removes that ID.
`(0, 0, 0, 0)` clears the count, including at startup or on an empty frame.
Cancellation coordinates are ignored. The record counter does not delimit a
video frame and zero is reserved; after 255 the normal counter returns to 1.

Receivers should also expire IDs after a short interval without refresh to
recover from lost radio packets. The demonstrator uses a configurable 100 ms
timeout, with immediate explicit cancellation. Choose this from the measured
hybrid output / link cadence, not just the sensor frame rate. No frame number,
box dimensions, confidence or timestamp is included in these four bytes.

Standard MAVLink 2 removes trailing zero payload bytes, so the serialized
payload is 1..4 bytes (unsigned packets are 13..16 bytes with framing and CRC).
Decode omitted trailing bytes as zero using the generated library. A signed
packet adds the standard 13-byte signature. MAVLink 1 cannot carry this ID.

Generate/install from the repository normally; for a common-only build:

```sh
MAVLINK_DIALECT=common PYMAVLINK_FAST_INDEX=0 python3 -m pip wheel --no-deps .
python3 -m unittest discover -s tests -p test_detection_compact.py
```
