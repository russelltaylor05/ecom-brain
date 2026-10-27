#!/usr/bin/env python3
"""Initialize or inspect a complete, resumable Content Studio answer inventory."""
import argparse
import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
STATUSES = {'unanswered', 'partial', 'sourced', 'user_confirmed', 'inferred', 'unknown',
            'deferred', 'not_applicable'}


def run(root, action):
    questions = json.loads((SKILL / 'references/questions.json').read_text())
    ids = {q['id'] for q in questions}
    path = Path(root) / 'research/content-studio/answers.json'
    if action == 'init' and not path.exists():
        data = {'form': 'Content Studio Intake (Operator Academy)', 'answers': {
            q['id']: {'answer': '', 'status': 'unanswered', 'sources': [],
                      'updated': None, 'notes': ''} for q in questions}}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    if not path.exists():
        return {'initialized': False, 'question_records': len(ids)}
    data = json.loads(path.read_text())
    answers = data['answers']
    if set(answers) != ids:
        raise ValueError('Answer IDs do not match the question inventory; preserve existing data and reconcile')
    counts = {status: 0 for status in sorted(STATUSES)}
    for key, record in answers.items():
        if record['status'] not in STATUSES or not isinstance(record['answer'], str):
            raise ValueError(f'Invalid answer or status: {key}')
        if not isinstance(record['sources'], list) or not isinstance(record['notes'], str):
            raise ValueError(f'Invalid evidence fields: {key}')
        if record['status'] in {'sourced', 'user_confirmed', 'inferred'} and not record['answer'].strip():
            raise ValueError(f'Answered field is empty: {key}')
        if record['status'] == 'sourced' and not record['sources']:
            raise ValueError(f'Sourced answer lacks evidence: {key}')
        counts[record['status']] += 1
    return {'initialized': True, 'question_records': len(ids), 'counts': counts,
            'readiness': 'Requires evidence review; coverage counts alone do not establish readiness'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init', 'status'])
    parser.add_argument('--root', type=Path, default=SKILL.parents[1])
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.action), indent=2))
