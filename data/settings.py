from enum import Enum

# minimum window size
W, H = 600, 400


class Pages(Enum):
    log_in_page = 1
    registration_page = 2
    competitions_list_page = 3
    create_competition_page = 4
    overview_competition_page = 5
    send_submission_page = 6
    all_submissions_page = 7
    leaderboard_page = 8
    results_page = 9
