from pydantic import BaseModel, ValidationError, field_validator
from typing import Any, Union


# File Relative Seconds - 12.183
# Media Time - 01:12:22.246
# SMPTE Time (NDF) - 01:12:22:05
# SMPTE Time (DF) - 01:12:22;05


class TimeInput(BaseModel):
    time: Union[float, str]


class FileRelativeSeconds(BaseModel):
    time: float


class MediaTime(BaseModel):
    time: str

    @field_validator("time", mode="before")
    @classmethod
    def validate_mediatime(cls, value: Any) -> Any:
        if value.count(":") == 2 and value.count(".") == 1:
            return value
        else:
            raise ValueError("Invalid MediaTime, should follow 'HH:MM:SS.msec' format")


class SmpteTimeNDF(BaseModel):
    time: str

    @field_validator("time", mode="before")
    @classmethod
    def validate_SMPTE_NDF(cls, value: Any) -> Any:
        if value.count(":") == 3:
            return value
        else:
            raise ValueError(
                "Invalid SMPTE NonDropFrame format, should follow 'HH:MM:SS:FF' format"
            )


class SmpteTimeDF(BaseModel):
    time: str

    @field_validator("time", mode="before")
    @classmethod
    def validate_SMPTE_NDF(cls, value: Any) -> Any:
        if value.count(":") == 2 and value.count(";") == 1:
            return value
        else:
            raise ValueError(
                "Invalid SMPTE DropFrame format, should follow 'HH:MM:SS;FF' format"
            )


def create_model_from_time(inputTime):
    try:
        return FileRelativeSeconds(time=inputTime)
    except ValidationError:
        pass
    try:
        return MediaTime(time=inputTime)
    except ValidationError:
        pass
    try:
        return SmpteTimeNDF(time=inputTime)
    except ValidationError:
        pass
    try:
        return SmpteTimeDF(time=inputTime)
    except ValidationError:
        pass

    raise ValueError(
        "Time does not match one of the following formats: 12.183, 01:12:22.246, 01:12:22:05, 01:12:22;05"
    )
