import json
import os
import openpyxl
import pandas as pd
from pathlib import Path

FILE_PATH = Path(__file__).parent

FILE_NAME = "all_data.json"  # Файл для сохранения данных
EXCEL_FILE_NAME = "results.xlsx"


class SaveToJSON:
    """
    Класс для сохранения отсортированных по зарплате вакансий.
    """

    def __init__(self, data):
        self.data = data
        self.full_path_to_data = os.path.join(FILE_PATH, FILE_NAME)
        self.all_filtered_data = None

    def __str__(self):
        return f"Вакансии сохранены в файл {FILE_NAME}."

    def save_data(self):
        sorted_data = self.sort_filtered_data()
        with open(self.full_path_to_data, "w", encoding='utf-8') as json_file:
            json.dump(sorted_data, json_file, ensure_ascii=False, indent=8)

    def append_data(self):
        sorted_data = self.sort_filtered_data()
        with open(self.full_path_to_data, "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
            data.extend(sorted_data)
            with open(self.full_path_to_data, "w", encoding='utf-8') as output_data:
                json.dump(data, output_data, ensure_ascii=False, indent=8)

    def sort_filtered_data(self) -> list:
        if len(self.data) <= 1:
            return self.data
        return sorted(self.data, key=lambda v: v['salary_min'], reverse=True)

    def make_final_file(self):
        with open(self.full_path_to_data, "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
            sorted_data = sorted(data, key=lambda v: v['salary_min'], reverse=True)
            self.all_filtered_data = sorted_data
            with open(self.full_path_to_data, "w", encoding='utf-8') as final_file:
                json.dump(sorted_data, final_file, ensure_ascii=False, indent=8)


class SaveToExcel(SaveToJSON):
    """
    Класс для сохранения отсортированных по зарплате вакансий в таблицу Excel.
    """
    def __init__(self, data):
        super().__init__(data)
        self.sheet_name = 'search_results'
        self.full_path_to_data = os.path.join(FILE_PATH, EXCEL_FILE_NAME)

    def __str__(self):
        return f"Вакансии сохранены в файл 'results.xlsx'. Лист: {self.sheet_name}"

    def get_sheets_names(self):
        # Получает список названий страниц в Excel
        xl = pd.ExcelFile(self.full_path_to_data)
        return list(xl.sheet_names)

    def delete_data(self):
        sheet_list = self.get_sheets_names()
        if self.sheet_name in sheet_list:
            wb = openpyxl.load_workbook(filename=EXCEL_FILE_NAME)
            wb.create_sheet("MySheet")
            wb.remove(wb[self.sheet_name])
            wb.save(EXCEL_FILE_NAME)

    def save_filtered_data(self, sorted_data):
        self.delete_data()
        df = pd.DataFrame(sorted_data)
        with pd.ExcelWriter(self.full_path_to_data, mode='w', engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=self.sheet_name, index=False)
