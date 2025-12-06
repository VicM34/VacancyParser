from unittest.mock import Mock, patch
from src.api import HeadHunterAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def test_api_initialization(self):
        """Тест инициализации API"""
        api = HeadHunterAPI()
        assert api._base_url == "https://api.hh.ru/vacancies"
        assert "User-Agent" in api._headers
        assert api._params["area"] == 113
        assert api._params["per_page"] == 50  # Теперь совпадает с api.py
        assert (
            api._params["only_with_salary"] is True
        )  # ИСПРАВЛЕНО: is True вместо == True

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "snippet": {
                        "requirement": "Опыт от 3 лет",
                        "responsibility": "Разработка на Python",
                    },
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        assert vacancies[0]["alternate_url"] == "https://hh.ru/vacancy/123"

    @patch("requests.get")
    def test_get_vacancies_empty(self, mock_get):
        """Тест пустого ответа"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Nonexistent")

        assert vacancies == []
