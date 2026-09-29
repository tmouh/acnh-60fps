#!/usr/bin/env python3
"""Convert an IPSwitch .pchtxt (emulator patch text) into the .ips file Atmosphere loads.

  pchtxt_to_ips.py <file.pchtxt> <out_dir>      writes <out_dir>/<NSO BUILD ID>.ips

Atmosphere applies `atmosphere/exefs_patches/<any name>/<build id>.ips` to the executable whose
build id matches the file name. Offsets in the .ips count from the start of the NSO file, header
(0x100) included; a pchtxt written against code addresses says so with `@flag offset_shift 0x100`,
which is added here. IPS32 (4-byte offsets) is used because ACNH patches sit above 16 MB.
Only `@enabled` blocks are converted; `@disabled` blocks and comments are skipped.
"""
from __future__ import annotations

import os
import re
import struct
import sys


def parse(text: str):
    bid, shift, on, recs = None, 0, False, []
    for raw in text.splitlines():
        line = raw.split("//")[0].strip()
        if not line or line.startswith("#"):
            continue
        low = line.lower()
        if low.startswith("@nsobid-"):
            bid = line.split("-", 1)[1].strip().upper()
        elif low.startswith("@flag offset_shift"):
            shift = int(line.split()[-1], 16)
        elif low.startswith("@enabled"):
            on = True
        elif low.startswith(("@disabled", "@stop")):
            on = False
        elif low.startswith("@"):
            continue
        elif on:
            m = re.fullmatch(r"([0-9A-Fa-f]{8})\s+((?:[0-9A-Fa-f]{2})+)", line)
            if not m:
                raise ValueError(f"unreadable patch line: {raw!r}")
            recs.append((int(m.group(1), 16) + shift, bytes.fromhex(m.group(2))))
    if not bid:
        raise ValueError("no @nsobid line")
    return bid, recs


def to_ips32(recs) -> bytes:
    out = bytearray(b"IPS32")
    for off, data in recs:
        if off == 0x45454F46:
            raise ValueError("offset collides with the EEOF marker")
        out += struct.pack(">IH", off, len(data)) + data
    return bytes(out + b"EEOF")


def main(argv):
    src, out_dir = argv[1], argv[2]
    bid, recs = parse(open(src, encoding="utf-8", errors="replace").read())
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, bid + ".ips")
    open(dst, "wb").write(to_ips32(recs))
    print(f"{os.path.basename(src)} -> {dst} ({len(recs)} patches, {os.path.getsize(dst)} B)")


if __name__ == "__main__":
    main(sys.argv)
