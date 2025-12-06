import pytest

from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    def test_vacancy_creation(self):
        """Тест создания вакансии"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python",
            requirements="Опыт от 3 лет",
        )

        assert vacancy.title == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.description == "Разработка на Python"
        assert vacancy.requirements == "Опыт от 3 лет"
        assert vacancy.avg_salary == 125000

    def test_vacancy_no_salary(self):
        """Тест создания вакансии без зарплаты"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary=None,
            description="Разработка",
            requirements="Опыт",
        )

        assert vacancy.salary is None
        assert vacancy.avg_salary == 0

    def test_vacancy_comparison(self):
        """Тест сравнения вакансий"""
        # ИСПРАВЛЕНО: URL должны начинаться с http:// или https://
        v1 = Vacancy(
            "Junior",
            "https://hh.ru/vacancy/1",
            {"from": 50000, "to": 70000, "currency": "RUR"},
            "",
            "",
        )
        v2 = Vacancy(
            "Senior",
            "https://hh.ru/vacancy/2",
            {"from": 150000, "to": 200000, "currency": "RUR"},
            "",
            "",
        )

        assert v2 > v1
        assert v1 < v2
        assert v2 >= v1
        assert v1 <= v2
        assert not v1 == v2

    def test_invalid_title(self):
        """Тест невалидного названия"""
        with pytest.raises(ValueError):
            Vacancy("", "https://hh.ru", None, "", "")

    def test_invalid_url(self):
        """Тест невалидного URL"""
        with pytest.raises(ValueError):
            Vacancy("Test", "invalid", None, "", "")

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        vacancy = Vacancy(
            title="Test",
            url="https://hh.ru/test",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Test description",
            requirements="Test requirements",
        )

        data = vacancy.to_dict()
        assert data["title"] == "Test"
        assert data["url"] == "https://hh.ru/test"
        assert data["avg_salary"] == 125000
        assert data["description"] == "Test description"
        assert data["requirements"] == "Test requirements"
        assert data["salary"]["from"] == 100000
        assert data["salary"]["to"] == 150000

    def test_cast_to_object_list(self):
        """Тест преобразования данных API в объекты Vacancy"""
        api_data = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {
                    "requirement": "Опыт от 3 лет",
                    "responsibility": "Разработка на Python",
                },
            },
            {
                "name": "Java Developer",
                "alternate_url": "https://hh.ru/vacancy/456",
                "salary": None,
                "snippet": {"requirement": "", "responsibility": ""},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(api_data)

        assert len(vacancies) == 2
        assert vacancies[0].title == "Python Developer"
        assert vacancies[0].url == "https://hh.ru/vacancy/123"
        assert vacancies[0].avg_salary == 125000
        assert vacancies[1].title == "Java Developer"
        assert vacancies[1].salary is None
        assert vacancies[1].avg_salary == 0
