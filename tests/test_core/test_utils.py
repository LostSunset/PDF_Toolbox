"""Tests for core utility functions."""

from pathlib import Path

from pdf_toolbox.core.utils import ensure_unique_path, human_readable_size, validate_pdf


class TestEnsureUniquePath:
    def test_unique_path_no_conflict(self, tmp_path: Path) -> None:
        target = tmp_path / "output.pdf"
        result = ensure_unique_path(target)
        assert result == target

    def test_unique_path_with_conflict(self, tmp_path: Path) -> None:
        target = tmp_path / "output.pdf"
        target.touch()
        result = ensure_unique_path(target)
        assert result != target
        assert result.stem.startswith("output")
        assert result.suffix == ".pdf"


class TestValidatePdf:
    def test_valid_pdf(self, tmp_path: Path) -> None:
        pdf = tmp_path / "test.pdf"
        pdf.write_bytes(b"%PDF-1.4 fake content")
        assert validate_pdf(pdf) is True

    def test_invalid_extension(self, tmp_path: Path) -> None:
        txt = tmp_path / "test.txt"
        txt.write_text("not a pdf")
        assert validate_pdf(txt) is False

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        assert validate_pdf(tmp_path / "missing.pdf") is False


class TestHumanReadableSize:
    def test_bytes(self) -> None:
        result = human_readable_size(500)
        assert "500" in result and "B" in result

    def test_kilobytes(self) -> None:
        result = human_readable_size(1536)
        assert "KB" in result

    def test_megabytes(self) -> None:
        result = human_readable_size(2 * 1024 * 1024)
        assert "MB" in result
