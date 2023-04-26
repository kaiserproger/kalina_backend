import pytest_asyncio
import aiohttp


@pytest_asyncio.fixture
async def authorize() -> str:
    phone = "+79039033333"
    async with aiohttp.ClientSession("http://localhost:8080/") as client:
        response = await client.post("/authorize", data={
            "phone": phone
        })
        assert response.status == 200
        code: int = (await response.json())["code"]
        response = await client.post("/authorize/confirm", data={
            "phone": phone,
            "code": code
        })
        if response.status == 200:
            return (await response.json())["token"]
        response = await client.post("/authorize/finish", data={
            "name": "Roman",
            "phone": phone,
        })
        assert response.status == 200
        return (await response.json())["token"]
