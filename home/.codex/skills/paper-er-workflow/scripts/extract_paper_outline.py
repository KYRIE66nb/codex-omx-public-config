#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

try:
    from docx import Document  # type: ignore
except Exception:  # pragma: no cover
    Document = None  # type: ignore


CHAPTER_PATTERNS = [
    re.compile(r"^第\s*[一二三四五六七八九十0-9]+\s*章\s*.+"),
    re.compile(r"^[一二三四五六七八九十]+、\S+"),
    re.compile(r"^[1-9]\s+\S+"),
]
SECTION_PATTERNS = [
    re.compile(r"^\d+\.\d+\s*\S+"),
    re.compile(r"^（[一二三四五六七八九十]+）\S+"),
]
ER_FIG_PATTERN = re.compile(r"^图\s*\d+[\-－]\d+\s*.*(ER|E-R)", re.I)
ER_KEYWORDS = ("er图", "e-r", "数据库表", "表结构", "概念结构", "逻辑结构", "实体关系")


def clean_line(text: str) -> str:
    text = text.replace("\u3000", " ").strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\t\s*\d+\s*$", "", text)
    text = re.sub(r"\s+\d+\s*$", "", text)
    return text.strip()


def looks_like_heading(text: str) -> bool:
    if len(text) > 50:
        return False
    if any(mark in text for mark in ("。", "；", "PAGEREF", "HYPERLINK", "毕业设计（论文）")):
        return False
    return True


def extract_lines(file_path: Path) -> list[str]:
    if file_path.suffix.lower() == ".docx":
        if Document is None:
            raise RuntimeError("python-docx 未安装，无法解析 .docx")
        doc = Document(file_path)
        return [clean_line(p.text) for p in doc.paragraphs if clean_line(p.text)]
    if file_path.suffix.lower() == ".doc":
        text = subprocess.check_output(
            ["textutil", "-convert", "txt", "-stdout", str(file_path)]
        ).decode("utf-8", "ignore")
        return [clean_line(line) for line in text.splitlines() if clean_line(line)]
    return []


def summarize_file(file_path: Path) -> dict[str, list[str]]:
    lines = extract_lines(file_path)
    chapters: list[str] = []
    sections: list[str] = []
    er_figs: list[str] = []
    er_lines: list[str] = []

    for line in lines:
        lower = line.lower()
        if any(keyword in lower for keyword in ER_KEYWORDS):
            if line not in er_lines and len(er_lines) < 12:
                er_lines.append(line)
        if ER_FIG_PATTERN.match(line) and line not in er_figs:
            er_figs.append(line)
        if not looks_like_heading(line):
            continue
        if any(pattern.match(line) for pattern in CHAPTER_PATTERNS):
            if line not in chapters:
                chapters.append(line)
        elif any(pattern.match(line) for pattern in SECTION_PATTERNS):
            if line not in sections and len(sections) < 12:
                sections.append(line)

    return {
        "chapters": chapters[:12],
        "sections": sections[:12],
        "er_figs": er_figs[:6],
        "er_lines": er_lines[:12],
    }


def write_markdown(result: dict[str, dict[str, list[str]]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        file.write("# 论文目录与ER线索自动提取\n\n")
        for filename, data in result.items():
            file.write(f"## {filename}\n")
            file.write("### 章节（提取）\n")
            for item in data["chapters"]:
                file.write(f"- {item}\n")
            file.write("### 二级小节（部分）\n")
            for item in data["sections"]:
                file.write(f"- {item}\n")
            file.write("### ER图标题\n")
            if data["er_figs"]:
                for item in data["er_figs"]:
                    file.write(f"- {item}\n")
            else:
                file.write("- （未直接提取到图题）\n")
            file.write("### ER/数据库相关句\n")
            for item in data["er_lines"]:
                file.write(f"- {item}\n")
            file.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="提取论文目录结构与ER线索。")
    parser.add_argument("input_dir", type=Path, help="论文目录路径")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("paper_outline_summary.md"),
        help="输出 Markdown 路径",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        raise SystemExit(f"输入目录不存在: {args.input_dir}")

    files = sorted(
        path
        for path in args.input_dir.iterdir()
        if path.suffix.lower() in {".docx", ".doc"} and path.is_file()
    )
    if not files:
        raise SystemExit("未找到 .docx/.doc 文件")

    summary = {file_path.name: summarize_file(file_path) for file_path in files}
    write_markdown(summary, args.output)
    print(f"已生成: {args.output}")


if __name__ == "__main__":
    main()
