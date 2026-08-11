import hashlib
import tempfile
import unittest
from pathlib import Path

from src.file_checksum import calculate_checksum, main, verify_checksum


class FileChecksumTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary_directory.name) / "sample.bin"
        self.content = b"Git practice\n\x00\xff"
        self.path.write_bytes(self.content)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_calculate_sha256(self) -> None:
        expected = hashlib.sha256(self.content).hexdigest()
        self.assertEqual(calculate_checksum(self.path), expected)

    def test_verify_checksum_is_case_insensitive(self) -> None:
        expected = hashlib.md5(self.content).hexdigest().upper()
        self.assertTrue(verify_checksum(self.path, expected, "md5"))

    def test_rejects_unsupported_algorithm(self) -> None:
        with self.assertRaises(ValueError):
            calculate_checksum(self.path, "crc32")

    def test_cli_returns_failure_for_wrong_checksum(self) -> None:
        self.assertEqual(main([str(self.path), "--verify", "0" * 64]), 1)


if __name__ == "__main__":
    unittest.main()
