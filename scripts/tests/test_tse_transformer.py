import pandas as pd

from transformers import tse as tse_transformer


def test_select_interest_columns_keeps_ordered_subset():
    frame = pd.DataFrame(
        {
            "NR_TURNO": [1],
            "SG_UF": ["SP"],
            "NM_URNA_CANDIDATO": ["Lula"],
            "SG_PARTIDO": ["PT"],
            "NM_PARTIDO": ["Partido dos Trabalhadores"],
            "QT_VOTOS_NOMINAIS": [100],
            "DS_SIT_TOT_TURNO": ["Eleito"],
            "extra": ["ignored"],
        }
    )

    result = tse_transformer.select_interest_columns(frame)

    assert list(result.columns) == tse_transformer.INTEREST_COLUMNS_PRESIDENCY
    assert result.iloc[0]["NM_URNA_CANDIDATO"] == "Lula"


def test_clean_presidency_data_removes_nulls_and_duplicates(tmp_path, monkeypatch):
    monkeypatch.setattr(tse_transformer, "PARSED_TSE_DIR", str(tmp_path))

    frame = pd.DataFrame(
        {
            "NR_TURNO": [1, 1, 2],
            "SG_UF": ["SP", "SP", "RJ"],
            "NM_URNA_CANDIDATO": ["Lula", "Lula", "Bolsonaro"],
            "QT_VOTOS_NOMINAIS": [100, 100, 80],
        }
    )

    cleaned = tse_transformer.clean_presidency_data(frame)

    assert len(cleaned) == 2
    assert cleaned["QT_VOTOS_NOMINAIS"].dtype.kind in {"i", "u"}


def test_save_presidency_data_writes_csv(tmp_path, monkeypatch):
    monkeypatch.setattr(tse_transformer, "PARSED_TSE_DIR", str(tmp_path))

    frame = pd.DataFrame({"NR_TURNO": [1], "SG_UF": ["SP"], "NM_URNA_CANDIDATO": ["Lula"], "QT_VOTOS_NOMINAIS": [100]})

    success = tse_transformer.save_presidency_data(frame, year=2018, format="csv")

    output_path = tmp_path / "parsed_presidencia_2018.csv"
    assert success is True
    assert output_path.exists()


def test_clean_voter_profile_data_casts_vote_count_to_int(tmp_path, monkeypatch):
    monkeypatch.setattr(tse_transformer, "PARSED_TSE_DIR", str(tmp_path))

    frame = pd.DataFrame(
        {
            "SG_UF": ["SP", "RJ"],
            "CD_MUNICIPIO": [1, 2],
            "NR_ZONA": [1, 2],
            "DS_FAIXA_ETARIA": ["18-24", "25-34"],
            "QT_ELEITORES_PERFIL": [10, 20],
        }
    )

    cleaned = tse_transformer.clean_voter_profile_data(frame)

    assert cleaned["QT_ELEITORES_PERFIL"].dtype.kind in {"i", "u"}
    assert cleaned.iloc[0]["QT_ELEITORES_PERFIL"] == 10
