from src.vacancies_collector import HeadHunterAPI, SuperJobAPI
from src.functions import PreparedData
from src.vacancy import Filters
from src.vacancy import Vacancy
from src.save_data import SaveToJSON, SaveToExcel


def get_data(keyword: str):
    hh_api = HeadHunterAPI(keyword)
    sj_api = SuperJobAPI(keyword)
    hh_vacancies = hh_api.get_vacancies()
    sj_vacancies = sj_api.get_vacancies()
    data_prep = PreparedData(hh_vacancies, sj_vacancies)
    data_prep.get_prepared_data_hh()
    data_prep.get_prepared_data_sj()
    return PreparedData.all_data


def set_filters():
    """
    Функция, взаимодействующая с пользователем.
    Получает данные, по которым будет осуществлена фильтрация.
    :return: Объект класса Filters
    """
    print("Укажите фильтр или нажмите Enter")
    name_filter = input("Уточняющие слова для названия профессии: ")
    area_filter = input("Город: ")
    salary = (input("Желаемая зарплата(): ")).split('-')
    salary_filter = [0, 0] if salary == [''] else [int(i) for i in salary]
    experience_filter = input("Поиск вакансий без требований к опыту работы?(yes): ")
    return Filters(name_filter, area_filter, salary_filter, experience_filter)


def main_part():
    """
    Основная часть программы. Собирает все классы и функции
    """
    # platforms = ["HeadHunter", "SuperJob"]
    keyword = input("Введите поисковый запрос: ")
    vacancies_data = get_data(keyword)

    ask_about_filters = input("Установить фильтры?(yes/no): ")
    if ask_about_filters.lower() == "yes":
        while ask_about_filters.lower() == "yes":
            filt = set_filters()
            for i in vacancies_data:
                vacancy = Vacancy(**i)
                if filt.check_experience(vacancy.experience) and \
                        filt.check_area(vacancy.area) and \
                        filt.check_name(vacancy.profession) and \
                        filt.check_salary(vacancy.salary):
                    vacancy.append_data()
            if len(Vacancy.all_vacancies) == 0:
                print("Нет вакансий, соответствующих заданным критериям")
            else:
                filtered_vacancies = Vacancy.all_vacancies
                print(filtered_vacancies)
                SaveToJSON(filtered_vacancies).save_data()
                SaveToExcel(filtered_vacancies, keyword).save_data()
                print("Вакансии сохранены в файл 'src/results.xlsx' ")
            ask_about_filters = input("Начать поиск по другим фильтрам?(yes/no): ")
    else:
        SaveToJSON(vacancies_data).save_data()
        SaveToExcel(vacancies_data, keyword).save_data()
        print("Вакансии сохранены в файл 'src/results.xlsx' ")


if __name__ == "__main__":
    main_part()
