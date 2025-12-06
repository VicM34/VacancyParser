from __future__ import annotations

from src.abstract_classes import FileHandler
from src.api import HeadHunterAPI
from src.file_handlers.csv_handler import CSVSaver
from src.file_handlers.json_handler import JSONSaver
from src.file_handlers.txt_handler import TXTSaver
from src.vacancy import Vacancy


def user_interaction() -> None:
    """
    Основная функция для взаимодействия с пользователем
    """

    print("=" * 60)
    print("СИСТЕМА ПОИСКА ВАКАНСИЙ С HH.RU")
    print("=" * 60)

    # Выбор формата сохранения
    print("\nВыберите формат для сохранения вакансий:")
    print("1. JSON (рекомендуется)")
    print("2. CSV")
    print("3. TXT")

    format_choice = input("\nВведите номер формата (1-3): ").strip()

    # ИСПРАВЛЕНО: правильные типы
    saver: FileHandler  # Объявляем переменную с типом FileHandler

    if format_choice == "1":
        saver = JSONSaver()
        print("Выбран формат: JSON")
    elif format_choice == "2":
        saver = CSVSaver()
        print("Выбран формат: CSV")
    elif format_choice == "3":
        saver = TXTSaver()
        print("Выбран формат: TXT (только для чтения человеком)")
    else:
        print("Неверный выбор, используется JSON по умолчанию")
        saver = JSONSaver()

    # Поиск вакансий
    print("\n" + "-" * 60)
    search_query = input(
        "🔍 Введите поисковый запрос (например: Python разработчик): "
    ).strip()

    if not search_query:
        print("Поисковый запрос не может быть пустым!")
        return

    print(f"\nИщем вакансии по запросу: '{search_query}'...")

    # Создаем экземпляр API
    hh_api = HeadHunterAPI()

    # Получаем вакансии
    vacancies_data = hh_api.get_vacancies(search_query)

    if not vacancies_data:
        print("По вашему запросу вакансий не найдено.")
        return

    # Преобразуем в объекты Vacancy
    vacancies_list = Vacancy.cast_to_object_list(vacancies_data)

    print(f"Найдено {len(vacancies_list)} вакансий.")

    # Сохраняем в выбранный формат
    for vacancy in vacancies_list:
        saver.add_vacancy(vacancy)

    print(f"💾 Вакансии сохранены в файл: {saver._filename}")

    # Работа с сохраненными вакансиями
    while True:
        print("\n" + "=" * 60)
        print("ГЛАВНОЕ МЕНЮ:")
        print("1. Показать все сохраненные вакансии")
        print("2. Найти вакансии по ключевому слову")
        print("3. Отфильтровать вакансии по минимальной зарплате")
        print("4. Очистить все сохраненные вакансии")
        print("5. Выход")

        choice = input("\nВыберите действие (1-5): ").strip()

        if choice == "1":
            # Показать все вакансии
            all_vacancies = saver.get_vacancies()

            if all_vacancies:
                print(f"\nВсе сохраненные вакансии ({len(all_vacancies)}):")
                print("=" * 60)

                for i, vacancy_data in enumerate(all_vacancies, 1):
                    salary_info = "Зарплата не указана"
                    if vacancy_data.get("salary"):
                        salary = vacancy_data["salary"]
                        from_salary = salary.get("from")
                        to_salary = salary.get("to")
                        currency = salary.get("currency", "RUR")

                        if from_salary and to_salary:
                            salary_info = f"{from_salary:,} - {to_salary:,} {currency}"
                        elif from_salary:
                            salary_info = f"от {from_salary:,} {currency}"
                        elif to_salary:
                            salary_info = f"до {to_salary:,} {currency}"

                    print(f"\n{i}. {vacancy_data['title']}")
                    print(f"   Зарплата: {salary_info}")
                    print(f"   Ссылка: {vacancy_data['url']}")
            else:
                print("\nНет сохраненных вакансий.")

        elif choice == "2":
            # Поиск по ключевому слову
            keyword = input("Введите ключевое слово для поиска: ").strip().lower()

            if keyword:
                filtered = saver.get_vacancies({"keyword": keyword})

                if filtered:
                    print(
                        f"\nНайдено {len(filtered)} вакансий с ключевым словом '{keyword}':"
                    )
                    print("=" * 60)

                    for i, vacancy_data in enumerate(filtered, 1):
                        print(f"\n{i}. {vacancy_data['title']}")
                        print(f"   Ссылка: {vacancy_data['url']}")
                        if vacancy_data.get("avg_salary", 0) > 0:
                            print(
                                f"   Средняя зарплата: {vacancy_data['avg_salary']:,}"
                            )
                else:
                    print(f"\nВакансий с ключевым словом '{keyword}' не найдено.")
            else:
                print("Ключевое слово не может быть пустым!")

        elif choice == "3":
            # Фильтрация по зарплате
            try:
                min_salary = int(input("Введите минимальную зарплату: "))

                filtered = saver.get_vacancies({"salary_range": {"min": min_salary}})

                if filtered:
                    print(
                        f"\nНайдено {len(filtered)} вакансий с зарплатой от {min_salary:,}:"
                    )
                    print("=" * 60)

                    for i, vacancy_data in enumerate(filtered, 1):
                        avg_salary = vacancy_data.get("avg_salary", 0)
                        print(f"\n{i}. {vacancy_data['title']}")
                        print(f"   Средняя зарплата: {avg_salary:,}")
                        print(f"   Ссылка: {vacancy_data['url']}")
                else:
                    print(f"\nВакансий с зарплатой от {min_salary:,} не найдено.")

            except ValueError:
                print("Некорректный ввод зарплаты!")

        elif choice == "4":
            # Очистка всех вакансий
            confirm = (
                input("Вы уверены, что хотите удалить все вакансии? (да/нет): ")
                .strip()
                .lower()
            )

            if confirm == "да":
                saver.clear_all()
                print("Все вакансии удалены.")
            else:
                print("Операция отменена.")

        elif choice == "5":
            print("\nВыход из программы. До свидания!")
            break

        else:
            print("Некорректный выбор! Введите число от 1 до 5.")

        input("\nНажмите Enter для продолжения...")
