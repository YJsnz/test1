import tempfile
import unittest
from pathlib import Path

from src.text_stats import analyze_file, analyze_text


class AnalyzeTextTests(unittest.TestCase):
    def test_mixed_chinese_and_english_text(self) -> None:
        stats = analyze_text("Hello Git\n你好 2026")
        self.assertEqual(stats, {
            "lines": 2,
            "words": 5,
            "characters": 17,
            "non_whitespace_characters": 14,
        })

    def test_empty_text(self) -> None:
        self.assertEqual(analyze_text(""), {
            "lines": 0,
            "words": 0,
            "characters": 0,
            "non_whitespace_characters": 0,
        })

    def test_analyze_utf8_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("Git practice", encoding="utf-8")
            self.assertEqual(analyze_file(path)["words"], 2)


if __name__ == "__main__":
    unittest.main()
