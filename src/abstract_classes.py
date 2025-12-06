from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from src.vacancy import Vacancy


class API(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по поисковому запросу
        """
        pass


class FileHandler(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy: "Vacancy") -> None:
        """Добавление вакансии в файл"""
        pass

    @abstractmethod
    def get_vacancies(
        self, criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Получение вакансий по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: "Vacancy") -> None:
        """Удаление вакансии из файла"""
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Очистка всех вакансий из файла"""
        pass
