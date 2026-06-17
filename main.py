#!/usr/bin/env python3
"""
main.py - Точка входа в консольную викторину
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.quiz_interface import QuizInterface
from src.logger_setup import logger


def main():
    """Главная функция"""
    try:
        quiz = QuizInterface()
        quiz.run()
    except KeyboardInterrupt:
        print("\n\n👋 Принудительное завершение...")
        logger.info("Принудительное завершение программы")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()