import os
import tempfile

import pytest

from src.file_handlers.json_handler import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    @pytest.fixture
    def temp_file(self):
        """Создание временного файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("[]")
            temp_filename = f.name

        yield temp_filename

        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

    @pytest.fixture
    def sample_vacancy(self):
        """Создание тестовой вакансии"""
        return Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python",
            requirements="Опыт работы с Python",
        )

    def test_add_vacancy(self, temp_file, sample_vacancy):
        """Тест добавления вакансии"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0]["title"] == "Python Developer"
        assert vacancies[0]["url"] == "https://hh.ru/vacancy/123"

    def test_add_vacancies(self, temp_file):
        """Тест добавления списка вакансий"""
        saver = JSONSaver(temp_file)

        vacancies_list = [
            Vacancy("Python 1", "https://hh.ru/1", {"from": 100000}, "Desc1", "Req1"),
            Vacancy("Python 2", "https://hh.ru/2", {"from": 150000}, "Desc2", "Req2"),
        ]

        # Метод add_vacancies не реализован, добавляем по одной
        for vacancy in vacancies_list:
            saver.add_vacancy(vacancy)

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 2
        assert vacancies[0]["title"] == "Python 1"
        assert vacancies[1]["title"] == "Python 2"

    def test_add_duplicate_vacancy(self, temp_file, sample_vacancy):
        """Тест добавления дубликата"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(sample_vacancy)  # Добавляем ту же вакансию

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1  # Дубликат не должен добавляться

    def test_delete_vacancy(self, temp_file, sample_vacancy):
        """Тест удаления вакансии"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1

        saver.delete_vacancy(sample_vacancy)
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 0

    def test_clear_all(self, temp_file, sample_vacancy):
        """Тест очистки всех вакансий"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        saver.clear_all()
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 0

    def test_get_vacancies_with_criteria(self, temp_file, sample_vacancy):
        """Тест получения вакансий по критериям"""
        saver = JSONSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        # Фильтрация по ключевому слову
        filtered = saver.get_vacancies({"keyword": "python"})
        assert len(filtered) == 1

        filtered = saver.get_vacancies({"keyword": "java"})
        assert len(filtered) == 0

        # Фильтрация по зарплате
        filtered = saver.get_vacancies({"salary_range": {"min": 50000}})
        assert len(filtered) == 1

        filtered = saver.get_vacancies({"salary_range": {"min": 200000}})
        assert len(filtered) == 0
