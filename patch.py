"""Patch io2cable/classify.py: add opt-in '&'-separated AND-pattern matching.
Run from the repo root: python patch_classify_and_pattern.py
Then verify: git diff io2cable\\classify.py
"""
import re

PATH = "io2cable/classify.py"

HELPERS = '''

def _pattern_matches(pat, text):
    if "&" not in pat:
        return pat in text
    return all(p.strip() in text for p in pat.split("&"))


def _pattern_length(pat):
    if "&" not in pat:
        return len(pat)
    return sum(len(p.strip()) for p in pat.split("&"))
'''

with open(PATH, encoding="utf-8") as f:
    src = f.read()

changed = False

# 1. Insert helpers right after the STRUCTURAL definition, if not already present.
if "_pattern_matches" not in src:
    marker = re.search(r'STRUCTURAL = \{[^\}]*\}\n', src)
    if not marker:
        raise SystemExit("Could not find the STRUCTURAL = {...} line -- nothing changed. "
                          "Paste the actual line so the anchor can be fixed.")
    insert_at = marker.end()
    src = src[:insert_at] + HELPERS + src[insert_at:]
    changed = True
    print("Inserted _pattern_matches/_pattern_length after STRUCTURAL.")
else:
    print("_pattern_matches already present -- skipping helper insertion.")

# 2. Swap the matches= line to use the new helpers, if not already swapped.
old_line = 'matches = [(prio, len(pat), ftype) for pat, ftype, prio in cfg.synonyms if pat in text]'
new_line = 'matches = [(prio, _pattern_length(pat), ftype) for pat, ftype, prio in cfg.synonyms if _pattern_matches(pat, text)]'

if old_line in src:
    src = src.replace(old_line, new_line)
    changed = True
    print("Replaced the matches= line.")
elif new_line in src:
    print("matches= line already updated -- skipping.")
else:
    raise SystemExit(
        "Could not find the expected matches= line (old or new form). "
        "Nothing changed -- the file may already differ from what this patch expects. "
        "Paste the current matches= line so the anchor can be fixed."
    )

if changed:
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(src)
    print("Wrote", PATH)
else:
    print("No changes needed -- file already patched.")

# Self-check: read back and confirm both pieces are actually there.
with open(PATH, encoding="utf-8") as f:
    verify = f.read()
assert "_pattern_matches" in verify, "Post-write check FAILED: helper not found after save."
assert "_pattern_length(pat)" in verify.split("matches = [")[1][:80], \
    "Post-write check FAILED: matches= line not updated after save."
print("Post-write verification passed.")