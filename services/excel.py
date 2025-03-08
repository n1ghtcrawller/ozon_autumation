import pandas as pd


class ExcelHandler:
    def __init__(self, config):
        self.config = config
        self.df = pd.read_excel(config.excel_path, engine="openpyxl")

    def get_accounts(self):
        return self.df[self.df["Профиль заполнен"] == "Да"].iterrows()

    def update_cookies(self, index, cookies):
        self.df.at[index, "Cookies"] = str(cookies)
        self.df.to_excel(self.config.excel_path, index=False, engine="openpyxl")