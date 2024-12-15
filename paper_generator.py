import random
from typing import List, Dict, Any, Optional

class InsufficientQuestionsError(Exception):
    """Raised when not enough questions are available for the paper"""
    pass

class PaperGenerator:
    def __init__(self, db_manager: 'DatabaseManager'):
        """
        Initialize the PaperGenerator with a database manager.
        
        :param db_manager: Database manager to fetch questions
        """
        self.db_manager = db_manager

    def generate_question_paper(
        self, 
        topic: str, 
        num_easy: int = 3, 
        num_medium: int = 2, 
        num_hard: int = 1
    ) -> Dict[str, Any]:
        available_difficulties = list(self.db_manager.collection.distinct(
            'Difficulty', 
            {'Topic': topic}
        ))

        print(f"Available difficulties for {topic}: {available_difficulties}")

        difficulty_map = {
            'easy': ['Easy', 'Medium'],
            'medium': ['Medium'],
            'hard': ['Hard']
        }

        question_paper = {
            'topic': topic,
            'questions': []
        }

        for difficulty, count in [('easy', num_easy), ('medium', num_medium), ('hard', num_hard)]:
            questions = []
            for diff_option in difficulty_map.get(difficulty, [difficulty.capitalize()]):
                questions = self.db_manager.get_questions_by_topic_and_difficulty(
                    topic, diff_option, limit=count * 3
                )
                if questions:
                    break
            
            if len(questions) < count:
                raise InsufficientQuestionsError(
                    f"Not enough {difficulty} questions available for topic '{topic}'. "
                    f"Required: {count}, Available: {len(questions)}"
                )
            
            selected_questions = random.sample(questions, count)
            question_paper['questions'].extend(selected_questions)

        return question_paper

    def generate_multiple_papers(
        self, 
        topic: str, 
        num_papers: int, 
        num_easy: int = 3, 
        num_medium: int = 2, 
        num_hard: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple unique question papers.
        """
        papers = []
        for _ in range(num_papers):
            paper = self.generate_question_paper(
                topic, num_easy, num_medium, num_hard
            )
            papers.append(paper)
        
        return papers