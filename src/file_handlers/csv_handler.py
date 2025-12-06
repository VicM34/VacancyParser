import csv
import os
from typing import Any, Dict, List, Optional

from src.abstract_classes import FileHandler
from src.vacancy import Vacancy


class CSVSaver(FileHandler):
    """Класс для сохранения вакансий в CSV-файл"""

    def __init__(self, filename: str = "data/vacancies.csv") -> None:
        self._filename = filename
        self._ensure_directory_exists()
        self._fieldnames = [
            "title",
            "url",
            "salary_from",
            "salary_to",
            "currency",
            "description",
            "requirements",
            "avg_salary",
        ]

    def _ensure_directory_exists(self) -> None:
        """Создание директории, если она не существует"""
        directory = os.path.dirname(self._filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def add_vacancy(self, vacancy: Vacancy) -> None:  # ИЗМЕНЕНО: принимает Vacancy
        """
        Добавление вакансии в CSV-файл.
        """
        vacancies = self.get_vacancies()
        vacancy_dict = vacancy.to_dict()  # Преобразуем Vacancy в словарь

        # Проверяем, нет ли уже такой вакансии по URL
        url = vacancy_dict.get("url", "")
        if not any(v.get("url") == url for v in vacancies):
            vacancies.append(vacancy_dict)
            self._save_all_vacancies(vacancies)

    def _save_all_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Сохранение всех вакансий в CSV-файл"""
        try:
            with open(self._filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self._fieldnames)
                writer.writeheader()  # Всегда пишем заголовок

                for vacancy in vacancies:
                    # Извлекаем данные о зарплате безопасно
                    salary = vacancy.get("salary")

                    if isinstance(salary, dict):
                        salary_from = salary.get("from", 0)
                        salary_to = salary.get("to", 0)
                        currency = salary.get("currency", "RUR")
                    else:
                        salary_from = vacancy.get("salary_from", 0)
                        salary_to = vacancy.get("salary_to", 0)
                        currency = vacancy.get("currency", "RUR")

                    # Преобразуем в int если нужно
                    try:
                        salary_from = int(salary_from) if salary_from else 0
                    except (ValueError, TypeError):
                        salary_from = 0

                    try:
                        salary_to = int(salary_to) if salary_to else 0
                    except (ValueError, TypeError):
                        salary_to = 0

                    # Получаем avg_salary
                    avg_salary = vacancy.get("avg_salary", 0)
                    try:
                        avg_salary = int(avg_salary) if avg_salary else 0
                    except (ValueError, TypeError):
                        avg_salary = 0

                    row = {
                        "title": str(vacancy.get("title", "")),
                        "url": str(vacancy.get("url", "")),
                        "salary_from": salary_from,
                        "salary_to": salary_to,
                        "currency": str(currency),
                        "description": str(vacancy.get("description", "")),
                        "requirements": str(vacancy.get("requirements", "")),
                        "avg_salary": avg_salary,
                    }
                    writer.writerow(row)

        except IOError as e:
            print(f"Ошибка при сохранении CSV-файла: {e}")

    def get_vacancies(
        self, criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Получение вакансий из CSV-файла по критериям"""
        vacancies: List[Dict[str, Any]] = []

        if not os.path.exists(self._filename):
            return vacancies

        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Безопасное преобразование типов
                    salary_from_str = row.get("salary_from", "0")
                    salary_to_str = row.get("salary_to", "0")
                    avg_salary_str = row.get("avg_salary", "0")

                    try:
                        salary_from = int(salary_from_str) if salary_from_str else 0
                    except ValueError:
                        salary_from = 0

                    try:
                        salary_to = int(salary_to_str) if salary_to_str else 0
                    except ValueError:
                        salary_to = 0

                    try:
                        avg_salary = int(avg_salary_str) if avg_salary_str else 0
                    except ValueError:
                        avg_salary = 0

                    vacancy = {
                        "title": row.get("title", ""),
                        "url": row.get("url", ""),
                        "salary": {
                            "from": salary_from,
                            "to": salary_to,
                            "currency": row.get("currency", "RUR"),
                        },
                        "description": row.get("description", ""),
                        "requirements": row.get("requirements", ""),
                        "avg_salary": avg_salary,
                    }

                    # Если зарплата не указана (обе границы 0)
                    salary_data = vacancy.get("salary", {})
                    salary_data = vacancy.get("salary", {})
                    if (
                        isinstance(salary_data, dict)
                        and salary_data.get("from", 0) == 0
                        and salary_data.get("to", 0) == 0
                    ):
                        vacancy["salary"] = None

                    # Фильтрация по критериям
                    if criteria and self._matches_criteria(vacancy, criteria):
                        vacancies.append(vacancy)
                    elif not criteria:
                        vacancies.append(vacancy)

        except (IOError, csv.Error, ValueError) as e:
            print(f"Ошибка при чтении CSV-файла: {e}")

        return vacancies

    def _matches_criteria(
        self, vacancy: Dict[str, Any], criteria: Dict[str, Any]
    ) -> bool:
        """Проверка соответствия вакансии критериям"""
        match = True

        if "keyword" in criteria:
            keyword = str(criteria["keyword"]).lower()
            title = str(vacancy.get("title", "")).lower()
            description = str(vacancy.get("description", "")).lower()
            requirements = str(vacancy.get("requirements", "")).lower()

            if (
                keyword not in title
                and keyword not in description
                and keyword not in requirements
            ):
                match = False

        if "salary_range" in criteria:
            salary_range = criteria["salary_range"]
            if isinstance(salary_range, dict):
                min_salary = salary_range.get("min", 0)
                avg_salary = vacancy.get("avg_salary", 0)

                if avg_salary < min_salary:
                    match = False

        return match

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаление вакансии из CSV-файла по ID (URL).
        """
        vacancies = self.get_vacancies()
        vacancy_url = vacancy.url

        if not vacancy_url:
            return

        # Удаляем вакансии с таким URL
        initial_count = len(vacancies)
        new_vacancies = []

        for v in vacancies:
            current_url = v.get("url", "")
            # Сравниваем URL, игнорируя пробелы и регистр
            if current_url.strip().lower() != vacancy_url.strip().lower():
                new_vacancies.append(v)

        # Сохраняем только если что-то изменилось
        if len(new_vacancies) < initial_count:
            self._save_all_vacancies(new_vacancies)

    def clear_all(self) -> None:
        """Очистка всех вакансий из CSV-файла"""
        try:
            with open(self._filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self._fieldnames)
                writer.writeheader()
        except IOError as e:
            print(f"Ошибка при очистке CSV-файла: {e}")
