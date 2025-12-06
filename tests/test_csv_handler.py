import os
import tempfile

import pytest

from src.file_handlers.csv_handler import CSVSaver
from src.vacancy import Vacancy


class TestCSVSaver:
    """Тесты для класса CSVSaver"""

    @pytest.fixture
    def temp_file(self):
        """Создание временного файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
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
        saver = CSVSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0]["title"] == "Python Developer"

    def test_filter_vacancies(self, temp_file, sample_vacancy):
        """Тест фильтрации вакансий"""
        saver = CSVSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        # Фильтрация по ключевому слову в названии
        filtered = saver.get_vacancies({"keyword": "python"})
        assert len(filtered) == 1
        assert filtered[0]["title"] == "Python Developer"

        # Фильтрация по ключевому слову в описании
        filtered = saver.get_vacancies({"keyword": "разработка"})
        assert len(filtered) == 1

        # Фильтрация по ключевому слову в требованиях
        filtered = saver.get_vacancies({"keyword": "опыт"})
        assert len(filtered) == 1

        # Фильтрация по несуществующему ключевому слову
        filtered = saver.get_vacancies({"keyword": "java"})
        assert len(filtered) == 0

        # Фильтрация по зарплате
        filtered = saver.get_vacancies({"salary_range": {"min": 50000}})
        assert len(filtered) == 1

        filtered = saver.get_vacancies({"salary_range": {"min": 200000}})
        assert len(filtered) == 0

    def test_add_duplicate_vacancy(self, temp_file, sample_vacancy):
        """Тест добавления дубликата"""
        saver = CSVSaver(temp_file)
        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(sample_vacancy)  # Добавляем ту же вакансию

        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1  # Дубликат не должен добавляться

    def test_clear_all(self, temp_file, sample_vacancy):
        """Тест очистки всех вакансий"""
        saver = CSVSaver(temp_file)
        saver.add_vacancy(sample_vacancy)

        saver.clear_all()
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 0

    def test_delete_vacancy(self, temp_file, sample_vacancy):
        """Тест удаления вакансии"""
        saver = CSVSaver(temp_file)

        saver.add_vacancy(sample_vacancy)

        vacancies_before = saver.get_vacancies()
        print("\n=== DEBUG ТЕСТ УДАЛЕНИЯ ===")  # Убрал f
        print(f"1. После добавления вакансий: {len(vacancies_before)}")  # Оставить f

        if vacancies_before:
            print("   Первая вакансия в файле:")  # Убрал f
            print(f"   - URL: '{vacancies_before[0].get('url')}'")  # Оставить f
            print(f"   - Title: '{vacancies_before[0].get('title')}'")  # Оставить f
            print(f"   - Тип URL: {type(vacancies_before[0].get('url'))}")  # Оставить f

        print("2. URL из sample_vacancy:")  # Убрал f
        print(f"   - URL: '{sample_vacancy.url}'")  # Оставить f
        print(f"   - Тип URL: {type(sample_vacancy.url)}")  # Оставить f

        assert len(vacancies_before) == 1

        print("3. Вызываем delete_vacancy...")  # Убрал f
        saver.delete_vacancy(sample_vacancy)

        vacancies_after = saver.get_vacancies()
        print(f"4. После удаления вакансий: {len(vacancies_after)}")  # Оставить f

        if vacancies_after:
            print("   Оставшиеся вакансии:")  # Убрал f
            for i, v in enumerate(vacancies_after):
                print(f"   {i + 1}. URL: '{v.get('url')}'")  # Оставить f

        assert len(vacancies_after) == 0
        print("=== КОНЕЦ DEBUG ===\n")
