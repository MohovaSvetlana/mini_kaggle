import shutil
import os


class FileHandler:

    @staticmethod
    def check_file(path):
        return path and os.path.exists(path)

    @staticmethod
    def find_n(path, file_name):
        n = 0
        if os.path.exists(os.path.join(path, f"{file_name}.csv")):
            n = 1
            while os.path.exists(os.path.join(path, f"{file_name} ({n}).csv")):
                n += 1
        return n

    def download_competition_file(self, file_name, id_competition):
        downloads_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
        n = self.find_n(downloads_path, f"{file_name}{id_competition}")
        file_path = os.path.join(os.getcwd(), "db", "competitions", str(id_competition), f"{file_name}.csv")
        shutil.copy(file_path, downloads_path)
        shutil.move(f"{downloads_path}/{file_name}.csv",
                    f"{downloads_path}/{file_name}{id_competition}" + (f" ({n}).csv" if n else ".csv"))

    @staticmethod
    def create_competition_files_folder(id_competition, train_file, test_file, solution_file):
        dst = os.path.join(os.getcwd(), "db", "competitions", str(id_competition))
        os.mkdir(dst)
        shutil.copy(train_file, dst)
        shutil.move(f"{dst}/{os.path.split(train_file)[-1]}", f"{dst}/train.csv")
        shutil.copy(test_file, dst)
        shutil.move(f"{dst}/{os.path.split(test_file)[-1]}", f"{dst}/test.csv")
        shutil.copy(solution_file, dst)
        shutil.move(f"{dst}/{os.path.split(solution_file)[-1]}", f"{dst}/solution.csv")
