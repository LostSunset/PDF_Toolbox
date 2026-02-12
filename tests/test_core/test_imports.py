"""Smoke tests: verify all modules can be imported."""

import importlib

import pytest

CORE_MODULES = [
    "pdf_toolbox",
    "pdf_toolbox.core.utils",
    "pdf_toolbox.core.unlock",
    "pdf_toolbox.core.convert",
    "pdf_toolbox.core.protect",
    "pdf_toolbox.core.merge",
    "pdf_toolbox.core.split",
    "pdf_toolbox.core.rotate",
    "pdf_toolbox.core.watermark",
    "pdf_toolbox.core.compress",
    "pdf_toolbox.core.reorder",
]


@pytest.mark.parametrize("module_name", CORE_MODULES)
def test_import_core_module(module_name: str) -> None:
    mod = importlib.import_module(module_name)
    assert mod is not None
