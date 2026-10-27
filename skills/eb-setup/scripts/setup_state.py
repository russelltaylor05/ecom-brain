#!/usr/bin/env python3
# Persist onboarding answers and verify completion without changing Git or company content.
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[3]
TEXT = {'company_name', 'website', 'user_name', 'timezone', 'priorities',
        'company_description', 'remote_url', 'branch'}
BOOL = {'auto_commit', 'auto_push', 'remote_confirmed'}
FIELDS = TEXT | BOOL | {'social_profiles'}
CHECKLIST = {
    'company_overview': ('Company name, industry, and description', False),
    'products': ('Main products/services and differentiators', False),
    'pricing': ('Public pricing, currency, and billing terms', False),
    'customers': ('Intended customers and use cases', False),
    'markets': ('Markets served and sales model', False),
    'sources': ('Sources and dates recorded', False),
    'auto_save_offer': ('Optional auto-save note delivered', True),
    'github_repository': ('GitHub repository verified for this project', True),
}
CHECKLIST_STATUSES = {'pending', 'in_progress', 'done', 'unavailable', 'deferred'}


def validate_checklist(checklist):
    if not isinstance(checklist, dict) or set(checklist) - CHECKLIST.keys():
        raise ValueError('Unknown checklist item or invalid checklist object')
    for item in checklist.values():
        if (not isinstance(item, dict) or set(item) != {'status', 'note'}
                or not isinstance(item['status'], str)
                or item['status'] not in CHECKLIST_STATUSES
                or not isinstance(item['note'], str) or not item['note'].strip()):
            raise ValueError('Checklist items need a valid status and a nonempty note')


def checklist_status(root, state):
    answers = state['answers']
    result = {
        'company_input': {
            'label': 'Company source received (website, storefront, or social profile)',
            'status': 'done' if answers.get('website') or answers.get('social_profiles') or answers.get('company_description', '').strip() else 'pending',
            'optional': False,
            'note': 'Required company input: request a public link; use a description only if no link exists.',
        }
    }
    for key, (label, optional) in CHECKLIST.items():
        result[key] = {'label': label, 'optional': optional,
                       **state.get('checklist', {}).get(key, {
                           'status': 'deferred' if optional and key != 'auto_save_offer' else 'pending',
                           'note': ('Mention optional auto-save at completion; no answer required.'
                                    if key == 'auto_save_offer' else
                                    'Optional follow-up; outside basic setup.' if optional else 'Not recorded yet.'),
                       })}
    commit_enabled = answers.get('auto_commit', False)
    push_enabled = answers.get('auto_push', False)
    result['auto_save'] = {
        'label': 'Auto-save preferences', 'optional': True,
        'status': 'done' if 'auto_commit' in answers or 'auto_push' in answers else 'deferred',
        'note': f'Automatic commits: {"on" if commit_enabled else "off"}; '
                f'automatic pushes: {"on" if push_enabled else "off"}. '
                'Off by default; optional and can be configured later.',
    }
    recorded = bool(state.get('profile_sha256') and state['profile_sha256'] == profile_hash(root))
    result['profile_saved'] = {
        'label': 'Current company profile saved', 'optional': False,
        'status': 'done' if recorded else 'pending',
        'note': 'Current profile recorded; this does not imply user approval.' if recorded else 'Save and record the sourced profile.',
    }
    result['setup_complete'] = {
        'label': 'Basic setup complete', 'optional': False,
        'status': 'done' if state['complete'] and not missing(root, state) else 'pending',
        'note': 'Research gaps and optional follow-ups do not block completion.',
    }
    return result


def validate(answers):
    if not isinstance(answers, dict) or set(answers) - FIELDS:
        raise ValueError('Unknown answer field or invalid answer object')
    for key, value in answers.items():
        if key in TEXT and not isinstance(value, str):
            raise ValueError(f'{key} must be text')
        if key in BOOL and type(value) is not bool:
            raise ValueError(f'{key} must be a JSON boolean')
    urls = answers.get('social_profiles', [])
    if not isinstance(urls, list) or any(not isinstance(url, str) for url in urls):
        raise ValueError('social_profiles must be a URL array')
    if answers.get('website'):
        urls = urls + [answers['website']]
    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme not in ('https', 'http') or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('Use public http(s) URLs without credentials')
    if answers.get('timezone'):
        try:
            ZoneInfo(answers['timezone'])
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError('Use an available IANA timezone, such as Europe/London')
    if answers.get('auto_push', False) != answers.get('auto_commit', False):
        raise ValueError('Auto-save requires both commits and GitHub pushes, or both off')


def load(root):
    path = root / '.brain/setup.json'
    if not path.exists():
        return {'version': 1, 'answers': {}, 'profile_sha256': None, 'complete': False}
    state = json.loads(path.read_text())
    if not isinstance(state, dict) or state.get('version') != 1:
        raise ValueError('Unsupported setup state version')
    validate(state['answers'])
    # Older runs tracked a separate draft; profile_saved now derives from the saved file.
    if isinstance(state.get('checklist'), dict):
        state['checklist'].pop('profile_draft', None)
    validate_checklist(state.get('checklist', {}))
    return state


def save(root, state):
    directory = root / '.brain'
    directory.mkdir(exist_ok=True)
    path = directory / 'setup.json'
    temporary = directory / 'setup.json.new'
    temporary.write_text(json.dumps(state, indent=2) + '\n')
    os.replace(temporary, path)


def profile_hash(root):
    path = root / 'COMPANY.md'
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def missing(root, state):
    answers = state['answers']
    # A researched company name and a public source or manual description are enough.
    # Personal details are optional; absent saving preferences remain disabled.
    items = ['company_name'] if not answers.get('company_name', '').strip() else []
    if not (answers.get('website') or answers.get('social_profiles')
            or answers.get('company_description', '').strip()):
        items.append('company source (website, storefront, or social profile; description if no link exists)')
    if answers.get('auto_push'):
        items += [key for key in ('remote_url', 'branch', 'remote_confirmed') if not answers.get(key)]
    if not state.get('profile_sha256') or state['profile_sha256'] != profile_hash(root):
        items.append('recorded current COMPANY.md')
    return items


def run(root, action, patch=None):
    state = load(root)
    if action == 'update':
        if not isinstance(patch, dict) or set(patch) - FIELDS:
            raise ValueError('Patch must contain only supported answer fields')
        answers = dict(state['answers'])
        answers.update(patch)
        validate(answers)
        if answers != state['answers']:
            # A new destination requires a new confirmation, even if the old state was confirmed.
            if any(answers.get(k) != state['answers'].get(k) for k in ('remote_url', 'branch')):
                answers['remote_confirmed'] = patch.get('remote_confirmed', False)
            if any(state['answers'].get(k) and answers.get(k) != state['answers'].get(k)
                   for k in ('website', 'company_name', 'company_description')):
                state['checklist'] = {
                    key: {'status': 'pending', 'note': 'Recheck after company details changed. ' + item['note']}
                    for key, item in state.get('checklist', {}).items() if not CHECKLIST[key][1]
                } | {
                    key: item for key, item in state.get('checklist', {}).items() if CHECKLIST[key][1]
                }
            profile_fields = FIELDS - BOOL - {'remote_url', 'branch'}
            if any(answers.get(k) != state['answers'].get(k) for k in profile_fields):
                state['profile_sha256'] = None
            state['complete'] = False
        state['answers'] = answers
        save(root, state)
    elif action == 'checklist':
        validate_checklist(patch)
        state['checklist'] = {**state.get('checklist', {}), **patch}
        save(root, state)
    elif action == 'record-profile':
        path = root / 'COMPANY.md'
        if not path.exists() or not any(
                line in ('Status: Researched', 'Status: Approved')
                for line in path.read_text().splitlines()):
            raise ValueError('Write the sourced profile with Status: Researched before recording it')
        state['profile_sha256'] = profile_hash(root)
        # Recording a later profile edit must not reopen completed onboarding. Answer
        # changes still invalidate completion in update; initial setup stays incomplete.
        state['complete'] = state['complete'] and not missing(root, state)
        save(root, state)
    elif action == 'complete':
        pending = missing(root, state)
        if pending:
            raise ValueError('Setup incomplete: ' + ', '.join(pending))
        state['complete'] = True
        save(root, state)
    pending = missing(root, state)
    return {'complete': state['complete'] and not pending, 'missing': pending,
            'answers': state['answers'], 'checklist': checklist_status(root, state)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['status', 'update', 'checklist', 'record-profile', 'complete'])
    parser.add_argument('patch', nargs='?', type=Path)
    args = parser.parse_args()
    try:
        if args.action in ('update', 'checklist') and not args.patch:
            raise ValueError(f'{args.action} requires a JSON patch file')
        patch = json.loads(args.patch.read_text()) if args.patch else None
        print(json.dumps(run(ROOT, args.action, patch), indent=2))
    except (ValueError, KeyError, OSError) as error:
        print(f'Setup error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
