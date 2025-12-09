"""Apache Airflow Provider for TwitterAPI.io"""

from __future__ import annotations

from typing import Any

__version__ = "2025.12.10"


def get_provider_info() -> dict[str, Any]:
    """Return provider metadata for Airflow."""
    return {
        "package-name": "airflow-provider-twitterapi",
        "name": "TwitterAPI.io Provider",
        "description": "Apache Airflow provider for TwitterAPI.io",
        "versions": [__version__],
        "hook-class-names": [
            "airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook",
        ],
        "connection-types": [
            {
                "hook-class-name": (
                    "airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook"
                ),
                "connection-type": "twitterapi",
            },
        ],
    }
