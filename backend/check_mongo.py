"""
Quick test to check MongoDB connection.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def test_mongo_connection():
    """Test if MongoDB is accessible."""
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth.
        await client.admin.command('ismaster')
        print("✅ MongoDB is running and accessible!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n📋 To fix this:")
        print("1. Install MongoDB Community Edition from: https://www.mongodb.com/try/download/community")
        print("2. Start MongoDB service:")
        print("   - Windows: Run 'net start MongoDB' in admin PowerShell")
        print("   - Or start MongoDB Compass and ensure server is running")
        print("3. Verify MongoDB is running on localhost:27017")
        return False


if __name__ == "__main__":
    asyncio.run(test_mongo_connection())
