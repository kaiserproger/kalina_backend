from enum import Enum


class TaskTypeEnum(Enum):
    MultiSelect = "multi_select"
    SingleSelect = "single_select"
    SingleLine = "single_line"
    MultiLine = "multi_line"


class MediaEnum(Enum):
    Audio = "audio/ogg"
    Image = "image/jpeg"
    Form = "application/json"
