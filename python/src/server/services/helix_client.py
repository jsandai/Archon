"""
HelixDB Client Manager Service

Manages HelixDB client connections.
"""

import os
from helix import Client
from ..config.logfire_config import search_logger

def get_helix_client() -> Client:
    """
    Get a HelixDB client instance.

    Returns:
        Client: HelixDB client instance (helix.Client)
    """
    # The host of the helixdb service is `helixdb` as defined in docker-compose.yml
    # The default port is 6969
    try:
        # For Docker container connections, we need to use the service name as hostname
        # Since we're connecting to another container, local=False and use api_endpoint
        client = Client(
            local=False, 
            api_endpoint="http://helixdb:6969",
            verbose=True
        )
        search_logger.info("HelixDB client initialized")
        return client
    except Exception as e:
        search_logger.error(f"Failed to create HelixDB client: {e}")
        raise
