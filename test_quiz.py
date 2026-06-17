"""
test_quiz.py - Тесты для викторины
Запускаются отдельно, не мешают игре
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import DataLoader, Question
from src.answer_handler import AnswerHandler
from src.score_manager import ScoreManager, Player


class TestQuestion(unittest.TestCase):
    """Тесты для класса Question"""
    
    def setUp(self):
        self.data = {
            'id': 1,
            'category': 'Test',
            'question': 'Test question?',
            'options': ['A', 'B', 'C', 'D'],
            'correct': 2,
            'difficulty': 'easy'
        }
        self.question = Question(self.data)
    
    def test_question_creation(self):
        """Тест: создание вопроса"""
        self.assertEqual(self.question.id, 1)
        self.assertEqual(self.question.category, 'Test')
        self.assertEqual(self.question.question, 'Test question?')
        self.assertEqual(len(self.question.options), 4)
        self.assertEqual(self.question.correct, 2)
    
    def test_get_correct_answer(self):
        """Тест: получение правильного ответа"""
        self.assertEqual(self.question.get_correct_answer(), 'C')
    
    def test_is_correct(self):
        """Тест: проверка правильности ответа"""
        self.assertTrue(self.question.is_correct(2))
        self.assertFalse(self.question.is_correct(0))
    
    def test_to_dict(self):
        """Тест: преобразование в словарь"""
        d = self.question.to_dict()
        self.assertEqual(d['id'], 1)
        self.assertEqual(d['category'], 'Test')


class TestDataLoader(unittest.TestCase):
    """Тесты для DataLoader"""
    
    def setUp(self):
        # Создаём временный файл с тестовыми данными
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        test_data = [
            {
                'id': 1,
                'category': 'Test',
                'question': 'Test question 1?',
                'options': ['A', 'B', 'C', 'D'],
                'correct': 0,
                'difficulty': 'easy'
            },
            {
                'id': 2,
                'category': 'Test',
                'question': 'Test question 2?',
                'options': ['A', 'B', 'C', 'D'],
                'correct': 1,
                'difficulty': 'medium'
            }
        ]
        json.dump(test_data, self.temp_file)
        self.temp_file.close()
        
        self.loader = DataLoader(self.temp_file.name)
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_load_questions(self):
        """Тест: загрузка вопросов"""
        questions = self.loader.get_all_questions()
        self.assertEqual(len(questions), 2)
    
    def test_get_categories(self):
        """Тест: получение категорий"""
        categories = self.loader.get_categories()
        self.assertEqual(categories, ['Test'])
    
    def test_get_random_questions(self):
        """Тест: получение случайных вопросов"""
        questions = self.loader.get_random_questions(1)
        self.assertEqual(len(questions), 1)
    
    def test_get_question_by_id(self):
        """Тест: получение вопроса по ID"""
        q = self.loader.get_question_by_id(1)
        self.assertIsNotNone(q)
        self.assertEqual(q.id, 1)


class TestAnswerHandler(unittest.TestCase):
    """Тесты для AnswerHandler"""
    
    def setUp(self):
        self.handler = AnswerHandler()
        self.test_questions = [
            Question({
                'id': 1,
                'category': 'Test',
                'question': 'Test 1?',
                'options': ['A', 'B'],
                'correct': 0,
                'difficulty': 'easy'
            }),
            Question({
                'id': 2,
                'category': 'Test',
                'question': 'Test 2?',
                'options': ['A', 'B'],
                'correct': 1,
                'difficulty': 'easy'
            })
        ]
        self.handler.start_quiz(self.test_questions)
    
    def test_start_quiz(self):
        """Тест: начало викторины"""
        self.assertEqual(self.handler.total_questions, 2)
        self.assertTrue(self.handler.has_next_question())
    
    def test_submit_answer(self):
        """Тест: отправка ответа"""
        question = self.handler.get_current_question()
        result = self.handler.submit_answer(0)
        self.assertIsNotNone(result)
        self.assertEqual(result.question.id, question.id)
        self.assertTrue(result.is_correct)
    
    def test_get_results(self):
        """Тест: получение результатов"""
        self.handler.submit_answer(0)
        self.handler.submit_answer(1)
        results = self.handler.get_results()
        self.assertEqual(len(results), 2)
    
    def test_get_correct_count(self):
        """Тест: подсчёт правильных ответов"""
        self.handler.submit_answer(0)  # Правильный
        self.handler.submit_answer(0)  # Неправильный (правильный - 1)
        self.assertEqual(self.handler.get_correct_count(), 1)
        self.assertEqual(self.handler.get_incorrect_count(), 1)
    
    def test_get_accuracy(self):
        """Тест: расчёт точности"""
        self.handler.submit_answer(0)  # Правильный
        self.handler.submit_answer(0)  # Неправильный
        self.assertEqual(self.handler.get_accuracy(), 50.0)


class TestPlayer(unittest.TestCase):
    """Тесты для класса Player"""
    
    def setUp(self):
        self.player = Player('TestPlayer')
    
    def test_player_creation(self):
        """Тест: создание игрока"""
        self.assertEqual(self.player.name, 'TestPlayer')
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.total_questions, 0)
        self.assertEqual(self.player.correct_answers, 0)
    
    def test_add_score(self):
        """Тест: добавление очков"""
        self.player.add_score(10)
        self.assertEqual(self.player.score, 10)
        self.player.add_score(20)
        self.assertEqual(self.player.score, 30)
    
    def test_add_correct_answer(self):
        """Тест: добавление правильного ответа"""
        self.player.add_correct_answer()
        self.assertEqual(self.player.correct_answers, 1)
        self.assertEqual(self.player.total_questions, 1)
    
    def test_get_accuracy(self):
        """Тест: расчёт точности"""
        self.player.correct_answers = 3
        self.player.total_questions = 5
        self.assertEqual(self.player.get_accuracy(), 60.0)
        
        # Проверка деления на ноль
        empty_player = Player('Empty')
        self.assertEqual(empty_player.get_accuracy(), 0.0)


class TestScoreManager(unittest.TestCase):
    """Тесты для ScoreManager"""
    
    def setUp(self):
        # Создаём временный файл для истории
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump([], self.temp_file)
        self.temp_file.close()
        
        self.manager = ScoreManager(self.temp_file.name)
        self.manager.start_game('TestPlayer')
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_start_game(self):
        """Тест: начало игры"""
        self.assertIsNotNone(self.manager.current_player)
        self.assertEqual(self.manager.current_player.name, 'TestPlayer')
    
    def test_get_current_score(self):
        """Тест: получение текущего счёта"""
        self.assertEqual(self.manager.get_current_score(), 0)
        self.manager.current_player.add_score(50)
        self.assertEqual(self.manager.get_current_score(), 50)
    
    def test_get_current_accuracy(self):
        """Тест: получение текущей точности"""
        self.manager.current_player.correct_answers = 5
        self.manager.current_player.total_questions = 10
        self.assertEqual(self.manager.get_current_accuracy(), 50.0)
    
    def test_get_leaderboard(self):
        """Тест: таблица лидеров"""
        # Добавляем несколько игр в историю
        self.manager.history = [
            {'player': 'Alice', 'score': 100, 'total_questions': 10, 'correct_answers': 8, 'accuracy': 80.0, 'difficulty': 'easy', 'date': '2024-01-01'},
            {'player': 'Bob', 'score': 80, 'total_questions': 10, 'correct_answers': 6, 'accuracy': 60.0, 'difficulty': 'easy', 'date': '2024-01-02'},
            {'player': 'Alice', 'score': 120, 'total_questions': 10, 'correct_answers': 9, 'accuracy': 90.0, 'difficulty': 'medium', 'date': '2024-01-03'}
        ]
        
        leaderboard = self.manager.get_leaderboard(2)
        self.assertEqual(len(leaderboard), 2)
        self.assertEqual(leaderboard[0]['name'], 'Alice')
        self.assertEqual(leaderboard[0]['total_score'], 220)
        self.assertEqual(leaderboard[1]['name'], 'Bob')


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_full_quiz_flow(self):
        """Тест: полный цикл викторины"""
        # Создаём тестовые вопросы
        questions = [
            Question({
                'id': 1,
                'category': 'Test',
                'question': '2 + 2 = 4?',
                'options': ['Да', 'Нет'],
                'correct': 0,
                'difficulty': 'easy'
            })
        ]
        
        # Запускаем обработчик
        handler = AnswerHandler()
        handler.start_quiz(questions)
        
        # Отвечаем на вопрос
        result = handler.submit_answer(0)
        self.assertTrue(result.is_correct)
        
        # Проверяем результаты
        self.assertEqual(handler.get_correct_count(), 1)
        self.assertEqual(handler.get_accuracy(), 100.0)
        
        # Проверяем менеджер очков
        manager = ScoreManager()
        manager.start_game('TestPlayer')
        manager.process_results(handler.get_results(), 'easy')
        
        self.assertEqual(manager.get_current_score(), 10)  # 10 очков за лёгкий вопрос


def run_tests():
    """Запускает все тесты"""
    # Загружаем все тесты
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем все тестовые классы
    suite.addTests(loader.loadTestsFromTestCase(TestQuestion))
    suite.addTests(loader.loadTestsFromTestCase(TestDataLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestAnswerHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestPlayer))
    suite.addTests(loader.loadTestsFromTestCase(TestScoreManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Запускаем
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 ЗАПУСК ТЕСТОВ ВИКТОРИНЫ")
    print("=" * 40)
    success = run_tests()
    print("=" * 40)
    if success:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ! 🎉")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")