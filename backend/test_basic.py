"""
Simple test to check if we can import and run a basic test.
"""
import asyncio
import sys
sys.path.insert(0, '.')

async def main():
    try:
        print("Testing imports...")
        from app.main import app
        print("✅ app imported")
        
        from app.models.user import User
        from app.models.sweet import Sweet
        print("✅ models imported")
        
        from beanie import init_beanie
        from motor.motor_asyncio import AsyncIOMotorClient
        print("✅ database imports OK")
        
        # Try to initialize database
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        database = client["sweet_shop_test"]
        
        await init_beanie(
            database=database,
            document_models=[User, Sweet]
        )
        print("✅ Beanie initialized")
        
        # Try to create a user
        from app.utils.password import hash_password
        user = User(
            email="test@example.com",
            password_hash=hash_password("password123"),
            name="Test User"
        )
        await user.insert()
        print(f"✅ User created: {user.email}")
        
        # Clean up
        await user.delete()
        client.close()
        print("✅ All basic operations work!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
