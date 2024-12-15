from question_generator import QuestionGenerator
from database import DatabaseManager
from paper_generator import PaperGenerator


question_generator = QuestionGenerator()
db_manager = DatabaseManager()
paper_generator = PaperGenerator(db_manager)

topic = "INFORMATICS PRACTICES"
    
question_generator.generate_questions(
    topic, 
    num_easy=1, 
    num_medium=1, 
    num_hard=0
)
question_paper = paper_generator.generate_question_paper(
    topic, 
    num_easy=1, 
    num_medium=1, 
    num_hard=0
)

print(question_paper)


    
