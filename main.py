"""
Точка входа для VacancyParser
"""

from src.user_interaction import user_interaction


def main() -> None:
    """Основная функция программы"""
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена пользователем.")
    except Exception as e:
        print(f"\n Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
