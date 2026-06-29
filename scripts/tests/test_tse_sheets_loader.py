import pandas as pd
from gspread.exceptions import WorksheetNotFound

from loaders.tse_sheets import (
    save_candidate_votes_by_round_to_sheets,
    save_round_comparison_to_sheets,
    save_state_vote_distribution_by_round_to_sheets,
)


class FakeWorksheet:
    def __init__(self, title):
        self.title = title
        self.cleared = False
        self.resized_to = None
        self.update_call = None

    def clear(self):
        self.cleared = True

    def resize(self, rows, cols):
        self.resized_to = (rows, cols)

    def update(self, range_name, values, value_input_option):
        self.update_call = {
            "range_name": range_name,
            "values": values,
            "value_input_option": value_input_option,
        }


class FakeSpreadsheet:
    def __init__(self, existing_titles=()):
        self.tabs = {title: FakeWorksheet(title) for title in existing_titles}
        self.added_titles = []

    def worksheet(self, title):
        if title not in self.tabs:
            raise WorksheetNotFound(title)
        return self.tabs[title]

    def add_worksheet(self, title, rows, cols):
        worksheet = FakeWorksheet(title)
        self.tabs[title] = worksheet
        self.added_titles.append(title)
        return worksheet


def test_save_candidate_votes_writes_expected_tab():
    spreadsheet = FakeSpreadsheet()
    df = pd.DataFrame(
        {
            "NM_URNA_CANDIDATO": ["Lula", "Bolsonaro"],
            "QT_VOTOS_NOMINAIS": [100, 80],
        }
    )

    title = save_candidate_votes_by_round_to_sheets(
        spreadsheet, df, year=2018, turno=1
    )

    assert title == "proc_tse_2018_votes_t1"
    assert title in spreadsheet.tabs

    worksheet = spreadsheet.tabs[title]
    assert worksheet.update_call["value_input_option"] == "RAW"
    assert worksheet.update_call["values"][0] == ["NM_URNA_CANDIDATO", "QT_VOTOS_NOMINAIS"]
    assert worksheet.update_call["values"][1][0] == "Lula"


def test_save_state_distribution_writes_expected_tab():
    spreadsheet = FakeSpreadsheet()
    df = pd.DataFrame(
        {
            "SG_UF": ["SP", "RJ"],
            "NM_URNA_CANDIDATO": ["Lula", "Lula"],
            "QT_VOTOS_NOMINAIS": [100, 80],
        }
    )

    title = save_state_vote_distribution_by_round_to_sheets(
        spreadsheet, df, year=2022, turno=2
    )

    assert title == "proc_tse_2022_state_dist_t2"
    assert title in spreadsheet.tabs


def test_save_round_comparison_writes_expected_tab():
    spreadsheet = FakeSpreadsheet()
    df = pd.DataFrame(
        {
            "NM_URNA_CANDIDATO": ["Lula", "Bolsonaro"],
            "NR_TURNO": [1, 2],
            "QT_VOTOS_NOMINAIS": [100, 90],
        }
    )

    title = save_round_comparison_to_sheets(spreadsheet, df, year=2018)

    assert title == "proc_tse_2018_comparison"
    assert title in spreadsheet.tabs
