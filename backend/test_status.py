"""
Quick test to check what status code we get for unauthorized access.
"""
import asyncio
from httpx import AsyncClient, ASGITransport

async def main():
    from app.main import app
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/sweets",
            json={
                "name": "Test",
                "category": "Test",
                "price": 1.0,
                "quantity": 10
            }
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")

if __name__ == "__main__":
    asyncio.run(main())
