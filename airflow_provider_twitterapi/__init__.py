"""Apache Airflow Provider for TwitterAPI.io"""

__version__ = "0.1.0"


def get_provider_info():
    """Return provider metadata for Airflow."""
    return {
        "package-name": "apache-airflow-provider-twitterapi",
        "name": "TwitterAPI.io Provider",
        "description": "Apache Airflow provider for TwitterAPI.io",
        "versions": [__version__],
        "hook-class-names": [
            "airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook",
        ],
        "connection-types": [
            {
                "hook-class-name": "airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook",
                "connection-type": "twitterapi",
            },
        ],
    }
