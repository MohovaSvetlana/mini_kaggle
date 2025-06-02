import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

from data.file_handler import FileHandler


class OverviewData:

    @staticmethod
    def get_columns_data(competition_id):
        file_path = FileHandler.get_competition_train_file_path(competition_id)
        data = pd.read_csv(file_path)
        return data.columns.tolist()

    @staticmethod
    def get_head_data(competition_id):
        file_path = FileHandler.get_competition_train_file_path(competition_id)
        data_head = pd.read_csv(file_path).head()
        return [data_head.columns.tolist()] + data_head.values.tolist()

    @staticmethod
    def get_described_data(competition_id):
        file_path = FileHandler.get_competition_train_file_path(competition_id)
        described_data = pd.read_csv(file_path).describe()
        table_data = [[' '] + described_data.columns.tolist()]
        table_data += [[index] + row.tolist() for index, row in described_data.iterrows()]
        return table_data

    @staticmethod
    def get_data_size(competition_id):
        file_path = FileHandler.get_competition_train_file_path(competition_id)
        return pd.read_csv(file_path).shape

    @staticmethod
    def generate_plot(func):

        def wrapped_func(competition_id, *args, **kwargs):
            file_path = FileHandler.get_competition_train_file_path(competition_id)
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
        plt.xticks(rotation=75)
        data = pd.read_csv(file_path, index_col=index_col)[columns]
        continuous_columns = [col for col in columns if data[col].dtype != "object"]
        if continuous_columns:
            data = pd.read_csv(file_path, index_col=index_col)[continuous_columns]
            plot = sns.lineplot(data=data)
            plot.get_legend().set_bbox_to_anchor((1.01, 1))

    @staticmethod
    @generate_plot
    def scatterplot(file_path, x, y, hue):
        plt.xticks(rotation=75)
        data = pd.read_csv(file_path)
        if hue:
            plot = sns.scatterplot(data=data, x=x, y=y, hue=hue)
            plot.get_legend().set_bbox_to_anchor((1.01, 1))
        else:
            sns.scatterplot(data=data, x=x, y=y)

    @staticmethod
    @generate_plot
    def reg_plot(file_path, x, y, hue):
        data = pd.read_csv(file_path)
        if hue:
            if data[hue].nunique() <= 10:
                plot = sns.lmplot(data=data, x=x, y=y, hue=hue)
                plot._legend.remove()
            else:
                sns.scatterplot(data=data, x=x, y=y, hue=hue)
            plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
        else:
            sns.regplot(data=data, x=x, y=y)

    @staticmethod
    @generate_plot
    def bar_chart(file_path, x, y):
        plt.xticks(rotation=75)
        data = pd.read_csv(file_path)
        if data[x].nunique() <= 15:
            sns.barplot(x=data[x], y=data[y], ci=95)
        else:
            sns.barplot(x=data[x][:15], y=data[y], ci=95)

    @staticmethod
    @generate_plot
    def heatmaps(file_path, val, index, annot):
        data = pd.read_csv(file_path, index_col=index)
        if all(data[el].dtype != "object" for el in val):
            sns.heatmap(data=data[val][:15], annot=annot)

    @staticmethod
    @generate_plot
    def histogram(file_path, val, hue):
        plt.xticks(rotation=75)
        data = pd.read_csv(file_path)
        if hue and data[hue].nunique() <= 10:
            plot = sns.histplot(data=data, x=val, hue=hue)
            plot.get_legend().set_bbox_to_anchor((1.01, 1))
        else:
            sns.histplot(data=data, x=val)

    @staticmethod
    @generate_plot
    def density_plot(file_path, val, hue):
        data = pd.read_csv(file_path)
        if data[val].dtype != "object":
            if hue and data[hue].nunique() <= 10:
                sns.kdeplot(data=data, x=val, hue=hue, fill=True)
            else:
                sns.kdeplot(data=data, x=val, fill=True)

    @staticmethod
    @generate_plot
    def categorical_scatterplot(file_path, x, y):
        plt.xticks(rotation=75)
        data = pd.read_csv(file_path)
        sns.swarmplot(data=data, x=data[x], y=data[y])

    @staticmethod
    @generate_plot
    def histogram_and_density_plot(file_path, val, hue):
        data = pd.read_csv(file_path)
        if data[val].dtype != "object":
            fig, ax = plt.subplots()
            if hue and data[hue].nunique() <= 10:
                sns.kdeplot(data=data, x=val, hue=hue, fill=True, ax=ax)
                ax2 = ax.twinx()
                plot = sns.histplot(data=data, x=val, hue=hue, ax=ax2)
                plot.get_legend().remove()
            else:
                sns.kdeplot(data=data, x=val, fill=True, ax=ax)
                ax2 = ax.twinx()
                sns.histplot(data=data, x=val, ax=ax2)
