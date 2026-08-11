"""Calculate and verify file checksums with Python's standard library."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Sequence


SUPPORTED_ALGORITHMS = ("md5", "sha1", "sha256", "sha512")


def calculate_checksum(
    path: Path,
    algorithm: str = "sha256",
    chunk_size: int = 64 * 1024,
) -> str:
    """Return the hexadecimal checksum for *path*.

    The file is read in chunks so that large files do not need to be loaded into
    memory all at once.
    """
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"不支持的算法: {algorithm}")
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    digest = hashlib.new(algorithm)
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def verify_checksum(path: Path, expected: str, algorithm: str = "sha256") -> bool:
    """Return whether *path* matches an expected hexadecimal checksum."""
    return calculate_checksum(path, algorithm) == expected.strip().lower()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="计算或验证文件哈希值")
    parser.add_argument("path", type=Path, help="要处理的文件")
    parser.add_argument(
        "--algorithm",
        choices=SUPPORTED_ALGORITHMS,
        default="sha256",
        help="哈希算法，默认 sha256",
    )
    parser.add_argument("--verify", metavar="HASH", help="验证文件是否匹配指定哈希值")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        checksum = calculate_checksum(args.path, args.algorithm)
    except (OSError, ValueError) as error:
        print(f"错误: {error}")
        return 2

    if args.verify is None:
        print(checksum)
        return 0

    if checksum == args.verify.strip().lower():
        print("校验成功")
        return 0
    print("校验失败")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
