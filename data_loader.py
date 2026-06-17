"""
data_loader.py - Модуль данных и генерации вопросов
"""

import json
import random
from typing import List, Dict, Optional


class Question:
    """Класс для представления вопроса"""
    
    def __init__(self, data: Dict):
        self.id = data.get('id', 0)
        self.category = data.get('category', '')
        self.question = data.get('question', '')
        self.options = data.get('options', [])
        self.correct = data.get('correct', 0)
        self.difficulty = data.get('difficulty', 'easy')
    
    def to_dict(self) -> Dict:
        """Преобразует вопрос в словарь"""
        return {
            'id': self.id,
            'category': self.category,
            'question': self.question,
            'options': self.options,
            'correct': self.correct,
            'difficulty': self.difficulty
        }
    
    def get_correct_answer(self) -> str:
        """Возвращает правильный ответ"""
        if 0 <= self.correct < len(self.options):
            return self.options[self.correct]
        return ""
    
    def is_correct(self, answer_index: int) -> bool:
        """Проверяет, правильный ли ответ"""
        return answer_index == self.correct
    
    def __str__(self) -> str:
        return f"{self.category}: {self.question}"


class DataLoader:
    """Класс для загрузки и управления вопросами"""
    
    def __init__(self, filepath: str = "data/questions.json"):
        self.filepath = filepath
        self.questions: List[Question] = []
        self._load_questions()
    
    def _load_questions(self):
        """Загружает вопросы из JSON-файла"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = [Question(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Ошибка загрузки вопросов: {e}")
            self.questions = []
    
    def get_all_questions(self) -> List[Question]:
        """Возвращает все вопросы"""
        return self.questions
    
    def get_questions_by_category(self, category: str) -> List[Question]:
        """Возвращает вопросы по категории"""
        return [q for q in self.questions if q.category == category]
    
    def get_questions_by_difficulty(self, difficulty: str) -> List[Question]:
        """Возвращает вопросы по сложности"""
        return [q for q in self.questions if q.difficulty == difficulty]
    
    def get_random_questions(self, count: int = 5) -> List[Question]:
        """Возвращает случайные вопросы"""
        if count > len(self.questions):
            count = len(self.questions)
        return random.sample(self.questions, count)
    
    def get_categories(self) -> List[str]:
        """Возвращает список всех категорий"""
        categories = set(q.category for q in self.questions)
        return sorted(list(categories))
    
    def get_question_count(self) -> int:
        """Возвращает количество вопросов"""
        return len(self.questions)
    
    def get_question_by_id(self, question_id: int) -> Optional[Question]:
        """Возвращает вопрос по ID"""
        for q in self.questions:
            if q.id == question_id:
                return q
        return None