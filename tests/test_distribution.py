"""规范及 GitHub／离线分发的可移植性检查，不运行业务工程。"""

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_skill", ROOT / "scripts/package_skill.py")
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)
RULE = r"(?:GOV|ARC|JAVA|VUE|API|DATA|SEC|TEST|DEV|REL|OPS)-\d{3}"


def check_markdown(path: Path, root: Path) -> tuple[int, int]:
    content = path.read_text(encoding="utf-8", errors="strict")
    assert "\ufffd" not in content, f"{path}: 存在替换字符"
    fence = None
    body = []
    columns = None
    tables = 0
    for number, line in enumerate(content.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, suffix = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not suffix.strip():
                fence = None
            continue
        if fence is not None:
            continue
        body.append(line)
        if line.strip().startswith("|"):
            # 转义管道不属于分隔符；现有表格不使用内嵌多行 HTML。
            count = len(re.split(r"(?<!\\)\|", line.strip())) - 2
            if columns is None:
                columns = count
                tables += 1
            assert count == columns, f"{path}:{number}: 表格列数不一致"
        else:
            columns = None
    assert fence is None, f"{path}: 代码围栏未闭合"
    links = 0
    for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", "\n".join(body)):
        target = target.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("#"):
            continue
        resolved = (path.parent / unquote(parsed.path)).resolve()
        assert resolved.is_relative_to(root.resolve()), f"{path}: 链接逃逸 {target}"
        assert resolved.exists(), f"{path}: 失效链接 {target}"
        links += 1
    return tables, links


class RepositoryTests(unittest.TestCase):
    def test_markdown_and_rule_references(self):
        paths = sorted(
            p for p in ROOT.rglob("*.md")
            if not {".git", "dist", "__pycache__"}.intersection(p.relative_to(ROOT).parts)
        )
        rules = []
        for path in (ROOT / "docs").glob("*.md"):
            rules.extend(re.findall(rf"^\| ({RULE}) \|", path.read_text("utf-8"), re.MULTILINE))
        self.assertEqual(len(rules), len(set(rules)), "规则定义重复")
        self.assertEqual(len(rules), 102, "本次不应修改规范规则数量")
        definitions = set(rules)
        counts = [0, 0]
        for path in paths:
            result = check_markdown(path, ROOT)
            counts = [a + b for a, b in zip(counts, result)]
            content = path.read_text("utf-8")
            self.assertFalse(set(re.findall(RULE, content)) - definitions, str(path))
            for prefix, first, last_prefix, last in re.findall(
                r"([A-Z]+)-(\d{3})[～~–](?:([A-Z]+)-)?(\d{3})", content
            ):
                self.assertIn(last_prefix, ("", prefix), str(path))
                self.assertLessEqual(int(first), int(last), str(path))
                for n in range(int(first), int(last) + 1):
                    self.assertIn(f"{prefix}-{n:03}", definitions, str(path))
        checklists = "\n".join(p.read_text("utf-8") for p in (ROOT / "checklists").glob("*.md"))
        self.assertFalse(definitions - set(re.findall(RULE, checklists)))
        print(f"Markdown: {len(paths)} files, {counts[0]} tables, {counts[1]} local links; rules: 102")


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="standard-distribution-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def test_archive_integrity_and_relocated_links(self):
        output = PACKAGE.package(ROOT, self.work / "portable.zip")
        with zipfile.ZipFile(output) as archive:
            self.assertIsNone(archive.testzip())
            archive.extractall(self.work / "relocated")
        skill = self.work / "relocated/java-vue-standards"
        snapshot = skill / "references/standard"
        manifest = json.loads((snapshot / "SNAPSHOT.json").read_text("utf-8"))
        actual = {
            p.relative_to(snapshot).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in snapshot.rglob("*") if p.is_file() and p.name != "SNAPSHOT.json"
        }
        self.assertEqual(manifest["files"], actual)
        snapshot_id = hashlib.sha256(
            json.dumps(actual, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(manifest["snapshot_id"], snapshot_id)
        self.assertEqual(manifest["standard_version"], "1.0.0")
        self.assertFalse((snapshot / "AGENTS.md").exists())
        for directory in PACKAGE.CONTENT_DIRS:
            for source in (ROOT / directory).rglob("*"):
                if source.is_file():
                    copied = snapshot / source.relative_to(ROOT)
                    self.assertEqual(source.read_bytes(), copied.read_bytes(), str(source))
        for path in skill.rglob("*.md"):
            check_markdown(path, skill)

    def test_existing_output_is_preserved(self):
        output = self.work / "existing.zip"
        output.write_bytes(b"preserve existing content")
        with self.assertRaises(FileExistsError):
            PACKAGE.package(ROOT, output)
        self.assertEqual(output.read_bytes(), b"preserve existing content")

    def test_repeated_packaging_is_deterministic(self):
        first = PACKAGE.package(ROOT, self.work / "first.zip")
        second = PACKAGE.package(ROOT, self.work / "second.zip")
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_missing_source_creates_no_output(self):
        output = self.work / "missing.zip"
        with self.assertRaises(FileNotFoundError):
            PACKAGE.package(self.work / "missing-source", output)
        self.assertFalse(output.exists())

    def test_rejects_output_inside_source_documents(self):
        output = ROOT / "templates/do-not-create-test.zip"
        with self.assertRaises(ValueError):
            PACKAGE.package(ROOT, output)
        self.assertFalse(output.exists())

    def test_github_root_install_layout_without_git(self):
        # 模拟 GitHub 下载后仅保留仓库文件，并安装到与源码无关的目录。
        installed = self.work / "installed/java-vue-standards"
        installed.mkdir(parents=True)
        for directory in (*PACKAGE.CONTENT_DIRS, "scripts", "agents", "tests"):
            shutil.copytree(ROOT / directory, installed / directory, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("README.md", "AGENTS.md", "SKILL.md", "CHANGELOG.md", "VALIDATION.md"):
            shutil.copy2(ROOT / name, installed / name)
        payload = PACKAGE.build_payload(installed)
        prefix = "java-vue-standards/references/standard/"
        manifest = json.loads(payload[prefix + "SNAPSHOT.json"])
        self.assertIsNone(manifest["source_git_commit"])
        self.assertIsNone(manifest["source_git_dirty"])
        self.assertIn(prefix + "templates/16-project-agents.md", payload)
        for path in installed.rglob("*.md"):
            check_markdown(path, installed)


if __name__ == "__main__":
    unittest.main()
