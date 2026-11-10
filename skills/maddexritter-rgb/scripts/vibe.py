#!/usr/bin/env python3
"""Pinned, credential-free Vibe Editing setup and local render adapter."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from types import SimpleNamespace

URL = 'https://github.com/maddexritter-rgb/vibe-editing.git'
REVISION = 'a342d7173d49b6be43e477a0041aad6014fbf377'
SCRIPT = Path(__file__).resolve()
ADAPTER_VERSION = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()[:16]
SKIPPED = ['AssemblyAI', 'Gemini', 'Groq', 'live editorial access', 'Frame.io', 'Monday']


def run(cmd, **kwargs):
    return subprocess.run([str(x) for x in cmd], check=True, **kwargs)


def capture(cmd):
    return run(cmd, capture_output=True, text=True).stdout.strip()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plugin(runtime):
    return runtime / 'upstream/plugins/vibe-editing'


def check_source(runtime):
    checkout = runtime / 'upstream'
    if capture(['git', '-C', checkout, 'remote', 'get-url', 'origin']) != URL:
        raise ValueError('Runtime origin does not match the pinned project')
    if capture(['git', '-C', checkout, 'rev-parse', 'HEAD']) != REVISION:
        raise ValueError('Runtime revision does not match the skill pin')
    if capture(['git', '-C', checkout, 'status', '--porcelain', '--untracked-files=no']):
        raise ValueError('Runtime source has local changes; use a new runtime directory')


def setup(runtime):
    runtime.mkdir(parents=True, exist_ok=True)
    checkout = runtime / 'upstream'
    if not checkout.exists():
        run(['git', 'clone', '--no-checkout', URL, checkout])
        run(['git', '-C', checkout, 'checkout', '--detach', REVISION])
    check_source(runtime)
    venv = runtime / '.venv'
    if not venv.exists():
        run([sys.executable, '-m', 'venv', venv])
    python = venv / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    run([python, '-m', 'pip', 'install', 'Pillow==12.0.0', 'imageio-ffmpeg==0.6.0'])
    env = dict(os.environ)
    env.pop('IMAGEIO_FFMPEG_EXE', None)
    binary = run([python, '-c', 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'],
                 env=env, capture_output=True, text=True).stdout.strip()
    local_bin = runtime / 'bin'
    local_bin.mkdir(exist_ok=True)
    link = local_bin / 'ffmpeg'
    if not link.exists():
        link.symlink_to(binary)
    save(runtime / 'status.json', {
        'revision': REVISION, 'mode': 'local', 'services_skipped': SKIPPED,
        'brand': 'deferred until user footage', 'editing': 'pending real user clip',
    })
    run([python, SCRIPT, '--runtime', runtime, 'doctor'])


def doctor(runtime):
    check_source(runtime)
    checks = {tool: shutil.which(tool) is not None for tool in ['ffmpeg', 'ffprobe']}
    if checks['ffmpeg']:
        filters = capture(['ffmpeg', '-hide_banner', '-filters'])
        encoders = capture(['ffmpeg', '-hide_banner', '-encoders'])
        checks.update(libass=' ass ' in filters, libx264='libx264' in encoders,
                      aac=' aac ' in encoders)
    try:
        import PIL
        checks['Pillow'] = bool(PIL.__version__)
    except ImportError:
        checks['Pillow'] = False
    root = plugin(runtime)
    for name in ['skills/render/engine.py', 'skills/caption-clips/scripts/generate_spice.py',
                 'skills/caption-clips/presets/spice.json',
                 'skills/caption-clips/fonts/free_font/Montserrat-ExtraBold.otf']:
        checks[name] = (root / name).is_file()
    result = {'local_tools_ready': all(checks.values()), 'checks': checks,
              'services_skipped': SKIPPED, 'production_onboarding': 'pending real user clip'}
    save(runtime / 'doctor.json', result)
    print(json.dumps(result, indent=2))
    if not result['local_tools_ready']:
        raise ValueError('Local tools missing; see doctor.json and references/setup.md')


def software_ff(cmd, **kwargs):
    # Upstream cut/mix hardcode VideoToolbox. Use the same FFmpeg stages on other platforms.
    return run(['libx264' if str(x) == 'h264_videotoolbox' else x for x in cmd], **kwargs)


def reframe(**args):
    prior = list(args['inputs'].values())[-1]
    run(['ffmpeg', '-y', '-v', 'error', '-i', prior,
         '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1',
         '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-c:a', 'copy', args['out_path']])
    return {'out': str(args['out_path']), 'meta': list(args['inputs_meta'].values())[-1]}


def captions(root, **args):
    cfg, project, work = args['config'], args['project'], args['work_dir']
    words = project / cfg['words']
    normalized = work / 'normalized.json'
    formatter = root / 'skills/caption-clips/scripts/spice_format.py'
    run([sys.executable, formatter, '--words', words, normalized])
    generator = load_module('eb_spice', root / 'skills/caption-clips/scripts/generate_spice.py')
    generator.encoder_args_for = None
    argv = [str(generator.__file__), str(normalized), '--out', str(work / 'captions.ass'),
            '--preset', str(root / 'skills/caption-clips/presets/spice.json'),
            '--no-onset-correct', '--burn', list(args['inputs'].values())[-1],
            '--burn-out', str(args['out_path'])]
    if cfg.get('director'):
        argv += ['--style', str(project / cfg['director'])]
    original = sys.argv
    try:
        sys.argv = argv
        result = generator.main()
        if result:
            raise RuntimeError(f'Caption generator failed: {result}')
    finally:
        sys.argv = original
    return {'out': str(args['out_path']), 'meta': list(args['inputs_meta'].values())[-1]}


def render(runtime, project):
    check_source(runtime)
    manifest = json.loads((project / 'manifest.json').read_text())
    if manifest['pipeline'] != 'eb-local':
        raise ValueError('Local mode only supports pipeline eb-local')
    root = plugin(runtime)
    engine = load_module('eb_render', root / 'skills/render/engine.py')
    pipeline_dir = runtime / 'pipelines'
    save(pipeline_dir / 'eb-local.json', {'stages': ['cut', 'reframe', 'captions', 'mix']})
    engine.PIPELINES_DIR = pipeline_dir
    upstream_load = engine.load_stage

    def local_stage(name):
        if name == 'reframe':
            return SimpleNamespace(VERSION=ADAPTER_VERSION, run=reframe)
        if name == 'captions':
            return SimpleNamespace(VERSION=ADAPTER_VERSION,
                                   run=lambda **kw: captions(root, **kw))
        if name not in {'cut', 'mix'}:
            raise ValueError(f'Unsupported local stage: {name}')
        stage = upstream_load(name)
        stage.ff = software_ff
        stage.VERSION += '+' + ADAPTER_VERSION
        return stage

    engine.load_stage = local_stage
    original = sys.argv
    try:
        sys.argv = [str(engine.__file__), str(project)]
        return engine.main()
    finally:
        sys.argv = original


def smoke(runtime, project):
    doctor(runtime)
    project.mkdir(parents=True, exist_ok=False)
    source = project / '00_SOURCE/input.mp4'
    source.parent.mkdir()
    work = project / '10_WORK'
    work.mkdir()
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i',
         'testsrc2=size=960x540:rate=24:duration=8', '-f', 'lavfi', '-i',
         'sine=frequency=440:sample_rate=48000:duration=8', '-c:v', 'libx264',
         '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', source])
    save(work / 'cuts.json', {'segments': [{'in': 0, 'out': 3}, {'in': 5, 'out': 8}]})
    words = [{'word': word, 'start': 0.5 + i * 0.55, 'end': 0.95 + i * 0.55}
             for i, word in enumerate('Local editing works without any API keys today'.split())]
    save(work / 'words.json', {'words': words})
    save(work / 'style.json', {'words': {'0': {'w': 'strong', 'c': 'speaker'}}, 'voice_spans': []})
    save(project / 'manifest.json', {
        'title': 'local-smoke', 'pipeline': 'eb-local', 'output': {'name': 'local-smoke.mp4'},
        'stages': {'cut': {'source_video': '00_SOURCE/input.mp4',
                           'source_audio': '00_SOURCE/input.mp4',
                           'spec': '10_WORK/cuts.json', 'snap_silence': False},
                   'reframe': {}, 'captions': {'words': '10_WORK/words.json',
                                              'director': '10_WORK/style.json'},
                   'mix': {'music': None, 'voice_lufs': -16, 'limiter': 0.45}}})
    for name in ['first-render', 'cache-render']:
        with (project / f'{name}.log').open('w') as log:
            run([sys.executable, SCRIPT, '--runtime', runtime, 'render', '--project', project],
                stdout=log, stderr=subprocess.STDOUT)
    output = project / '20_DELIVER/v1/local-smoke.mp4'
    info = json.loads(capture(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                               '-of', 'json', output]))
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    decoded = run(['ffmpeg', '-v', 'error', '-xerror', '-i', output, '-f', 'null', '-'],
                  capture_output=True, text=True)
    frame = project / 'sample.png'
    run(['ffmpeg', '-y', '-v', 'error', '-ss', '1', '-i', output, '-frames:v', '1', frame])
    # Compare the caption stage against its exact pre-caption input at the same frame.
    from PIL import Image, ImageChops, ImageStat
    samples = []
    for stage in ['reframe', 'captions']:
        cached = next((work / 'stages' / stage).glob('*.mp4'))
        image = project / f'{stage}.png'
        run(['ffmpeg', '-y', '-v', 'error', '-ss', '1', '-i', cached, '-frames:v', '1', image])
        with Image.open(image) as opened:
            samples.append(opened.convert('RGB').crop((100, 900, 980, 1600)))
    difference = sum(ImageStat.Stat(ImageChops.difference(*samples)).mean)
    ass = (work / 'captions.ass').read_text()
    checks = {'h264': video['codec_name'] == 'h264', 'aac': audio['codec_name'] == 'aac',
              'vertical_1080': (video['width'], video['height']) == (1080, 1920),
              'six_second_cut': abs(float(info['format']['duration']) - 6) < 0.2,
              'full_decode': not decoded.stderr.strip(),
              'caption_events': 'Dialogue:' in ass, 'visible_caption_difference': difference > 1,
              'four_cache_hits': (project / 'cache-render.log').read_text().count(' HIT') == 4}
    report = {'pass': all(checks.values()), 'checks': checks, 'revision': REVISION,
              'adapter_version': ADAPTER_VERSION, 'caption_pixel_difference': difference,
              'output': str(output), 'services_skipped': SKIPPED,
              'fixture': 'synthetic test pattern, tone, and supplied timed words',
              'not_tested': ['ASR', 'face tracking', 'editorial quality', 'delivery', 'real footage']}
    save(project / 'report.json', report)
    print(json.dumps(report, indent=2))
    if not report['pass']:
        raise RuntimeError('Smoke failed; inspect report.json and render logs')
    status_path = runtime / 'status.json'
    status = json.loads(status_path.read_text()) if status_path.exists() else {}
    status.update(smoke='passed', report=str(project / 'report.json'))
    save(status_path, status)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, default=Path('tmp/vibe-editing'))
    parser.add_argument('command', choices=['setup', 'doctor', 'smoke', 'render'])
    parser.add_argument('--project', type=Path)
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    # Restrict the override to this process and its children; never change the shell or system.
    os.environ['PATH'] = str(runtime / 'bin') + os.pathsep + os.environ.get('PATH', '')
    if args.command == 'setup':
        setup(runtime)
    elif args.command == 'doctor':
        doctor(runtime)
    elif args.command == 'render':
        if not args.project:
            parser.error('render requires --project')
        render(runtime, args.project.resolve())
    else:
        project = args.project or runtime / ('smoke-' + time.strftime('%Y%m%d-%H%M%S'))
        smoke(runtime, project.resolve())


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
