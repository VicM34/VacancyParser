from __future__ import annotations

from typing import Any, Dict, List, Optional, Union


class Vacancy:
    """Класс для представления и работы с вакансиями"""

    __slots__ = ("_title", "_url", "_salary", "_description", "_requirements")

    def __init__(
        self,
        title: str,
        url: str,
        salary: Optional[Dict[str, Optional[Union[int, str]]]],
        description: str,
        requirements: str = "",
    ) -> None:
        """
        Инициализация объекта вакансии

        Args:
            title: Название вакансии
            url: Ссылка на вакансию на hh.ru
            salary: Данные о зарплате
            description: Описание вакансии
            requirements: Требования к кандидату
        """
        self._title: str = self._validate_title(title)
        self._url: str = self._validate_url(url)
        self._salary: Optional[Dict[str, Any]] = self._validate_salary(salary)
        self._description: str = description
        self._requirements: str = requirements

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """Создание объекта Vacancy из словаря"""
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            salary=data.get("salary"),
            description=data.get("description", ""),
            requirements=data.get("requirements", ""),
        )

    @property
    def title(self) -> str:
        """Название вакансии"""
        return self._title

    @property
    def url(self) -> str:
        """Ссылка на вакансию"""
        return self._url

    @property
    def salary(self) -> Optional[Dict[str, Any]]:
        """Данные о зарплате"""
        return self._salary

    @property
    def description(self) -> str:
        """Описание вакансии"""
        return self._description

    @property
    def requirements(self) -> str:
        """Требования к кандидату"""
        return self._requirements

    @property
    def avg_salary(self) -> int:
        """Средняя зарплата для сравнения"""
        if not self._salary:
            return 0

        salary_from: int = self._salary.get("from", 0) or 0
        salary_to: int = self._salary.get("to", 0) or 0

        if salary_from and salary_to:
            return (salary_from + salary_to) // 2
        elif salary_from:
            return salary_from
        elif salary_to:
            return salary_to
        else:
            return 0

    def _validate_title(self, title: str) -> str:
        """Приватный метод валидации названия вакансии"""
        if not isinstance(title, str):
            raise ValueError("Название вакансии должно быть строкой")
        if not title.strip():
            raise ValueError("Название вакансии не может быть пустым")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Приватный метод валидации URL вакансии"""
        if not isinstance(url, str):
            raise ValueError("URL должен быть строкой")
        if not url.strip():
            raise ValueError("URL не может быть пустым")
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или https://")
        return url.strip()

    def _validate_salary(
        self, salary: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Приватный метод валидации данных о зарплате"""
        if salary is None:
            return None

        if not isinstance(salary, dict):
            raise ValueError("Данные о зарплате должны быть в формате словаря")

        validated_salary: Dict[str, Any] = {}

        if "from" in salary:
            salary_from = salary["from"]
            if salary_from is not None:
                try:
                    validated_salary["from"] = int(salary_from)
                except (ValueError, TypeError):
                    validated_salary["from"] = 0

        if "to" in salary:
            salary_to = salary["to"]
            if salary_to is not None:
                try:
                    validated_salary["to"] = int(salary_to)
                except (ValueError, TypeError):
                    validated_salary["to"] = 0

        if "currency" in salary:
            currency = salary["currency"]
            validated_salary["currency"] = str(currency) if currency else "RUR"
        else:
            validated_salary["currency"] = "RUR"

        if validated_salary.get("from", 0) == 0 and validated_salary.get("to", 0) == 0:
            return None

        return validated_salary

    def __str__(self) -> str:
        """Строковое представление вакансии в читаемом формате"""
        salary_info = "Зарплата не указана"
        if self._salary:
            from_salary = self._salary.get("from")
            to_salary = self._salary.get("to")
            currency = self._salary.get("currency", "RUR")

            if from_salary and to_salary:
                salary_info = f"{from_salary:,} - {to_salary:,} {currency}"
            elif from_salary:
                salary_info = f"от {from_salary:,} {currency}"
            elif to_salary:
                salary_info = f"до {to_salary:,} {currency}"

        return (
            f"Вакансия: {self._title}\n"
            f"Зарплата: {salary_info}\n"
            f"Ссылка: {self._url}\n"
            f"Требования: {self._requirements[:100]}...\n"
            f"{'-' * 50}"
        )

    def __repr__(self) -> str:
        return f"Vacancy(title='{self._title}', salary={self._salary})"

    # Методы сравнения по зарплате
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List[Vacancy]:
        """
        Преобразование JSON-данных из API в список объектов Vacancy

        Args:
            vacancies_data: Список словарей с данными вакансий

        Returns:
            Список объектов Vacancy
        """
        vacancies: List[Vacancy] = []

        for vacancy_data in vacancies_data:
            try:
                title = vacancy_data.get("name", "")
                url = vacancy_data.get("alternate_url", "")

                salary_data = vacancy_data.get("salary")
                if salary_data:
                    salary = {
                        "from": salary_data.get("from"),
                        "to": salary_data.get("to"),
                        "currency": salary_data.get("currency", "RUR"),
                    }
                else:
                    salary = None

                snippet = vacancy_data.get("snippet", {})
                description = snippet.get("responsibility", "")
                requirements = snippet.get("requirement", "")

                vacancy = cls(
                    title=title,
                    url=url,
                    salary=salary,
                    description=description,
                    requirements=requirements,
                )

                vacancies.append(vacancy)

            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта вакансии в словарь для сохранения"""
        return {
            "title": self._title,
            "url": self._url,
            "salary": self._salary,
            "description": self._description,
            "requirements": self._requirements,
            "avg_salary": self.avg_salary,
        }
