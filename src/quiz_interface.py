"""
quiz_interface.py - Модуль консольного интерфейса
"""

import time
from typing import Optional
from src.data_loader import DataLoader
from src.answer_handler import AnswerHandler
from src.score_manager import ScoreManager
from src.logger_setup import logger


class QuizInterface:
    """Класс для консольного интерфейса викторины"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.answer_handler = AnswerHandler()
        self.score_manager = ScoreManager()
        self.current_player: Optional[str] = None
    
    def show_welcome(self):
        """Показывает приветственное сообщение"""
        print("\n" + "=" * 50)
        print("🎯 ДОБРО ПОЖАЛОВАТЬ В ВИКТОРИНУ!")
        print("=" * 50)
        print(f"📚 Всего вопросов: {self.data_loader.get_question_count()}")
        print(f"🏷️ Категории: {', '.join(self.data_loader.get_categories())}")
        print("=" * 50)
    
    def show_main_menu(self):
        """Показывает главное меню"""
        print("\n" + "=" * 40)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 40)
        print("1. 🎮 Начать викторину")
        print("2. 📊 Посмотреть статистику")
        print("3. 🏆 Таблица лидеров")
        print("4. 🚪 Выйти")
        print("=" * 40)
    
    def get_player_name(self) -> str:
        """Запрашивает имя игрока"""
        while True:
            name = input("\n👤 Введите ваше имя: ").strip()
            if name:
                return name
            print("❌ Имя не может быть пустым!")
    
    def select_difficulty(self) -> str:
        """Выбор сложности"""
        print("\n📊 ВЫБЕРИТЕ СЛОЖНОСТЬ:")
        print("1. Легкая (1x очки)")
        print("2. Средняя (2x очки)")
        print("3. Сложная (3x очки)")
        
        while True:
            choice = input("Выберите (1-3): ").strip()
            if choice == "1":
                return "easy"
            elif choice == "2":
                return "medium"
            elif choice == "3":
                return "hard"
            print("❌ Неверный выбор!")
    
    def select_question_mode(self) -> str:
        """Выбор режима вопросов"""
        print("\n📝 ВЫБЕРИТЕ РЕЖИМ ВОПРОСОВ:")
        print("1. Все вопросы")
        print("2. По категории")
        print("3. Случайные 5 вопросов")
        
        while True:
            choice = input("Выберите (1-3): ").strip()
            if choice == "1":
                return "all"
            elif choice == "2":
                return "category"
            elif choice == "3":
                return "random"
            print("❌ Неверный выбор!")
    
    def get_questions(self, mode: str) -> list:
        """Получает вопросы в зависимости от режима"""
        if mode == "all":
            return self.data_loader.get_all_questions()
        elif mode == "category":
            categories = self.data_loader.get_categories()
            print("\n📂 ДОСТУПНЫЕ КАТЕГОРИИ:")
            for i, cat in enumerate(categories, 1):
                count = len(self.data_loader.get_questions_by_category(cat))
                print(f"   {i}. {cat} ({count} вопросов)")
            
            while True:
                try:
                    choice = int(input("Выберите номер категории: "))
                    if 1 <= choice <= len(categories):
                        category = categories[choice - 1]
                        return self.data_loader.get_questions_by_category(category)
                except ValueError:
                    pass
                print("❌ Неверный выбор!")
        elif mode == "random":
            return self.data_loader.get_random_questions(5)
        return []
    
    def ask_question(self, question) -> int:
        """Задаёт вопрос и возвращает ответ пользователя"""
        print("\n" + "-" * 40)
        print(f"📌 {question.question}")
        print(f"🏷️ Категория: {question.category} | Сложность: {question.difficulty}")
        print("-" * 40)
        
        for i, option in enumerate(question.options):
            print(f"   {chr(65 + i)}. {option}")  # A, B, C, D
        
        while True:
            answer = input("\nВаш ответ (A, B, C, D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                return ord(answer) - ord('A')
            print("❌ Неверный ввод! Введите A, B, C или D")
    
    def show_answer_result(self, result):
        """Показывает результат ответа"""
        if result.is_correct:
            print("\n✅ ПРАВИЛЬНО!")
        else:
            print("\n❌ НЕПРАВИЛЬНО!")
            print(f"Правильный ответ: {result.correct_answer}")
        print(f"Вы ответили: {result.user_answer_text}")
        time.sleep(1)
    
    def show_final_results(self):
        """Показывает финальные результаты"""
        results = self.answer_handler.get_results()
        correct = self.answer_handler.get_correct_count()
        total = len(results)
        accuracy = (correct / total * 100) if total > 0 else 0
        score = self.score_manager.get_current_score()
        
        print("\n" + "=" * 50)
        print("🏆 РЕЗУЛЬТАТЫ ВИКТОРИНЫ")
        print("=" * 50)
        print(f"👤 Игрок: {self.current_player}")
        print(f"📊 Всего вопросов: {total}")
        print(f"✅ Правильных: {correct}")
        print(f"❌ Неправильных: {total - correct}")
        print(f"🎯 Точность: {accuracy:.1f}%")
        print(f"⭐ Очки: {score}")
        
        # Детальные результаты
        print("\n📝 ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
        print("-" * 50)
        for i, result in enumerate(results, 1):
            status = "✅" if result.is_correct else "❌"
            print(f"{i}. {status} {result.question.question[:50]}...")
        
        print("=" * 50)
        
        # Сохраняем в историю
        logger.info(f"Игра завершена. Игрок: {self.current_player}, Очки: {score}")
    
    def show_statistics(self):
        """Показывает статистику текущего игрока"""
        stats = self.score_manager.get_current_player_stats()
        if not stats:
            print("\n❌ Нет статистики для текущего игрока")
            return
        
        print("\n" + "=" * 40)
        print(f"📊 СТАТИСТИКА ИГРОКА: {stats['name']}")
        print("=" * 40)
        print(f"🎯 Очки: {stats['score']}")
        print(f"📝 Всего вопросов: {stats['total_questions']}")
        print(f"✅ Правильных: {stats['correct_answers']}")
        print(f"🎯 Точность: {stats['accuracy']}%")
        print("=" * 40)
    
    def show_leaderboard(self):
        """Показывает таблицу лидеров"""
        leaderboard = self.score_manager.get_leaderboard(5)
        
        if not leaderboard:
            print("\n📭 История игр пуста. Сыграйте первую игру!")
            return
        
        print("\n" + "=" * 50)
        print("🏆 ТАБЛИЦА ЛИДЕРОВ")
        print("=" * 50)
        print(f"{'#':>3} {'Игрок':<15} {'Очки':<8} {'Игры':<6} {'Точность':>8}")
        print("-" * 50)
        
        for i, player in enumerate(leaderboard, 1):
            print(f"{i:>3} {player['name']:<15} {player['total_score']:<8} {player['games_played']:<6} {player['accuracy']:>7.1f}%")
        print("=" * 50)
    
    def start_quiz(self):
        """Запускает процесс викторины"""
        # Выбор игрока
        player_name = self.get_player_name()
        self.current_player = player_name
        self.score_manager.start_game(player_name)
        
        # Выбор сложности
        difficulty = self.select_difficulty()
        
        # Выбор режима вопросов
        mode = self.select_question_mode()
        questions = self.get_questions(mode)
        
        if not questions:
            print("❌ Нет вопросов для выбранного режима!")
            return
        
        print(f"\n🎯 Начинаем викторину! Всего вопросов: {len(questions)}")
        print("=" * 40)
        time.sleep(1)
        
        # Запускаем обработчик
        self.answer_handler.start_quiz(questions)
        
        # Цикл вопросов
        while self.answer_handler.has_next_question():
            question = self.answer_handler.get_current_question()
            answer_index = self.ask_question(question)
            result = self.answer_handler.submit_answer(answer_index)
            self.show_answer_result(result)
        
        # Обрабатываем результаты
        self.score_manager.process_results(
            self.answer_handler.get_results(),
            difficulty
        )
        
        # Показываем финальные результаты
        self.show_final_results()
        
        # Спрашиваем, хочет ли игрок продолжить
        print("\nХотите сыграть ещё раз? (y/n): ", end="")
        if input().lower() == 'y':
            self.start_quiz()
    
    def run(self):
        """Запускает основной цикл программы"""
        self.show_welcome()
        
        while True:
            self.show_main_menu()
            choice = input("Выберите действие (1-4): ").strip()
            
            if choice == "1":
                self.start_quiz()
            elif choice == "2":
                self.show_statistics()
            elif choice == "3":
                self.show_leaderboard()
            elif choice == "4":
                print("\n👋 До свидания! Спасибо за игру!")
                logger.info("Завершение программы")
                break
            else:
                print("❌ Неверный выбор!")
            
            if choice != "1":  # После викторины не ждём Enter
                input("\nНажмите Enter для продолжения...")
