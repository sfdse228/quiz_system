"""
answer_handler.py - Модуль обработки ответов
"""

from typing import Dict, List
from src.data_loader import Question
from src.logger_setup import logger


class AnswerResult:
    """Класс для хранения результата ответа"""
    
    def __init__(self, question: Question, user_answer: int, is_correct: bool):
        self.question = question
        self.user_answer = user_answer
        self.is_correct = is_correct
        self.correct_answer = question.get_correct_answer()
        self.user_answer_text = question.options[user_answer] if 0 <= user_answer < len(question.options) else "Нет ответа"
    
    def to_dict(self) -> Dict:
        return {
            'question_id': self.question.id,
            'question_text': self.question.question,
            'user_answer': self.user_answer_text,
            'correct_answer': self.correct_answer,
            'is_correct': self.is_correct
        }


class AnswerHandler:
    """Класс для обработки ответов пользователя"""
    
    def __init__(self):
        self.results: List[AnswerResult] = []
        self.current_question_index = 0
        self.total_questions = 0
    
    def start_quiz(self, questions: List[Question]):
        """Начинает викторину с указанными вопросами"""
        self.questions = questions
        self.results = []
        self.current_question_index = 0
        self.total_questions = len(questions)
        logger.info(f"Начата викторина. Количество вопросов: {self.total_questions}")
    
    def get_current_question(self) -> Question:
        """Возвращает текущий вопрос"""
        if self.current_question_index < self.total_questions:
            return self.questions[self.current_question_index]
        return None
    
    def has_next_question(self) -> bool:
        """Проверяет, есть ли следующий вопрос"""
        return self.current_question_index < self.total_questions
    
    def submit_answer(self, answer_index: int) -> AnswerResult:
        """Принимает ответ пользователя и возвращает результат"""
        question = self.get_current_question()
        if not question:
            return None
        
        # Проверяем корректность индекса ответа
        if not (0 <= answer_index < len(question.options)):
            logger.warning(f"Неверный индекс ответа: {answer_index}")
            answer_index = -1  # Неверный ответ
        
        is_correct = question.is_correct(answer_index)
        result = AnswerResult(question, answer_index, is_correct)
        self.results.append(result)
        
        # Логируем ответ
        logger.info(f"Вопрос {question.id}: {'✅' if is_correct else '❌'} - {question.question[:30]}...")
        
        self.current_question_index += 1
        return result
    
    def get_results(self) -> List[AnswerResult]:
        """Возвращает все результаты"""
        return self.results
    
    def get_correct_count(self) -> int:
        """Возвращает количество правильных ответов"""
        return sum(1 for r in self.results if r.is_correct)
    
    def get_incorrect_count(self) -> int:
        """Возвращает количество неправильных ответов"""
        return self.total_questions - self.get_correct_count()
    
    def get_accuracy(self) -> float:
        """Возвращает точность ответов (процент правильных)"""
        if self.total_questions == 0:
            return 0.0
        return (self.get_correct_count() / self.total_questions) * 100
    
    def reset(self):
        """Сбрасывает состояние обработчика"""
        self.results = []
        self.current_question_index = 0
        self.total_questions = 0
        logger.info("Сброс состояния викторины")