"""Run every project regression. THE MERGE GATE: nothing changes unless this is green.

    python run_all_tests.py

Add a project: drop its test in projects/<name>/test.py and it is picked up
automatically.
"""
import glob
import subprocess
import sys
import os

def discover():
    return sorted(glob.glob("projects/*/test.py"))

def main():
    tests = discover()
    if not tests:
        print("No tests found."); return 1

    print("=" * 62)
    print(f"io2cable — running {len(tests)} project regression(s)")
    print("=" * 62)

    results = []
    for t in tests:
        name = os.path.basename(os.path.dirname(t))
        r = subprocess.run([sys.executable, t], capture_output=True, text=True)
        tail = [l for l in r.stdout.strip().splitlines() if "checks" in l]
        summary = tail[-1] if tail else ("OK" if r.returncode == 0 else "ERROR")
        ok = r.returncode == 0
        results.append((name, ok, summary))
        print(f"  {'PASS' if ok else 'FAIL'}  {name:24} {summary}")
        if not ok:
            for line in r.stdout.strip().splitlines():
                if line.startswith("FAIL"):
                    print(f"        {line}")
            if r.stderr.strip():
                print(f"        {r.stderr.strip().splitlines()[-1]}")

    print("-" * 62)
    passed = sum(1 for _, ok, _ in results if ok)
    if passed == len(results):
        print(f"ALL GREEN — {passed}/{len(results)} projects reproduce their validated list.")
        print("Safe to merge.")
        return 0
    print(f"{passed}/{len(results)} passed — DO NOT MERGE until green.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
