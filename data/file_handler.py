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

    def download_submission_file(self, submission_id):
        downloads_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
        n = self.find_n(downloads_path, f"submission{submission_id}")
        file_path = os.path.join(os.getcwd(), "db", "submissions", f"submission{submission_id}.csv")
        shutil.copy(file_path, f"{downloads_path}/submission{submission_id}" + (f" ({n})" if n else "") + ".csv")

    def download_competition_file(self, file_name, id_competition):
        downloads_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
        n = self.find_n(downloads_path, f"{file_name}{id_competition}")
        file_path = os.path.join(os.getcwd(), "db", "competitions", str(id_competition), f"{file_name}.csv")
        shutil.copy(file_path, f"{downloads_path}/{file_name}{id_competition}" + (f" ({n})" if n else "") + ".csv")

    @staticmethod
    def create_competition_files_folder(id_competition, train_file, test_file, solution_file):
        dst = os.path.join(os.getcwd(), "db", "competitions", str(id_competition))
        os.mkdir(dst)
        shutil.copy(train_file, f"{dst}/train.csv")
        shutil.copy(test_file, f"{dst}/test.csv")
        shutil.copy(solution_file, f"{dst}/solution.csv")

    @staticmethod
    def create_submission_file(id_submission, submission_file):
        dst = os.path.join(os.getcwd(), "db", "submissions")
        shutil.copy(submission_file, f"{dst}/submission{id_submission}.csv")
