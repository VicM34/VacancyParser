import os
from typing import Any, Dict, List, Optional

from src.abstract_classes import FileHandler
from src.vacancy import Vacancy


class TXTSaver(FileHandler):
    """Класс для сохранения вакансий в текстовый файл"""

    def __init__(self, filename: str = "data/vacancies.txt") -> None:
        self._filename = filename
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Создание директории, если она не существует"""
        directory = os.path.dirname(self._filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _vacancy_to_string(self, vacancy: Vacancy) -> str:
        """Преобразование вакансии в строку для TXT-файла"""
        salary_info = "Зарплата не указана"
        if vacancy.salary:
            salary = vacancy.salary
            from_salary = salary.get("from")
            to_salary = salary.get("to")
            currency = salary.get("currency", "RUR")

            if from_salary and to_salary:
                salary_info = f"{from_salary:,} - {to_salary:,} {currency}"
            elif from_salary:
                salary_info = f"от {from_salary:,} {currency}"
            elif to_salary:
                salary_info = f"до {to_salary:,} {currency}"

        return (
            f"Вакансия: {vacancy.title}\n"
            f"Зарплата: {salary_info}\n"
            f"Ссылка: {vacancy.url}\n"
            f"Описание: {vacancy.description}\n"
            f"Требования: {vacancy.requirements}"
        )

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в текстовый файл"""
        try:
            with open(self._filename, "a", encoding="utf-8") as f:
                f.write(self._vacancy_to_string(vacancy))
                f.write("\n" + "=" * 50 + "\n\n")

        except IOError as e:
            print(f"Ошибка при добавлении вакансии в TXT-файл: {e}")

    def get_vacancies(
        self, criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Получение вакансий из TXT-файла (заглушка)"""
        # Для TXT-файлов сложно реализовать полноценное чтение и фильтрацию
        return []

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из TXT-файла (заглушка)"""
        print("Удаление отдельных вакансий из TXT-файла не поддерживается")

    def clear_all(self) -> None:
        """Очистка всех вакансий из TXT-файла"""
        try:
            with open(self._filename, "w", encoding="utf-8"):
                pass
        except IOError as e:
            print(f"Ошибка при очистке TXT-файла: {e}")
