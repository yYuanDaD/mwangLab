"""mwangLab tool package.

Package-level names are resolved lazily so that importing a lightweight module
(for example ``tools.analysis_policy`` or ``tools.native``) does not require
GEOparse, LangChain, or the other optional heavy dependencies.
"""

from importlib import import_module

_LAZY_EXPORTS = {
    "download_geo_data": "geo_tools",
    "extract_sea_cdm_conditions": "seacdm_tools",
}

__all__ = list(_LAZY_EXPORTS)


def __getattr__(name):
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(f".{module_name}", __name__), name)
