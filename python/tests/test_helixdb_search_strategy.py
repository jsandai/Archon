import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.server.services.search.helixdb_search_strategy import HelixDBSearchStrategy

@pytest.fixture
def mock_helix_client():
    """Fixture for a mocked HelixDB client."""
    mock_client = MagicMock()
    mock_client.query = AsyncMock(return_value=[{"content": "mocked result"}])
    return mock_client

@patch('src.server.services.search.helixdb_search_strategy.get_helix_client')
@pytest.mark.asyncio
async def test_vector_search_documents(mock_get_helix_client, mock_helix_client):
    mock_get_helix_client.return_value = mock_helix_client

    strategy = HelixDBSearchStrategy()

    query = "test query"
    match_count = 5

    results = await strategy.vector_search(query, match_count, table="Document")

    mock_helix_client.query.assert_called_once_with(
        "searchDocument",
        {"query": query, "k": match_count},
    )

    assert results == [{"content": "mocked result"}]

@patch('src.server.services.search.helixdb_search_strategy.get_helix_client')
@pytest.mark.asyncio
async def test_vector_search_code_examples(mock_get_helix_client, mock_helix_client):
    mock_get_helix_client.return_value = mock_helix_client

    strategy = HelixDBSearchStrategy()

    query = "test code query"
    match_count = 3

    results = await strategy.vector_search(query, match_count, table="CodeExample")

    mock_helix_client.query.assert_called_once_with(
        "searchCodeExample",
        {"query": query, "k": match_count},
    )

    assert results == [{"content": "mocked result"}]
