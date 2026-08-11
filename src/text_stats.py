"""Count lines, words, and characters in text or text files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Sequence


WORD_PATTERN = re.compile(r"[A-Za-z0-9_]+|[\u3400-\u4dbf\u4e00-\u9fff]")


def analyze_text(text: str) -> Dict[str, int]:
    """Return common text statistics."""
    return {
        "lines": len(text.splitlines()),
        "words": len(WORD_PATTERN.findall(text)),
        "characters": len(text),
        "non_whitespace_characters": sum(not char.isspace() for char in text),
    }


def analyze_file(path: Path, encoding: str = "utf-8") -> Dict[str, int]:
    """Read *path* and return its text statistics."""
    return analyze_text(path.read_text(encoding=encoding))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="统计文本文件的行数、词数和字符数")
    parser.add_argument("path", type=Path, help="要统计的文本文件")
    parser.add_argument("--encoding", default="utf-8", help="文件编码，默认 utf-8")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        stats = analyze_file(args.path, args.encoding)
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
