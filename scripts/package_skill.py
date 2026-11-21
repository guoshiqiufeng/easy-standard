#!/usr/bin/env python3
"""将 skill 和规范快照打包为可移植 ZIP；仅使用 Python 标准库。"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile


SKILL_NAME = "java-vue-standards"
SOURCE_ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = ("docs", "templates", "checklists", "examples")


def read_regular_file(path: Path, root: Path) -> bytes:
    """不跟随符号链接或目录连接，不读取来源目录以外的内容。"""
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"文件超出来源目录：{path}")
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink() or part.resolve() != part.absolute():
            raise ValueError(f"不打包符号链接或目录连接：{part}")
    return path.read_bytes()


def git_state(root: Path) -> dict:
    def git(*args):
        return subprocess.check_output(
            ["git", "-C", str(root), *args], stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()

    try:
        if Path(git("rev-parse", "--show-toplevel")).resolve() != root.resolve():
            raise ValueError("来源不是 Git 仓库根目录")
        return {
            "source_git_commit": git("rev-parse", "HEAD"),
            "source_git_dirty": bool(git("status", "--porcelain", "--untracked-files=all")),
        }
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError):
        return {"source_git_commit": None, "source_git_dirty": None}


def build_payload(root: Path) -> dict[str, bytes]:
    root = root.resolve()
    source_readme = read_regular_file(root / "README.md", root).decode("utf-8")
    version = re.search(r"^版本：([^\s·]+)", source_readme, re.MULTILINE)
    if not version:
        raise ValueError("README.md 缺少规范版本")

    snapshot = {}
    for directory in CONTENT_DIRS:
        base = root / directory
        if not base.is_dir():
            raise ValueError(f"缺少规范目录：{directory}")
        for path in sorted(base.rglob("*")):
            if path.is_symlink() or path.resolve() != path.absolute():
                raise ValueError(f"不打包符号链接或目录连接：{path}")
            if path.is_file() and (
                path.suffix.lower() in {".md", ".yaml", ".yml"}
                or path.name == ".env.example"
            ):
                snapshot[path.relative_to(root).as_posix()] = read_regular_file(path, root)

    for required in (
        "docs/00-governance.md",
        "templates/01-project-baseline.md",
        "templates/16-project-agents.md",
        "checklists/02-merge.md",
    ):
        if required not in snapshot:
            raise ValueError(f"缺少接入必需资料：{required}")

    snapshot["CHANGELOG.md"] = read_regular_file(root / "CHANGELOG.md", root)
    index = [
        "# Java＋Vue 3 团队项目规范快照",
        "",
        f"版本：{version.group(1)}。正文、模板、清单与示例来自打包时的来源工作区。",
        "此首页为便携包生成的导航；来源与逐文件摘要见 [SNAPSHOT.json](SNAPSHOT.json)。",
        "未提交状态或未知 Git 状态均不代表已发布或已评审。摘要清单用于完整性核对，不是审批或签名。",
        "",
        "先阅读[总则与治理](docs/00-governance.md)。强制、推荐、可选等级按正文；示例不代表项目承诺。",
        "业务项目使用[项目 AGENTS.md 模板](templates/16-project-agents.md)，按实际目录和基线填写。",
        "变更历史见 [CHANGELOG.md](CHANGELOG.md)。",
        "",
    ]
    for directory in CONTENT_DIRS:
        index.extend([f"## {directory}", ""])
        for name in sorted(snapshot):
            if name.startswith(directory + "/") and name.endswith(".md"):
                heading = next(
                    (line[2:] for line in snapshot[name].decode("utf-8").splitlines()
                     if line.startswith("# ")),
                    name,
                )
                index.append(f"- [{heading}]({name})")
        index.append("")
    snapshot["README.md"] = "\n".join(index).encode("utf-8")
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(snapshot.items())}
    snapshot_id = hashlib.sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    manifest = {
        "schema_version": 1,
        "standard_version": version.group(1),
        **git_state(root),
        "snapshot_id": snapshot_id,
        "generated_files": ["README.md"],
        "files": hashes,
    }
    snapshot["SNAPSHOT.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    payload = {}
    for name in ("SKILL.md", "agents/openai.yaml"):
        data = read_regular_file(root / name, root)
        if name == "SKILL.md":
            # 便携包没有仓库根目录资料；入口中的链接统一指向随包快照。
            content = data.decode("utf-8")
            for target in (
                "README.md", "docs/00-governance.md", "templates/16-project-agents.md",
                "checklists/02-merge.md",
            ):
                content = content.replace(f"]({target})", f"](references/standard/{target})")
            # 打包脚本仅供根目录安装方式使用，包内保留脚本便于引用解析。
            data = content.encode("utf-8")
        payload[f"{SKILL_NAME}/{name}"] = data
    payload[f"{SKILL_NAME}/scripts/package_skill.py"] = read_regular_file(
        root / "scripts/package_skill.py", root
    )
    for name, data in snapshot.items():
        payload[f"{SKILL_NAME}/references/standard/{name}"] = data
    return payload


def package(root: Path, output: Path) -> Path:
    """先收集并验证输入，独占创建输出；不覆盖已有压缩包。"""
    root = root.resolve()
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"输出已存在，请选择新文件名：{output}")
    # 避免把生成物写进规范正文或 skill 源目录。
    if any(output.resolve().is_relative_to(root / d) for d in (*CONTENT_DIRS, "skills")):
        raise ValueError("输出不能位于规范资料或 skill 源目录内")
    payload = build_payload(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return output.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path("dist") / f"{SKILL_NAME}.zip",
        help="输出 ZIP 路径；已存在时拒绝覆盖",
    )
    args = parser.parse_args()
    try:
        result = package(SOURCE_ROOT, args.output)
    except (OSError, ValueError, UnicodeError) as error:
        parser.exit(1, f"打包失败：{error}\n")
    print(f"已生成：{result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
