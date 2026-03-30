import pytest
from pathlib import Path
from process_drop import collect_audio_files, parse_recorded_time, classify_entry, AUDIO_EXTENSIONS


# --- parse_recorded_time ---

@pytest.mark.parametrize("stem, expected", [
    ("250329_1430", "14:30"),
    ("000101_0000", "00:00"),
    ("991231_2359", "23:59"),
])
def test_parse_recorded_time_valid(stem, expected):
    assert parse_recorded_time(stem) == expected


@pytest.mark.parametrize("stem", [
    "recording",
    "250329",
    "250329_14300",     # too long (hour overflows)
    "25-03-29_14:30",
    "",
])
def test_parse_recorded_time_invalid(stem):
    assert parse_recorded_time(stem) is None


# --- classify_entry ---

def test_classify_task():
    assert classify_entry("task buy milk") == ("task", "buy milk")

def test_classify_task_punctuation():
    assert classify_entry("Task. buy milk") == ("task", "buy milk")

def test_classify_note():
    assert classify_entry("note remember to call Alice") == ("note", "remember to call Alice")

def test_classify_continue():
    assert classify_entry("continue and also pick up bread") == ("continue", "and also pick up bread")

def test_classify_plain_note():
    assert classify_entry("just a plain sentence") == ("note", "just a plain sentence")

def test_classify_single_keyword_only():
    # "task" with no body → body should be empty string
    assert classify_entry("task") == ("task", "")

def test_classify_single_word_non_keyword():
    assert classify_entry("hello") == ("note", "hello")


# --- collect_audio_files ---

def test_collect_audio_files(tmp_path):
    for name in ["a.mp3", "b.wav", "c.txt", "d.MP3", "e.flac"]:
        (tmp_path / name).touch()
    result = collect_audio_files(tmp_path)
    names = [f.name for f in result]
    assert "a.mp3" in names
    assert "b.wav" in names
    assert "d.MP3" in names
    assert "e.flac" in names
    assert "c.txt" not in names

def test_collect_audio_files_sorted(tmp_path):
    for name in ["c.mp3", "a.mp3", "b.mp3"]:
        (tmp_path / name).touch()
    result = collect_audio_files(tmp_path)
    assert [f.name for f in result] == ["a.mp3", "b.mp3", "c.mp3"]

def test_collect_audio_files_empty(tmp_path):
    assert collect_audio_files(tmp_path) == []
