from pymongo import MongoClient
from config import Config
from typing import List, Dict, Any
import logging
from bson.objectid import ObjectId

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

class DatabaseManager:
    def __init__(self):
        try:
            self.client = MongoClient(
                Config.MONGODB_URI, 
                serverSelectionTimeoutMS=5000, 
                connectTimeoutMS=5000 
            )
            
            self.client.admin.command('ismaster')
            
            self.db = self.client[Config.DATABASE_NAME]
            self.collection = self.db[Config.COLLECTION_NAME]
            
            logging.info("✅ MongoDB Connection Successful!")
            logging.info(f"Connected to Database: {Config.DATABASE_NAME}")
            logging.info(f"Using Collection: {Config.COLLECTION_NAME}")
        
        except Exception as e:
            logging.error(f"❌ MongoDB Connection Failed: {e}")
            raise

    def insert_questions(self, questions: List[Dict[str, Any]]):
        """
        Insert multiple questions into the database
        
        :param questions: List of question dictionaries
        :return: Insertion result
        """
        try:
            # Validate input
            if not questions:
                logging.warning("No questions provided for insertion.")
                return None
            
            # Insert questions
            result = self.collection.insert_many(questions)
            
            logging.info(f"✅ Successfully inserted {len(result.inserted_ids)} questions")
            logging.info(f"Inserted IDs: {result.inserted_ids}")
            
            return result
        
        except Exception as e:
            logging.error(f"❌ Error inserting questions: {e}")
            return None

    def get_questions_by_topic_and_difficulty(
        self, 
        topic: str, 
        difficulty: str, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        try:
            query = {
                'Topic': topic,
                'Difficulty': {'$regex': f'^{difficulty}', '$options': 'i'}
            }

            questions = list(self.collection.find(query).limit(limit))
            
            logging.info(f"✅ Retrieved {len(questions)} questions")
            logging.info(f"Query: {query}")
            
            return questions
        
        except Exception as e:
            logging.error(f"❌ Error retrieving questions: {e}")
            return []

    

def main():
    """
    Test DatabaseManager functionality
    """
    try:
        db_manager = DatabaseManager()
        
        print("Testing DatabaseManager methods:")
        
        questions = db_manager.get_questions_by_topic_and_difficulty(
            topic="CSV File Module", 
            difficulty="Easy"
        )
        
        print("\nRetrieved Questions:")
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()