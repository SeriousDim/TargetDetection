import asyncio
import sys
from pathlib import Path

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.main import app


@pytest.mark.asyncio
async def test_get_index():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "<title>" in response.text


@pytest.mark.asyncio
async def test_load_get_index():
    """
    Нагрузочный тест
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:

        async def make_request():
            response = await client.get("/")
            assert response.status_code == 200
            assert "<title>" in response.text

        tasks = [make_request() for _ in range(100)]
        await asyncio.gather(*tasks)
