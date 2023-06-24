import json
import os
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

    def save_data(self):
        sorted_data = self.sort_filtered_data()
        full_path_to_data = os.path.join(FILE_PATH, FILE_NAME)
        with open(full_path_to_data, "a", encoding='utf-8') as json_file:
            json.dump(sorted_data, json_file, ensure_ascii=False)

    def sort_filtered_data(self) -> list:
        if len(self.data) <= 1:
            return self.data
        return sorted(self.data, key=lambda v: v['salary'][0], reverse=True)


class SaveToExcel(SaveToJSON):
    """
        Класс для сохранения отсортированных по зарплате вакансий в таблицу Excel.
        """
    def __init__(self, data, keyword):
        super().__init__(data)
        self.keyword = keyword

    def save_data(self):
        sheet_list = []
        sorted_data = self.sort_filtered_data()
        full_path_to_data = os.path.join(FILE_PATH, EXCEL_FILE_NAME)
        df = pd.DataFrame(sorted_data)
        # Получает список названий страниц в Excel
        xl = pd.ExcelFile(full_path_to_data)
        sheet_list = list(xl.sheet_names)

        if self.keyword not in sheet_list:
            with pd.ExcelWriter(full_path_to_data, mode='a', engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=self.keyword, index=False)
        else:
            with pd.ExcelWriter(full_path_to_data, mode='a', engine="openpyxl", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name=self.keyword, startrow=writer.sheets[self.keyword].max_row, index=False, header=False)
