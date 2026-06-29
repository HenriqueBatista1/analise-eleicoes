import zipfile
from pathlib import Path

import pytest

from extractors import tse as tse_extractor


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def raise_for_status(self):
        return None

    def iter_content(self, chunk_size: int):
        yield self.payload


def _write_zip_archive(path: Path, target_filename: str, content: str) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(target_filename, content)


def test_download_and_extract_tse_extracts_target_file(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    target_filename = "votacao_candidato_munzona_2018_BR.csv"
    zip_path = tmp_path / "archive.zip"
    _write_zip_archive(zip_path, target_filename, "NR_TURNO;QT_VOTOS_NOMINAIS\n1;100\n")

    class FakeGet:
        def __call__(self, url, stream=True):
            return FakeResponse(zip_path.read_bytes())

    monkeypatch.setattr(tse_extractor, "RAW_DATA_DIR", str(raw_dir))
    monkeypatch.setattr(tse_extractor.requests, "get", FakeGet())

    tse_extractor.download_and_extract_tse("https://example.com/archive.zip", target_filename)

    extracted_path = raw_dir / target_filename
    assert extracted_path.exists()
    assert extracted_path.read_text(encoding="utf-8") == "NR_TURNO;QT_VOTOS_NOMINAIS\n1;100\n"


def test_extract_presidency_data_calls_download_for_both_years(monkeypatch):
    calls = []

    def fake_download(url, target_filename):
        calls.append((url, target_filename))

    monkeypatch.setattr(tse_extractor, "download_and_extract_tse", fake_download)

    count = tse_extractor.extract_presidency_data()

    assert count == 2
    assert [target for _, target in calls] == [
        tse_extractor.TARGET_CSV_PRESIDENCY_2018,
        tse_extractor.TARGET_CSV_PRESIDENCY_2022,
    ]
