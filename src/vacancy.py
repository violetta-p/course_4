class Vacancy:
    """
    Класс создает объекты-вакансии для их дальнейшей фильтрации и
    сохраняет отфильтрованные экземпляры.
    """

    all_vacancies = []

    def __init__(self, **data):
        self.profession: str = data.get('profession')
        self.area: str = data.get('city')
        self.salary: list = data.get('salary')
        self.url: str = data.get('url')
        self.experience: str = data.get('experience')
        self.schedule: str = data.get('schedule')
        self.company_name: str = data.get('company')

    def append_data(self):
        data = {
                "profession": self.profession, "url": self.url, "city": self.area,
                "company": self.company_name, "schedule": self.schedule,
                "experience": self.experience, "salary": self.salary
            }
        Vacancy.all_vacancies.append(data)


class Filters:
    """
    Класс для создания объекта-фильтра на основании данных, введенных пользователем,
    и фильтрации данных путем сравнения атрибутов объекта-фильтра с атрибутами
    объектов-вакансий класса Vacancy.
    """

    def __init__(self, name: str, area: str, salary: list[int], experience):
        self.name = name
        self.area = area
        self.salary = salary
        self.experience = experience

    def check_experience(self, data):
        if self.experience.lower() == "yes":
            if data.lower() == "не имеет значения" or data.lower() == "нет опыта":
                return True
            else:
                return False
        elif self.experience == "":
            return True

    def check_area(self, data):
        if self.area.lower() == data.lower():
            return True
        elif self.area == "":
            return True
        else:
            return False

    def check_name(self, data):
        if self.name.lower() in data.lower():
            return True
        elif self.name == "":
            return True
        else:
            return False

    def check_salary(self, data):
        if data[0] >= self.salary[0]:
            return True
        else:
            return False
