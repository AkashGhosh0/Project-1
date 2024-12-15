import logging
import json
from groq import Groq
from config import Config
from database import DatabaseManager

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('question_generator.log'),
        logging.StreamHandler()
    ]
)

class QuestionGenerator:
    def __init__(self):
        try:
            self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
            logging.info("✅ Groq Client Initialized Successfully")
            
            self.db_manager = DatabaseManager()
            logging.info("✅ Database Manager Initialized Successfully")
        
        except Exception as e:
            logging.error(f"❌ Initialization Failed: {e}")
            raise

    def generate_questions(
        self,
        topic: str,
        num_easy: int = 3,
        num_medium: int = 2,
        num_hard: int = 1
    ):
        """
        Generate questions using Groq API and store in MongoDB
        
        :param topic: Subject/topic for question generation
        :param num_easy: Number of easy questions to generate
        :param num_medium: Number of medium questions to generate
        :param num_hard: Number of hard questions to generate
        :return: List of generated questions
        """
        logging.info(f"🚀 Starting Question Generation")
        logging.info(f"Topic: {topic}")
        logging.info(f"Question Distribution - Easy: {num_easy}, Medium: {num_medium}, Hard: {num_hard}")

        difficulties = [
            ('Easy', num_easy),
            ('Medium', num_medium),
            ('Hard', num_hard)
        ]

        generated_questions = []

        for difficulty, count in difficulties:
            try:
                logging.info(f"Generating {count} {difficulty} questions")
                
                # Detailed prompt with specific instructions
                prompt = f"""
                Generate {count} {difficulty.lower()} level multiple-choice questions on the topic: {topic}
                
                For each question, provide:
                - Question Number (incremental)
                - Question Text
                - Option A
                - Option B
                - Option C
                - Option D
                - Correct Answer
                - Explanation
                - Difficulty Level
                
                Output Format (JSON):
                {{
                    "Question Number": "1",
                    "Topic": "{topic}",
                    "Question Text": "...",
                    "Option A": "...",
                    "Option B": "...", 
                    "Option C": "...",
                    "Option D": "...",
                    "Correct Answer": "...",
                    "Explanation": "...",
                    "Difficulty": "{difficulty}"
                }}
                """

                # Generate questions using Groq
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert educational question generator."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192",
                    response_format={"type": "json_object"}
                )

                try:
                    questions_data = json.loads(chat_completion.choices[0].message.content)
                    
                    if not isinstance(questions_data, list):
                        questions_data = [questions_data]
                    
                    generated_questions.extend(questions_data)
                    logging.info(f"✅ Successfully generated {len(questions_data)} {difficulty} questions")
                
                except json.JSONDecodeError as json_err:
                    logging.error(f"❌ JSON Parsing Error: {json_err}")
                    logging.error(f"Raw Content: {chat_completion.choices[0].message.content}")
                
            except Exception as e:
                logging.error(f"❌ Error generating {difficulty} questions: {e}")
                continue

        try:
            if generated_questions:
                insert_result = self.db_manager.insert_questions(generated_questions)
                logging.info(f"💾 Inserted {len(generated_questions)} questions into MongoDB")
            else:
                logging.warning("⚠️ No questions were generated")
        
        except Exception as e:
            logging.error(f"❌ Database Insertion Failed: {e}")

        return generated_questions

# def main():
#     """
#     Main function to demonstrate question generation
#     """
#     try:
#         question_generator = QuestionGenerator()

#         generated_questions = question_generator.generate_questions(
#             topic="Python Programming",
#             num_easy=2,
#             num_medium=1,
#             num_hard=1
#         )
        
#         print("\n📋 Generated Questions:")
#         for q in generated_questions:
#             print(f"\nQuestion: {q.get('Question Text', 'N/A')}")
#             print(f"Difficulty: {q.get('Difficulty', 'N/A')}")
    
#     except Exception as e:
#         logging.error(f"❌ Main Execution Failed: {e}")

# if __name__ == "__main__":
#     main()