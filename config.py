import os
from dotenv import load_dotenv
from groq import Groq
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

load_dotenv()

class Config:
    GROQ_API_KEY = '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'
    MONGODB_URI = 'mongodb://localhost:27017/'
    DATABASE_NAME = 'llm_questions'
    COLLECTION_NAME = 'llm_data'

def test_groq_connection():
    """Test connection to Groq API"""
    try:
        client = Groq(api_key=Config.GROQ_API_KEY)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Can you confirm the API is working?"}
            ],
            model="llama3-8b-8192"
        )
        
        logging.info("✅ Groq API Connection: Successful")
        logging.info(f"Response received: {chat_completion.choices[0].message.content}")
        return True
    except Exception as e:
        logging.error(f"❌ Groq API Connection Failed: {e}")
        return False

def test_mongodb_connection():
    """Test connection to MongoDB"""
    try:
        client = MongoClient(Config.MONGODB_URI)

        db = client[Config.DATABASE_NAME]

        collection = db[Config.COLLECTION_NAME]
        
        test_document = {"test": "connection"}
        result = collection.insert_one(test_document)

        collection.delete_one({"_id": result.inserted_id})
        
        logging.info("✅ MongoDB Connection: Successful")
        logging.info(f"Database: {Config.DATABASE_NAME}")
        logging.info(f"Collection: {Config.COLLECTION_NAME}")
        return True
    except Exception as e:
        logging.error(f"❌ MongoDB Connection Failed: {e}")
        return False

def main():
    """Main function to test connections"""
    print("🔍 Checking Groq API and MongoDB Connections...")
    
    groq_status = test_groq_connection()
    mongodb_status = test_mongodb_connection()
    
    if groq_status and mongodb_status:
        print("\n✨ All Connections Successful! ✨")
    else:
        print("\n⚠️ Some Connections Failed. Check the logs above.")

if __name__ == "__main__":
    main()