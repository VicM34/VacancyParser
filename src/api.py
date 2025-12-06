from __future__ import annotations

from typing import Any, Dict, List

import requests

from .abstract_classes import API


class HeadHunterAPI(API):
    """Класс для работы с API HeadHunter (hh.ru)"""

    def __init__(self, per_page: int = 50) -> None:
        """
        Инициализация API
        """
        self._base_url: str = "https://api.hh.ru/vacancies"
        self._headers: Dict[str, str] = {
            "User-Agent": "VacancyParser/1.0",
            "Accept": "application/json",
        }
        self._params: Dict[str, Any] = {
            "area": 113,  # Россия
            "per_page": per_page,  # Теперь 50 как в тесте
            "page": 0,
            "only_with_salary": True,
        }

    def _connect_to_api(self, params: Dict[str, Any]) -> requests.Response:
        """
        Приватный метод для подключения к API hh.ru
        """
        try:
            response = requests.get(
                self._base_url, headers=self._headers, params=params, timeout=10
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Ошибка API: {e}")
            if e.response is not None:
                print(f"Код статуса: {e.response.status_code}")
                print(f"Ответ: {e.response.text[:200]}")
            raise

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий с hh.ru по поисковому запросу
        """
        # Копируем параметры чтобы не менять оригинальные
        params = self._params.copy()
        params["text"] = search_query
        params["page"] = 0

        vacancies: List[Dict[str, Any]] = []
        try:
            print(f"Отправляем запрос: {search_query}")
            response = self._connect_to_api(params)
            data: Dict[str, Any] = response.json()

            print(f"Найдено вакансий: {data.get('found', 0)}")
            print(f"Страниц: {data.get('pages', 0)}")

            vacancies.extend(data.get("items", []))

        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []
        except (KeyError, ValueError) as e:
            print(f"Ошибка обработки данных: {e}")
            return []

        return vacancies
