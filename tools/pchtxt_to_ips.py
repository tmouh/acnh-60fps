#!/usr/bin/env python3
"""Convert an IPSwitch .pchtxt (emulator patch text) into the .ips file Atmosphere loads.

  pchtxt_to_ips.py <file.pchtxt> <out_dir>      writes <out_dir>/<NSO BUILD ID>.ips

Atmosphere applies `atmosphere/exefs_patches/<any name>/<build id>.ips` to the executable whose
build id matches the file name. Offsets in the .ips count from the start of the NSO file, header
(0x100) included; a pchtxt written against code addresses says so with `@flag offset_shift 0x100`,
which is added here. IPS32 (4-byte offsets) is used because ACNH patches sit above 16 MB.

The file is read the way the emulators read it (Ryujinx, and the yuzu-family reader in Citron and
Eden), so the .ips holds exactly the bytes an emulator would patch:
  - line 1 must be the @nsobid- line;
  - @enabled starts a block of patch lines; @disabled starts a block that is skipped;
  - a blank line ends the block; patch lines after it are ignored until the next @enabled;
  - @stop ends the file;
  - @flag offset_shift takes 0x-prefixed hex or plain decimal.
Where the two readers would patch different bytes, the file is refused with the line number:
a comment or other text inside a block, @stop right after patch lines, a leading-zero or
malformed offset_shift, @little-endian, leading whitespace, an ambiguous patch line.
"""
from __future__ import annotations

import os
import re
import struct
import sys

PATCH = re.compile(r"([0-9A-Fa-f]{8}) ((?:[0-9A-Fa-f]{2})+)(?: *//.*)?")
SHIFT = re.compile(r"@flag offset_shift (0[xX][0-9A-Fa-f]+|0|[1-9][0-9]*) *(?://.*)?")


def parse(text: str):
    lines = [ln[:-1] if ln.endswith("\r") else ln for ln in text.split("\n")]
    if not lines or not lines[0].startswith("@nsobid-"):
        raise ValueError("line 1 must be the @nsobid-<build id> line (Ryujinx reads the build id from line 1 only)")
    bid = lines[0][8:].strip().upper()
    if not re.fullmatch(r"[0-9A-F]{1,64}", bid):
        raise ValueError(f"line 1: unreadable build id {bid!r}")
    shift, block, recs, skipped = 0, None, [], []  # block: None outside a block, True/False = @enabled/@disabled

    def fail(n, why, line):
        raise ValueError(f"line {n}: {why}: {line!r}")

    for n, line in enumerate(lines[1:], 2):
        if not line.strip():
            if block is not None and len(line) >= 11:
                fail(n, "a whitespace-only line of 11 or more characters is a patch line to the yuzu-family reader", line)
            block = None  # both readers end the block here
            continue
        if line[0].isspace():
            fail(n, "leading whitespace (Ryujinx trims it, the yuzu-family reader does not)", line)
        if line.startswith("@enabled") or line.startswith("@disabled"):
            block = line.startswith("@enabled")
        elif line.startswith("@stop"):
            if block is not None:
                fail(n, "@stop directly after patch lines (the yuzu-family reader ignores it there, Ryujinx stops); "
                        "put a blank line before it", line)
            break
        elif line.startswith("@flag offset_shift"):
            m = SHIFT.fullmatch(line)
            if not m:
                fail(n, "offset_shift must be 0x-prefixed hex or plain decimal (a leading zero is octal to the "
                        "yuzu-family reader and decimal to Ryujinx)", line)
            shift = int(m.group(1), 0)
        elif line.startswith("@little-endian"):
            fail(n, "@little-endian is not supported (Ryujinx ignores it, the yuzu-family reader reverses the bytes)", line)
        elif line.startswith("@nsobid-"):
            fail(n, "a second @nsobid- line", line)
        elif line.startswith("@"):
            continue  # other directives (@big-endian, @flag print_values, ...) change no bytes in either reader
        elif block is not None:
            m = PATCH.fullmatch(line)
            if not m:
                fail(n, "not a patch line inside a block (the yuzu-family reader would patch it in as junk "
                        "or end the block; put comments before @enabled)", line)
            if block:
                recs.append((int(m.group(1), 16) + shift, bytes.fromhex(m.group(2))))
        elif line.startswith("//") or line.startswith("#"):
            continue
        elif PATCH.fullmatch(line):
            skipped.append(n)  # outside any block: neither reader applies it
        else:
            fail(n, "unreadable line", line)
    seen = {}
    for off, data in recs:
        for k in range(off, off + len(data)):
            if k in seen:
                raise ValueError(f"patch bytes overlap at 0x{k:X} (the yuzu-family reader applies a block's lines "
                                 f"in offset order, not file order)")
            seen[k] = True
    return bid, recs, skipped


def to_ips32(recs) -> bytes:
    out = bytearray(b"IPS32")
    for off, data in recs:
        if off == 0x45454F46:
            raise ValueError("offset collides with the EEOF marker")
        out += struct.pack(">IH", off, len(data)) + data
    return bytes(out + b"EEOF")


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: python pchtxt_to_ips.py <file.pchtxt> <out_dir>")
    src, out_dir = argv[1], argv[2]
    try:
        bid, recs, skipped = parse(open(src, encoding="utf-8").read())
    except (ValueError, UnicodeDecodeError) as e:
        raise SystemExit(f"{src}: {e}")
    for n in skipped:
        print(f"warning: line {n} is a patch line outside any @enabled block; no emulator applies it, so it is skipped",
              file=sys.stderr)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, bid + ".ips")
    with open(dst, "wb") as f:
        f.write(to_ips32(recs))
    print(f"{os.path.basename(src)} -> {dst} ({len(recs)} patches, {os.path.getsize(dst)} B)")


if __name__ == "__main__":
    main(sys.argv)
