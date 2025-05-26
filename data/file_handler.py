import os


class FileHandler:
    @staticmethod
    def get_competition_directory_path(competition_id):
        return os.path.join(os.getcwd(), "db", "competitions", str(competition_id))

    @staticmethod
    def get_competition_train_file_path(competition_id):
        return os.path.join(FileHandler.get_competition_directory_path(competition_id), "train.csv")

    @staticmethod
    def get_competition_test_file_path(competition_id):
        return os.path.join(FileHandler.get_competition_directory_path(competition_id), "test.csv")

    @staticmethod
    def get_competition_solution_file_path(competition_id):
        return os.path.join(FileHandler.get_competition_directory_path(competition_id), "solution.csv")

    @staticmethod
    def get_competition_submission_file_path(submission_id):
        return os.path.join(os.getcwd(), "db", "submissions", f"submission{submission_id}.csv")

    @staticmethod
    def create_competition_files_folder(competition_id, train_file, test_file, solution_file):
        os.mkdir(FileHandler.get_competition_directory_path(competition_id))
        train_file.save(FileHandler.get_competition_train_file_path(competition_id))
        test_file.save(FileHandler.get_competition_test_file_path(competition_id))
        solution_file.save(FileHandler.get_competition_solution_file_path(competition_id))

    @staticmethod
    def create_submission_file(submission_id, submission_file):
        submission_file.save(FileHandler.get_competition_submission_file_path(submission_id))

    @staticmethod
    def delete_competition_file(competition_id):
        os.remove(FileHandler.get_competition_train_file_path(competition_id))
        os.remove(FileHandler.get_competition_test_file_path(competition_id))
        os.remove(FileHandler.get_competition_solution_file_path(competition_id))
        os.rmdir(FileHandler.get_competition_directory_path(competition_id))

    @staticmethod
    def delete_submission_file(submission_id):
        os.remove(FileHandler.get_competition_submission_file_path(submission_id))
