"""
HelixDB Search Strategy

Implements vector similarity search using HelixDB.
"""

from typing import Any, List
import asyncio
from ...config.logfire_config import get_logger, safe_span
from ..helix_client import get_helix_client

logger = get_logger(__name__)

class HelixDBSearchStrategy:
    """Strategy for searching documents and code examples in HelixDB."""

    def __init__(self):
        """Initialize with database client"""
        self.helix_client = get_helix_client()

    async def vector_search(
        self,
        query: str,
        match_count: int,
        filter_metadata: dict | None = None, # This is ignored for now.
        table: str = "Document",
    ) -> list[dict[str, Any]]:
        """
        Perform vector similarity search in HelixDB.

        Args:
            query: The search query string.
            match_count: Number of results to return.
            filter_metadata: Optional metadata filters (ignored for now).
            table: The node type to search ('Document' or 'CodeExample').

        Returns:
            List of matching documents with similarity scores.
        """
        with safe_span("helixdb_vector_search", table=table, match_count=match_count) as span:
            try:
                # Assumes that `searchDocument` and `searchCodeExample` queries are defined in HelixDB.
                search_query_name = f"search{table}"

                params = {
                    "query": query,
                    "k": match_count,
                }

                # The helix.Client.query method is synchronous, not async
                # So we need to run it in a thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                results = await loop.run_in_executor(
                    None, 
                    lambda: self.helix_client.query(search_query_name, params)
                )

                span.set_attribute("results_found", len(results))
                return results

            except Exception as e:
                logger.error(f"HelixDB vector search failed: {e}")
                span.set_attribute("error", str(e))
                return []
