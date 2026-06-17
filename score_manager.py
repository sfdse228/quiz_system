"""
score_manager.py - Менеджер подсчёта очков
"""

import json
import datetime
from typing import Dict, List, Optional
from src.answer_handler import AnswerResult
from src.logger_setup import logger


class Player:
    """Класс для представления игрока"""
    
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.total_questions = 0
        self.correct_answers = 0
        self.start_time = None
        self.end_time = None
    
    def add_score(self, points: int):
        """Добавляет очки игроку"""
        self.score += points
    
    def add_correct_answer(self):
        """Увеличивает счётчик правильных ответов"""
        self.correct_answers += 1
        self.total_questions += 1
    
    def add_total_question(self):
        """Увеличивает счётчик всех ответов"""
        self.total_questions += 1
    
    def get_accuracy(self) -> float:
        """Возвращает точность игрока"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'accuracy': round(self.get_accuracy(), 2),
            'start_time': self.start_time,
            'end_time': self.end_time
        }


class ScoreManager:
    """Класс для управления очками и статистикой"""
    
    def __init__(self, history_file: str = "data/scores.json"):
        self.history_file = history_file
        self.current_player: Optional[Player] = None
        self.history: List[Dict] = []
        self._load_history()
    
    def _load_history(self):
        """Загружает историю игр"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
    
    def _save_history(self):
        """Сохраняет историю игр"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения истории: {e}")
    
    def start_game(self, player_name: str):
        """Начинает новую игру для игрока"""
        self.current_player = Player(player_name)
        self.current_player.start_time = datetime.datetime.now().isoformat()
        logger.info(f"Новая игра для игрока: {player_name}")
    
    def process_results(self, results: List[AnswerResult], difficulty: str = "easy"):
        """Обрабатывает результаты и начисляет очки"""
        if not self.current_player:
            logger.error("Нет активного игрока")
            return
        
        # Начисляем очки в зависимости от сложности
        difficulty_multiplier = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }.get(difficulty, 1)
        
        for result in results:
            self.current_player.add_total_question()
            if result.is_correct:
                self.current_player.add_correct_answer()
                # Очки: базовое значение 10 * множитель сложности
                points = 10 * difficulty_multiplier
                self.current_player.add_score(points)
        
        self.current_player.end_time = datetime.datetime.now().isoformat()
        
        # Сохраняем историю
        self._save_game_history(difficulty)
        
        logger.info(f"Игра завершена. Игрок: {self.current_player.name}, Очки: {self.current_player.score}")
    
    def _save_game_history(self, difficulty: str):
        """Сохраняет историю игры"""
        if self.current_player:
            game_record = {
                'player': self.current_player.name,
                'score': self.current_player.score,
                'total_questions': self.current_player.total_questions,
                'correct_answers': self.current_player.correct_answers,
                'accuracy': round(self.current_player.get_accuracy(), 2),
                'difficulty': difficulty,
                'date': datetime.datetime.now().isoformat()
            }
            self.history.append(game_record)
            self._save_history()
    
    def get_current_score(self) -> int:
        """Возвращает текущий счёт игрока"""
        if self.current_player:
            return self.current_player.score
        return 0
    
    def get_current_accuracy(self) -> float:
        """Возвращает текущую точность"""
        if self.current_player:
            return self.current_player.get_accuracy()
        return 0.0
    
    def get_current_player_stats(self) -> Dict:
        """Возвращает статистику текущего игрока"""
        if self.current_player:
            return self.current_player.to_dict()
        return {}
    
    def get_leaderboard(self, top_n: int = 5) -> List[Dict]:
        """Возвращает таблицу лидеров"""
        if not self.history:
            return []
        
        # Группируем по игрокам и суммируем очки
        player_scores = {}
        for game in self.history:
            name = game['player']
            if name not in player_scores:
                player_scores[name] = {
                    'name': name,
                    'total_score': 0,
                    'games_played': 0,
                    'total_questions': 0,
                    'total_correct': 0
                }
            player_scores[name]['total_score'] += game['score']
            player_scores[name]['games_played'] += 1
            player_scores[name]['total_questions'] += game['total_questions']
            player_scores[name]['total_correct'] += game['correct_answers']
        
        # Сортируем по очкам
        sorted_players = sorted(
            player_scores.values(),
            key=lambda x: x['total_score'],
            reverse=True
        )
        
        # Добавляем среднюю точность
        for player in sorted_players:
            if player['total_questions'] > 0:
                player['accuracy'] = round(
                    (player['total_correct'] / player['total_questions']) * 100, 2
                )
            else:
                player['accuracy'] = 0.0
        
        return sorted_players[:top_n]