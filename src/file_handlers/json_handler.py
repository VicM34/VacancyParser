import json
import os
from typing import Any, Dict, List, Optional

from src.abstract_classes import FileHandler
from src.vacancy import Vacancy


class JSONSaver(FileHandler):
    """РљР»Р°СЃСЃ РґР»СЏ СЃРѕС…СЂР°РЅРµРЅРёСЏ РІР°РєР°РЅСЃРёР№ РІ JSON-С„Р°Р№Р»"""

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        self._filename = filename
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """РЎРѕР·РґР°РЅРёРµ РґРёСЂРµРєС‚РѕСЂРёРё РґР»СЏ С„Р°Р№Р»Р°, РµСЃР»Рё РѕРЅР° РЅРµ СЃСѓС‰РµСЃС‚РІСѓРµС‚"""
        directory = os.path.dirname(self._filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """РџСЂРёРІР°С‚РЅС‹Р№ РјРµС‚РѕРґ Р·Р°РіСЂСѓР·РєРё РІР°РєР°РЅСЃРёР№ РёР· JSON-С„Р°Р№Р»Р°"""
        try:
            if os.path.exists(self._filename):
                with open(self._filename, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"РћС€РёР±РєР° РїСЂРё Р·Р°РіСЂСѓР·РєРµ JSON-С„Р°Р№Р»Р°: {e}")
        return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """РџСЂРёРІР°С‚РЅС‹Р№ РјРµС‚РѕРґ СЃРѕС…СЂР°РЅРµРЅРёСЏ РІР°РєР°РЅСЃРёР№ РІ JSON-С„Р°Р№Р»"""
        try:
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"РћС€РёР±РєР° РїСЂРё СЃРѕС…СЂР°РЅРµРЅРёРё JSON-С„Р°Р№Р»Р°: {e}")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Р”РѕР±Р°РІР»РµРЅРёРµ РѕРґРЅРѕР№ РІР°РєР°РЅСЃРёРё РІ JSON-С„Р°Р№Р»"""
        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()

        # РџСЂРѕРІРµСЂСЏРµРј, РЅРµС‚ Р»Рё СѓР¶Рµ С‚Р°РєРѕР№ РІР°РєР°РЅСЃРёРё (РїРѕ URL)
        if not any(v.get("url") == vacancy.url for v in vacancies):
            vacancies.append(vacancy_dict)
            self._save_vacancies(vacancies)

    def get_vacancies(
        self, criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """РџРѕР»СѓС‡РµРЅРёРµ РІР°РєР°РЅСЃРёР№ РёР· JSON-С„Р°Р№Р»Р° РїРѕ РєСЂРёС‚РµСЂРёСЏРј"""
        vacancies = self._load_vacancies()

        if not criteria:
            return vacancies

        filtered_vacancies: List[Dict[str, Any]] = []

        for vacancy in vacancies:
            match = True

            if "keyword" in criteria and criteria["keyword"]:
                keyword = criteria["keyword"].lower()
                title = (vacancy.get("title") or "").lower()
                description = (vacancy.get("description") or "").lower()
                requirements = (vacancy.get("requirements") or "").lower()

                if (
                    keyword not in title
                    and keyword not in description
                    and keyword not in requirements
                ):
                    match = False

            if "salary_range" in criteria:
                salary_range = criteria["salary_range"]
                min_salary = salary_range.get("min", 0)
                avg_salary = vacancy.get("avg_salary", 0)

                if avg_salary < min_salary:
                    match = False

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """РЈРґР°Р»РµРЅРёРµ РІР°РєР°РЅСЃРёРё РёР· JSON-С„Р°Р№Р»Р°"""
        vacancies = self._load_vacancies()
        vacancies = [v for v in vacancies if v.get("url") != vacancy.url]
        self._save_vacancies(vacancies)

    def clear_all(self) -> None:
        """РћС‡РёСЃС‚РєР° РІСЃРµС… РІР°РєР°РЅСЃРёР№ РёР· JSON-С„Р°Р№Р»Р°"""
        self._save_vacancies([])
