from json import JSONDecodeError
from src.vacancies_collector import HeadHunterAPI, SuperJobAPI
from src.functions import PreparedData
from src.vacancy import Filters
from src.vacancy import Vacancy
from src.save_data import SaveToJSON, SaveToExcel


def get_data(keyword: str):
    """
    Получение данных по ключевому слову с различных ресурсов
    и приведение их к единому формату:

    {  "profession": '', "url": '', "city": '',
       "company": '', "schedule": '',
       "experience": '', "salary_min": '',
       "salary_max": ''}

    """
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
    print(f"\nУкажите фильтр или нажмите Enter\n")
    name_filter = input("Уточняющие слова для названия профессии: ")
    area_filter = input("Город: ")
    salary = (input("Желаемая зарплата(Примеры ввода: 1000 или 1000-5000): ")).split('-')
    salary_filter = [0, 0] if salary == [''] else [int(i) for i in salary]
    experience_filter = input("Поиск вакансий без требований к опыту работы?(yes): ")
    return Filters(name_filter, area_filter, salary_filter, experience_filter)


def save_data(user_answer, json_data, excel_data):
    """
    Функция сохраняет данные в пустой файл или дописывает их
    в существующий в зависимости от ответа пользователя.
    """

    if user_answer.lower() == "yes":
        json_data.save_data()
    else:
        try:
            json_data.append_data()
        except JSONDecodeError:
            json_data.save_data()

    json_data.make_final_file()
    all_sorted_data = json_data.all_filtered_data
    excel_data.save_filtered_data(all_sorted_data)


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
                        filt.check_salary(vacancy.salary_min):
                    vacancy.append_data()
            if len(Vacancy.all_vacancies) == 0:
                print("Нет вакансий, соответствующих заданным критериям")
            else:
                filtered_vacancies = Vacancy.all_vacancies
                save_json = SaveToJSON(filtered_vacancies)
                save_excel = SaveToExcel(filtered_vacancies)
                user_answer = input(f"\nОчистить файл перед сохранением? (yes/no) ")
                save_data(user_answer, save_json, save_excel)
                print(f"\n{str(save_json)}\n{str(save_excel)}")
            ask_about_filters = input(f"\nНачать поиск по другим фильтрам?(yes/no): ")
    else:
        save_json = SaveToJSON(vacancies_data)
        save_excel = SaveToExcel(vacancies_data)
        user_answer = input(f"\nОчистить файл перед сохранением? (yes/no) ")
        save_data(user_answer, save_json, save_excel)
        print(f"\n{str(save_json)}\n{str(save_excel)}")


if __name__ == "__main__":
    main_part()
