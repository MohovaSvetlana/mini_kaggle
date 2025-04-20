import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO


class OverviewData:

    @staticmethod
    def get_file_path(competition_id):
        return os.path.join(os.getcwd(), "db", "competitions", str(competition_id), "train.csv")

    @staticmethod
    def get_columns_data(competition_id):
        file_path = OverviewData.get_file_path(competition_id)
        data = pd.read_csv(file_path)
        return data.columns.tolist()

    @staticmethod
    def get_head_data(competition_id):
        file_path = OverviewData.get_file_path(competition_id)
        data_head = pd.read_csv(file_path).head()
        return [data_head.columns.tolist()] + data_head.values.tolist()

    @staticmethod
    def get_described_data(competition_id):
        file_path = OverviewData.get_file_path(competition_id)
        described_data = pd.read_csv(file_path).describe()
        table_data = [[' '] + described_data.columns.tolist()]
        table_data += [[index] + row.tolist() for index, row in described_data.iterrows()]
        return table_data

    @staticmethod
    def generate_plot(func):

        def wrapped_func(competition_id, *args, **kwargs):
            file_path = OverviewData.get_file_path(competition_id)
            func(file_path, *args, **kwargs)
            buf = BytesIO()
            plt.savefig(buf, bbox_inches='tight')
            buf.seek(0)
            plt.close('all')
            return buf

        return wrapped_func

    @staticmethod
    @generate_plot
    def line_chart(file_path, index_col, columns):
        data = pd.read_csv(file_path, index_col=index_col)[columns]
        sns.lineplot(data=data)

    @staticmethod
    @generate_plot
    def scatterplot(file_path, x, y, hue):
        data = pd.read_csv(file_path)
        if hue:
            sns.scatterplot(data=data, x=x, y=y, hue=hue)
            plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
        else:
            sns.scatterplot(data=data, x=x, y=y)
