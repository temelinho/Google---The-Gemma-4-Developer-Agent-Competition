"""Compile with the official compiler, exercise package guards, build reproducibly.

Run with validator-env/Scripts/python.exe validate_and_package.py.
No model inference is performed: tool functions are inert signature-compatible
fixtures and the model registry maps the declared model to its own alias.
"""
from __future__ import annotations

import asyncio
import hashlib
import importlib.metadata
import json
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import zipfile

import yaml
from adk_submission import (
    GenerationConstraints, ModelRegistry, NumericRange, SubmissionLimits,
    ToolRegistry, compile_submission, discover_declared_models,
    discover_skills, validate_directory,
)
from adk_submission.schema import SandboxedAgentConfig
from adk_submission.yaml_loader import load_yaml
from google.adk.skills import load_skill_from_dir

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'submission'
MODEL = 'gemma-4-31b-it-qat-w4a16-ct'
ALLOWED = frozenset({'.yaml', '.yml', '.md', '.txt', '.py', '.json', '.safetensors'})
LIMITS = SubmissionLimits(max_total_size_bytes=3 * 1024**3, allowed_file_extensions=ALLOWED)


def run_command(command: str) -> str:
    return 'inert validation fixture'


def read_file(filepath: str, start_line: int | None = None, end_line: int | None = None) -> str:
    return 'inert validation fixture'


def edit_file(filepath: str, old_string: str, new_string: str, allow_multiple: bool = False) -> str:
    return 'inert validation fixture'


def write_file(filepath: str, content: str) -> str:
    return 'inert validation fixture'


def get_status() -> str:
    return 'inert validation fixture'


def submit_patch() -> str:
    return 'inert validation fixture'


def get_code_neighbors(node: str, edge_type: str | None = None, max_neighbors: int = 50) -> str:
    return 'inert validation fixture'


def search_similar_code(query: str, k: int = 10) -> str:
    return 'inert validation fixture'


def get_code_subgraph(nodes: list[str]) -> str:
    return 'inert validation fixture'


FIXTURES = [run_command, read_file, edit_file, write_file, get_status,
            submit_patch, get_code_neighbors, search_similar_code, get_code_subgraph]


def check_archive(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        names = [i.filename for i in archive.infolist()]
        if names.count('agent.yaml') != 1:
            raise ValueError('Exactly one root agent.yaml is required')
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive members')
        if archive.testzip() is not None:
            raise ValueError('Corrupt archive member')
        if sum(i.file_size for i in archive.infolist()) >= 3 * 1024**3:
            raise ValueError('Unpacked archive reaches size limit')
        for info in archive.infolist():
            p = PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in info.filename or ':' in info.filename:
                raise ValueError('Unsafe archive path')
            if p.suffix not in ALLOWED or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Disallowed archive member')
            archive.read(info).decode('utf-8')  # This release deliberately has no weights.


def guard_regressions() -> list[str]:
    cases = {
        'nested_root': {'submission/agent.yaml': 'name: bad'},
        'traversal': {'agent.yaml': 'name: bad', '../escape.md': 'bad'},
        'binary_extension': {'agent.yaml': 'name: bad', 'weights.bin': 'bad'},
    }
    passed = []
    with tempfile.TemporaryDirectory(prefix='gemma_archive_checks_') as tmp:
        for name, entries in cases.items():
            path = Path(tmp) / (name + '.zip')
            with zipfile.ZipFile(path, 'w') as archive:
                for filename, content in entries.items():
                    archive.writestr(filename, content)
            try:
                check_archive(path)
            except ValueError:
                passed.append(name)
            else:
                raise AssertionError('Guard failed: ' + name)
    return passed


def main() -> None:
    view = validate_directory(ROOT, limits=LIMITS)
    raw = load_yaml(view.config_path, ROOT, limits=LIMITS)
    config = SandboxedAgentConfig.model_validate(raw).root
    declared = discover_declared_models(ROOT)
    assert declared == {MODEL}, declared
    assert config.model == MODEL
    # Catch ADK template placeholders that could require absent session state.
    assert not re.search(r'\{[^{}]+\}', config.instruction)
    generation = config.generate_content_config.model_dump(exclude_none=True)
    assert generation['max_output_tokens'] <= 32768
    assert generation['thinking_config']['thinking_budget'] <= 32768
    eval_config = yaml.safe_load((ROOT / 'eval_config.yaml').read_text(encoding='utf-8'))['evaluation']
    assert set(eval_config) == {'timeout_seconds', 'max_tool_calls', 'max_time_minutes', 'max_turns'}
    assert eval_config['max_time_minutes'] * 120 < 600
    assert 0 < eval_config['timeout_seconds'] < eval_config['max_time_minutes'] * 60

    tools = ToolRegistry()
    for fn in FIXTURES:
        tools.register(fn.__name__, fn)
    models = ModelRegistry()
    models.register(MODEL, MODEL)
    agent = compile_submission(ROOT, tool_registry=tools, model_registry=models, limits=LIMITS)
    assert agent.name == config.name
    assert agent.model == MODEL
    assert len(agent.tools) == len(FIXTURES) + 1  # One ADK SkillToolset.
    skill = load_skill_from_dir(ROOT / 'skills/python-repair')
    assert skill.frontmatter.name == 'python-repair'
    skill_manifest = discover_skills(ROOT, limits=LIMITS)

    # Build the exact tool declarations ADK will expose, without running an LLM.
    from google.adk.tools.function_tool import FunctionTool
    tool_declarations = []
    for fn in FIXTURES:
        decl = FunctionTool(fn)._get_declaration()
        assert decl.name == fn.__name__
        tool_declarations.append(decl.model_dump(exclude_none=True))

    toolset = agent.tools[-1]
    exposed_skill_tools = asyncio.run(toolset.get_tools())
    skill_tool_names = [tool.name for tool in exposed_skill_tools]
    assert 'load_skill' in skill_tool_names
    assert 'load_skill_resource' in skill_tool_names

    archive_path = BASE / 'submission.zip'
    members = []
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file():
                continue
            assert not path.is_symlink()
            relative = path.relative_to(ROOT).as_posix()
            content = path.read_bytes()
            info = zipfile.ZipInfo(relative, date_time=(2026, 10, 29, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, content)
            members.append({'path': relative, 'bytes': len(content),
                            'sha256': hashlib.sha256(content).hexdigest()})
    check_archive(archive_path)
    # Validate the actual extracted upload, rather than only the source folder.
    with tempfile.TemporaryDirectory(prefix='gemma_upload_check_') as tmp:
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(tmp)
        extracted_agent = compile_submission(tmp, tool_registry=tools, model_registry=models, limits=LIMITS)
        assert extracted_agent.instruction == agent.instruction

    report = {
        'compiler': importlib.metadata.version('adk-submission'),
        'google_adk': importlib.metadata.version('google-adk'),
        'model': MODEL, 'evaluation': eval_config,
        'archive_sha256': hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        'archive_bytes': archive_path.stat().st_size,
        'unpacked_bytes': sum(m['bytes'] for m in members),
        'files': members, 'workspace_tool_names': [fn.__name__ for fn in FIXTURES],
        'skill_tool_names': skill_tool_names, 'negative_archive_checks': guard_regressions(),
        'directory_validation': 'passed', 'official_compilation': 'passed',
        'extracted_archive_compilation': 'passed',
        'live_model_inference': 'not_run_no_local_cuda',
        'resolution_rate': None, 'leaderboard_score': None,
    }
    (BASE / 'validation_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (BASE / 'tool_declarations.json').write_text(json.dumps(tool_declarations, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
