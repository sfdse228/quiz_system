"""
logger_setup.py - Настройка логирования
"""

import logging
import os


def setup_logger():
    """Настраивает логирование"""
    
    # Создаём папку для логов
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Настраиваем логгер
    logger = logging.getLogger('quiz')
    logger.setLevel(logging.DEBUG)
    
    # Очищаем существующие обработчики
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик для файла
    file_handler = logging.FileHandler('logs/quiz.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Обработчик для консоли (только INFO и выше)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Создаём логгер для использования в других модулях
logger = setup_logger()
