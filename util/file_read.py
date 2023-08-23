import pandas as pd


class FileReader:
    def __init__(self):
        self._a_path = "./csv_data/a_雇用_医療福祉_一人当たり賃金_全国_全産業.csv"
        self._b_path = "./csv_data/b_雇用_医療福祉_一人当たり賃金_全国_大分類.csv"
        self._c_path = "./csv_data/c_雇用_医療福祉_一人当たり賃金_都道府県_全産業.csv"
        self._jp_lat_lon_path = "./csv_data/pref_lat_lon.csv"

        self.df_jp_ind = pd.read_csv(self.a_path, encoding="shift_jis")
        self.df_jp_category = pd.read_csv(self.b_path, encoding="shift_jis")
        self.df_pref_ind = pd.read_csv(self.c_path, encoding="shift_jis")
        self.jp_lat_lon = pd.read_csv(self.jp_lat_lon_path)

    @property
    def a_path(self):
        return self._a_path

    @property
    def b_path(self):
        return self._b_path

    @property
    def c_path(self):
        return self._c_path

    @property
    def jp_lat_lon_path(self):
        return self._jp_lat_lon_path
