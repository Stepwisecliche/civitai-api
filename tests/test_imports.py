"""Test that all modules in the project directory are importable.

This module discovers all modules in the project and verifies that they can be imported without errors.
"""

import importlib
import os
import pkgutil
import sys

import pytest


def get_project_modules(project_root: str) -> list[str]:
    """Get all module names in the specified project directory.

    Parameters
    ----------
    project_root : str
        The root directory of the project to search for modules.

    Returns
    -------
    list[str]
        A list of module names found in the project directory.

    """
    modules = []
    for _importer, modname, _ispkg in pkgutil.walk_packages(
        path=[project_root], prefix="", onerror=lambda x: None
    ):
        # Only include modules in the project directory
        modules.append(modname)
    return modules


def test_all_project_modules_importable() -> None:
    """Test that all modules in the project directory are importable.

    Raises
    ------
    AssertionError
        If any module fails to import.

    """
    # Assuming the project root is one level above the tests directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, project_root)
    modules = get_project_modules(project_root)
    failed_imports = []
    for modname in modules:
        try:
            importlib.import_module(modname)
        except Exception as e:
            failed_imports.append((modname, str(e)))
    assert not failed_imports, f"Failed to import modules: {failed_imports}"
