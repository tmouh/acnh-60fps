#!/usr/bin/env python3
"""Apply a classic IPS patch to a file.

Made for pack/StaticParam.pack.ips (60 FPS), pack45/StaticParam45.pack.ips (45 FPS),
and pack120/StaticParam120.pack.ips (120 FPS): it turns the
game's own romfs/Pack/StaticParam.pack (from your 3.0.3 dump) into the modified one shipped in the
release zips.

  python apply_ips.py <patch.ips> <original file> <output file> [--force]

The input and output are checked against the known SHA-256 of the unmodified 3.0.3 file and of the
modified result. A file from another game version is refused, because the patch would write into
the wrong places. --force skips the check.
"""
import hashlib
import sys

CLEAN_303 = "4a3d6530d6430b6b967467f16784f91700a3cd8baad5f5b28fe3c6cfe4983298"  # StaticParam.pack, ACNH 3.0.3
PATCHED = {
    "b1e690bc18f60a1b6794526c7bd8228d3138f50c897fe23d0b631264be31e9a8",  # 60 FPS result
    "7c2538181c3ea6e0b2e4374e566995d9cb7e1d3d4fa98ff0d792b057d455bac9",  # 45 FPS result
    "ed9f8c4554560c9611a2b1ddbee3586a4e9d11cff75faaa3dc01a5433df08b36",  # 120 FPS result
}


def apply_ips(patch: bytes, data: bytes) -> bytes:
    if patch[:5] != b"PATCH":
        raise SystemExit("not an IPS file")
    buf = bytearray(data)
    i = 5
    while patch[i:i + 3] != b"EOF":
        if i + 5 > len(patch):
            raise SystemExit("the IPS file is truncated (no EOF marker); download it again")
        off = int.from_bytes(patch[i:i + 3], "big")
        size = int.from_bytes(patch[i + 3:i + 5], "big")
        i += 5
        need = 3 if size == 0 else size
        if i + need > len(patch):
            raise SystemExit("the IPS file is truncated inside a record; download it again")
        if size == 0:  # RLE record: 2-byte count, 1-byte value
            count = int.from_bytes(patch[i:i + 2], "big")
            buf[off:off + count] = patch[i + 2:i + 3] * count
            i += 3
        else:
            buf[off:off + size] = patch[i:i + size]
            i += size
    return bytes(buf)


def main(argv):
    args = [a for a in argv[1:] if a != "--force"]
    force = "--force" in argv
    if len(args) != 3:
        raise SystemExit(__doc__)
    patch_path, src, dst = args
    data = open(src, "rb").read()
    if not force and hashlib.sha256(data).hexdigest() != CLEAN_303:
        raise SystemExit(f"{src} is not the unmodified 3.0.3 StaticParam.pack (SHA-256 mismatch). "
                         "Dump it again from game version 3.0.3, or use --force.")
    out = apply_ips(open(patch_path, "rb").read(), data)
    if not force and hashlib.sha256(out).hexdigest() not in PATCHED:
        raise SystemExit("the result does not match the expected file; nothing was written")
    open(dst, "wb").write(out)
    print(f"wrote {dst} ({len(out):,} bytes)")


if __name__ == "__main__":
    main(sys.argv)
