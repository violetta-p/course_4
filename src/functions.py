class PreparedData:
    """
    Класс предназначен для приведения данных, полученных с разных ресурсов,
    к единому формату и сохранения данных в единый список.
    """

    all_data = []
    items = ("null", [], {}, "", False, "None", None, "NoneType")

    def __init__(self, hh_data, sj_data):
        self.hh_data = hh_data
        self.sj_data = sj_data

    def get_prepared_data_hh(self):
        if self.hh_data is None:
            return None
        vacancies = self.hh_data.get("items", [])
        for vacancy in vacancies:
            area = vacancy.get("area", {}).get("name")
            salary_min = 0 if vacancy.get("salary", {}) in PreparedData.items or type(vacancy.get("salary", {})) == 'NoneType' else vacancy["salary"]["from"]
            salary_max = 0 if vacancy.get("salary", {}) in PreparedData.items or type(vacancy.get("salary", {})) == 'NoneType' else vacancy["salary"]["to"]
            salary = self.convert_salary_from_str_to_int(salary_min, salary_max)
            name = vacancy.get("name", "-")
            vacancy_url = vacancy.get("alternate_url")
            work_experience = "нет опыта" if vacancy.get("experience", {}) in PreparedData.items else vacancy["experience"]["name"]
            working_time = "-" if vacancy.get("working_time_intervals", {}) in PreparedData.items else vacancy["working_time_intervals"][0]["name"]
            company_name = "-" if vacancy.get("employer", {}) in PreparedData.items else vacancy["employer"]["name"]

            vac_info = {
                "profession": name, "url": vacancy_url, "city": area,
                "company": company_name, "schedule": working_time,
                "experience": work_experience, "salary": salary
            }
            PreparedData.all_data.append(vac_info)

    def get_prepared_data_sj(self):
        if self.sj_data is None:
            return None
        vacancies = self.sj_data.get("objects", [])
        for vacancy in vacancies:
            area = vacancy.get("town", {}).get("title")
            salary_min = 0 if vacancy.get("payment_from", {}) in PreparedData.items or type(vacancy.get("payment_from")) == 'NoneType' else vacancy["payment_from"]
            salary_max = 0 if vacancy.get("payment_to", {}) in PreparedData.items or type(vacancy.get("payment_to")) == 'NoneType' else vacancy["payment_to"]
            salary = self.convert_salary_from_str_to_int(salary_min, salary_max)
            name = vacancy.get("profession", "-")
            vacancy_url = vacancy.get("link")
            work_experience = "не имеет значения" if vacancy.get("experience", {}) in PreparedData.items else vacancy["experience"]["title"]
            working_time = "-" if vacancy.get("type_of_work", {}) in PreparedData.items else vacancy["type_of_work"]["title"]
            company_name = "-" if vacancy.get("firm_name", {}) in PreparedData.items else vacancy["firm_name"]
            vac_info = {
                "profession": name, "url": vacancy_url, "city": area,
                "company": company_name, "schedule": working_time,
                "experience": work_experience, "salary": salary
            }
            PreparedData.all_data.append(vac_info)

    @staticmethod
    def convert_salary_from_str_to_int(s_min, s_max):
        salary_min = 0 if type(s_min) == "NoneType" or s_min in PreparedData.items else int(s_min)
        salary_max = 0 if type(s_max) == "NoneType" or s_max in PreparedData.items else int(s_max)
        return [salary_min, salary_max]
