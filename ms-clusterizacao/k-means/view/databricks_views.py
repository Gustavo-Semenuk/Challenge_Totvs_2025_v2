import pandas as pd

class ConsoleView:
    @staticmethod
    def display_table(df: pd.DataFrame):
        """Exibe o DataFrame no console"""
        print(df)