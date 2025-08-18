"""
HelixDB Client Manager Service

Manages HelixDB client connections.
"""

import os
from helix_py import HelixDB
from ..config.logfire_config import search_logger

def get_helix_client() -> HelixDB:
    """
    Get a HelixDB client instance.

    Returns:
        HelixDB client instance
    """
    # The host of the helixdb service is `helixdb` as defined in docker-compose.yml
    # The default port is 6969
    try:
        client = HelixDB(host="helixdb")
        search_logger.info("HelixDB client initialized")
        return client
    except Exception as e:
        search_logger.error(f"Failed to create HelixDB client: {e}")
        raise
