"""Tests for core split module."""

from pdf_toolbox.core.split import SplitMode, parse_page_ranges


class TestParsePageRanges:
    def test_single_page(self) -> None:
        result = parse_page_ranges("3", total_pages=10)
        assert result == [(2, 2)]

    def test_range(self) -> None:
        result = parse_page_ranges("1-3", total_pages=10)
        assert result == [(0, 2)]

    def test_multiple_ranges(self) -> None:
        result = parse_page_ranges("1-3, 5, 7-9", total_pages=10)
        assert len(result) == 3
        assert result[0] == (0, 2)
        assert result[1] == (4, 4)
        assert result[2] == (6, 8)


class TestSplitMode:
    def test_modes_exist(self) -> None:
        assert SplitMode.BY_RANGE is not None
        assert SplitMode.EVERY_N_PAGES is not None
        assert SplitMode.EXTRACT_PAGES is not None
