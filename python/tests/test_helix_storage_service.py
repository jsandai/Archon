import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.server.services.storage.helix_storage_service import add_documents_to_helixdb, add_code_examples_to_helixdb
import json

@pytest.fixture
def mock_helix_client():
    """Fixture for a mocked HelixDB client."""
    mock_client = MagicMock()
    mock_client.query = AsyncMock()
    return mock_client

@patch('src.server.services.storage.helix_storage_service.get_helix_client')
@pytest.mark.asyncio
async def test_add_documents_to_helixdb(mock_get_helix_client, mock_helix_client):
    mock_get_helix_client.return_value = mock_helix_client

    urls = ["http://example.com/1"]
    chunk_numbers = [1]
    contents = ["This is a test document."]
    metadatas = [{"source_id": "example"}]

    await add_documents_to_helixdb(urls, chunk_numbers, contents, metadatas)

    mock_helix_client.query.assert_called_once_with(
        "addDocument",
        {
            "url": "http://example.com/1",
            "chunk_number": 1,
            "content": "This is a test document.",
            "metadata": json.dumps({"source_id": "example"}),
            "source_id": "example",
        },
    )

@patch('src.server.services.storage.helix_storage_service.get_helix_client')
@pytest.mark.asyncio
async def test_add_code_examples_to_helixdb(mock_get_helix_client, mock_helix_client):
    mock_get_helix_client.return_value = mock_helix_client

    urls = ["http://example.com/code/1"]
    chunk_numbers = [1]
    code_examples = ["print('hello world')"]
    summaries = ["A simple hello world."]
    metadatas = [{"source_id": "example_code"}]

    await add_code_examples_to_helixdb(urls, chunk_numbers, code_examples, summaries, metadatas)

    mock_helix_client.query.assert_called_once_with(
        "addCodeExample",
        {
            "url": "http://example.com/code/1",
            "chunk_number": 1,
            "content": "print('hello world')",
            "summary": "A simple hello world.",
            "metadata": json.dumps({"source_id": "example_code"}),
            "source_id": "example_code",
        },
    )
