#!/usr/bin/env python3
"""Validate msf skills. Errors fail the run; warnings are informational."""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors, warnings = [], []

def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    body = m.group(1)
    name = re.search(r"^name:\s*(.+)$", body, re.M)
    desc = re.search(r"^description:\s*(.*?)(?=^[A-Za-z][\w-]*:|\Z)", body, re.S | re.M)
    d = ""
    if desc:
        d = re.sub(r"^[>|][-+]?\s*", "", desc.group(1).strip())
        d = re.sub(r"\s*\n\s*", " ", d).strip().strip("\"'")
    return (name.group(1).strip().strip("\"'") if name else None), d

def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)

def names_in(sub):
    return {os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT, sub, "**", "SKILL.md"), recursive=True)}

active = names_in("skills")
staged = names_in("skills-staging")
secret = re.compile(r"(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")

for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
    d = os.path.dirname(path)
    folder = os.path.basename(d)
    rel = os.path.relpath(path, ROOT)
    text = open(path, encoding="utf-8", errors="ignore").read()
    fm = frontmatter(text)
    if not fm:
        errors.append(f"{rel}: missing frontmatter"); continue
    name, desc = fm
    if name != folder: errors.append(f"{rel}: name '{name}' != folder '{folder}'")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", folder): errors.append(f"{rel}: invalid folder/name format")
    if not desc: errors.append(f"{rel}: empty description")
    elif len(desc) > 1024: errors.append(f"{rel}: description {len(desc)} chars (>1024)")
    prose = strip_code(text)
    for link in re.findall(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)", prose):
        target = link.split("#")[0]
        if target and not os.path.exists(os.path.normpath(os.path.join(d, target))):
            errors.append(f"{rel}: broken relative link '{link}'")
    for called in re.findall(r"Skill tool (?:with|for) [\"“]([a-z0-9-]+)[\"”]", text):
        if called not in active:
            (warnings if called in staged else errors).append(f"{rel}: calls skill '{called}' which is {'staged, not active' if called in staged else 'missing'}")
    no_fences = re.sub(r"```.*?```", "", text, flags=re.S)
    for ref in set(re.findall(r"(?:`|\*\*)([a-z0-9]+(?:-[a-z0-9]+)+)(?:`|\*\*)", no_fences)):
        if ref in staged and ref not in active and ref != folder:
            warnings.append(f"{rel}: mentions staged skill '{ref}'")
    for f in glob.glob(os.path.join(d, "**", "*"), recursive=True):
        if os.path.isfile(f) and f.endswith((".md", ".sh", ".mjs", ".json", ".txt")):
            m = secret.search(open(f, encoding="utf-8", errors="ignore").read())
            if m: errors.append(f"{os.path.relpath(f, ROOT)}: secret-like string '{m.group(0)[:12]}...'")

print(f"active skills: {len(active)} | staged: {len(staged)}")
for w in warnings: print("warn :", w)
for e in errors: print("ERROR:", e)
print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
