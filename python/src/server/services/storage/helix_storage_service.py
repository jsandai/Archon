"""
HelixDB Storage Service

Handles storage of documents and code examples in HelixDB.
"""

from helix_py import HelixDB
from ...config.logfire_config import search_logger
from ..helix_client import get_helix_client
from typing import Any, List
import asyncio
import json

async def add_documents_to_helixdb(
    urls: List[str],
    chunk_numbers: List[int],
    contents: List[str],
    metadatas: List[dict[str, Any]],
    batch_size: int = 50,
):
    """
    Add documents to HelixDB.
    """
    client = get_helix_client()
    search_logger.info(f"Adding {len(contents)} documents to HelixDB.")

    for i in range(0, len(contents), batch_size):
        # This is not efficient as it sends one request per document.
        # A batch insert query would be better.
        # For now, this is a simple implementation.
        for j in range(i, min(i + batch_size, len(contents))):
            try:
                await client.query(
                    "addDocument",
                    {
                        "url": urls[j],
                        "chunk_number": chunk_numbers[j],
                        "content": contents[j],
                        "metadata": json.dumps(metadatas[j]),
                        "source_id": metadatas[j].get("source_id", ""),
                    },
                )
            except Exception as e:
                search_logger.error(f"Failed to add document to HelixDB: {e}")

async def add_code_examples_to_helixdb(
    urls: List[str],
    chunk_numbers: List[int],
    code_examples: List[str],
    summaries: List[str],
    metadatas: List[dict[str, Any]],
    batch_size: int = 20,
):
    """
    Add code examples to HelixDB.
    """
    client = get_helix_client()
    search_logger.info(f"Adding {len(code_examples)} code examples to HelixDB.")

    for i in range(0, len(code_examples), batch_size):
        for j in range(i, min(i + batch_size, len(code_examples))):
            try:
                await client.query(
                    "addCodeExample",
                    {
                        "url": urls[j],
                        "chunk_number": chunk_numbers[j],
                        "content": code_examples[j],
                        "summary": summaries[j],
                        "metadata": json.dumps(metadatas[j]),
                        "source_id": metadatas[j].get("source_id", ""),
                    },
                )
            except Exception as e:
                search_logger.error(f"Failed to add code example to HelixDB: {e}")
