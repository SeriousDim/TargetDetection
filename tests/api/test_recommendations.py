import asyncio
import io
import sys
from pathlib import Path

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from PIL import Image

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.main import app


@pytest.mark.asyncio
async def test_post_recommendations():
    # Создание тестового изображения
    image = Image.new("RGB", (100, 100), "white")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # Создание ASGITransport
    transport = ASGITransport(app=app)

    # Выполнение POST-запроса
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("test.png", img_byte_arr, "image/png")}
        response = await ac.post("/recommendations", files=files)

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert "recommendation" in response_json
    assert "target_name" in response_json
    assert "image" in response_json


@pytest.mark.asyncio
async def test_load_post_recommendations():
    """
    Нагрузочный тест
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:

        async def make_request():
            # Создание тестового изображения
            image = Image.new("RGB", (100, 100), "white")
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)

            # Выполнение POST-запроса
            files = {"file": ("test.png", img_byte_arr, "image/png")}
            response = await client.post("/recommendations", files=files)

            assert response.status_code == 200
            response_json = response.json()
            assert "recommendation" in response_json
            assert "target_name" in response_json
            assert "image" in response_json

        tasks = [make_request() for _ in range(50)]
        await asyncio.gather(*tasks)
