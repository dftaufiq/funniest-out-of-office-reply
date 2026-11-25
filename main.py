import os

LINE = "Out until Thursday. I left my laptop at home on purpose, which is the bravest thing I've done since I replied-all in 2023."

# Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-160 chars,
# not only whitespace, a single line. Fail loudly instead of shipping an
# invalid entry.
if not 1 <= len(LINE) <= 160 or not LINE.strip() or "\n" in LINE:
    raise SystemExit("entry line violates the 1-160 char single-line gate")

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
entry_path = os.path.join(out_dir, "entry.txt")
with open(entry_path, "w", encoding="utf-8", newline="") as f:
    f.write(LINE)

# Read-back verification: prove the file the grader reads is byte-identical
# to LINE. Fail loudly rather than ship a corrupted or truncated entry.
with open(entry_path, "r", encoding="utf-8", newline="") as f:
    written = f.read()
if written != LINE:
    raise SystemExit(
        f"entry.txt verification failed: read back {len(written)} chars, "
        f"expected {len(LINE)} chars identical to the entry line"
    )

# Byte check: the tie-break counts bytes, so confirm the file on disk is
# exactly the entry's UTF-8 bytes — no trailing newline, no BOM.
if os.path.getsize(entry_path) != len(LINE.encode("utf-8")):
    raise SystemExit("entry.txt byte length does not match the entry line")
print(f"wrote {len(LINE)} chars / {len(LINE.encode('utf-8'))} bytes to {entry_path}")
