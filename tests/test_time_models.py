import pytest
from pydantic import ValidationError
from src.videotime.models.time_models import (
    TimeInput,
    FileRelativeSeconds,
    MediaTime,
    SmpteTimeNDF,
    SmpteTimeDF,
    create_model_from_time,
)


def test_FRS_model():
    frs = FileRelativeSeconds(time=131.123)
    assert frs.time == 131.123


def test_FRS_model_validation_error():
    with pytest.raises(ValidationError):
        frs = FileRelativeSeconds(time="01:02:03.123")


def test_mediatime():
    mediatime = MediaTime(time="01:02:03.123")

    assert mediatime.time == "01:02:03.123"
    assert type(mediatime.time) == str


def test_mediatime_model_validation_error():
    with pytest.raises(ValidationError):
        mt = MediaTime(time="01:02:03:02")
        mt2 = MediaTime(time="01:02:03;04")
        mt3 = MediaTime(time=123.123)


def test_SMPTE_NDF_model():
    ndf = SmpteTimeNDF(time="01:02:03:04")

    assert type(ndf.time) == str
    assert ndf.time == "01:02:03:04"


def test_SMPTE_NDF_model_validation_error():
    with pytest.raises(ValidationError):
        ndf = SmpteTimeNDF(time="01:02:03;04")
        ndf_2 = SmpteTimeNDF(time="01:02:03.123")
        ndf_3 = SmpteTimeNDF(time=12.123)


def test_SMPTE_DF_model():
    df = SmpteTimeDF(time="01:02:03;04")

    assert type(df.time) == str
    assert df.time == "01:02:03;04"


def test_SMPTE_DF_model_validation_error():
    with pytest.raises(ValidationError):
        df = SmpteTimeDF(time="01:02:03:04")
        df_2 = SmpteTimeDF(time="01:02:03.123")
        df_3 = SmpteTimeDF(time=12.123)


def test_create_time_model_frs():
    model = create_model_from_time(12.123)

    assert isinstance(model, FileRelativeSeconds)


def test_create_time_model_mediatime():
    model = create_model_from_time("01:02:03.123")

    assert isinstance(model, MediaTime)


def test_create_time_model_SMPTE_NDF():
    model = create_model_from_time("01:02:03:04")

    assert isinstance(model, SmpteTimeNDF)


def test_create_time_model_SMPTE_DF():
    model = create_model_from_time("01:02:03;04")

    assert isinstance(model, SmpteTimeDF)


def test_create_time_model_error():
    with pytest.raises(ValueError):
        model = create_model_from_time("1:2:3:4:5")
