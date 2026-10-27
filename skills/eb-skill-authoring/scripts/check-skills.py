#!/usr/bin/env python3
# Check portable skill metadata, index entries, and relative discovery links.
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[3]
errors = []
index = (root / 'SKILLS.md').read_text()
for folder in sorted((root / 'skills').iterdir()):
    if not folder.is_dir():
        continue
    entry = folder / 'SKILL.md'
    if not folder.name.startswith('eb-') and folder.name != 'evans-content-studio':
        errors.append(f'Missing eb- prefix: {folder.name}')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', folder.name) or len(folder.name) > 64:
        errors.append(f'Invalid skill name: {folder.name}')
    if not entry.exists():
        errors.append(f'Missing {entry.relative_to(root)}')
        continue
    text = entry.read_text()
    front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not front or not re.search(r'^name: ' + re.escape(folder.name) + r'$', front[1], re.M):
        errors.append(f'Invalid frontmatter name: {folder.name}')
    if not front or not re.search(r'^description: \S.+$', front[1], re.M):
        errors.append(f'Missing description: {folder.name}')
    if f'(skills/{folder.name}/SKILL.md)' not in index:
        errors.append(f'Missing index entry: {folder.name}')
    link = root / '.agents/skills' / folder.name
    if not link.is_symlink() or link.readlink().is_absolute() or link.resolve() != folder.resolve():
        errors.append(f'Invalid discovery link: {folder.name}')
for error in errors:
    print(error, file=sys.stderr)
print(f'Skill validation: {len(errors)} error(s)')
sys.exit(bool(errors))
