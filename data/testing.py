import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score, recall_score
from threading import Thread

from database import DataBase
import os


class TestingSolutions(Thread):

    def __init__(self):
        super().__init__()
        self.metrics = [
            mean_absolute_error,
            mean_squared_error,
            accuracy_score,
            lambda sol_y, sub_y: recall_score(sol_y, sub_y, average='macro', zero_division=0)
        ]

    def run(self):
        for submission in DataBase.get_unchecked_submissions():
            competition = DataBase.get_competition_by_id(submission.competition)
            metric = self.metrics[competition.metric - 1]
            DataBase.set_score_to_submission(submission, self.test_submission(metric, submission.id, competition.id))

    def test_submission(self, metric, submission_id, competition_id):
        try:
            solution_path = os.path.join('db', 'competitions', str(competition_id), 'solution.csv')
            solution_data = pd.read_csv(solution_path)
            submission_path = os.path.join('db', 'submissions', f'submission{submission_id}.csv')
            submission_data = pd.read_csv(submission_path)
            y = solution_data.columns[-1]
            solution_y = solution_data[y]
            submission_y = submission_data[y]
            n = len(solution_y)

            return (metric(solution_y[:n // 2], submission_y[:n // 2]),
                    metric(solution_y[(n + 1) // 2:], submission_y[(n + 1) // 2:]))
        except:
            return None, None
