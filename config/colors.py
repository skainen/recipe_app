from dataclasses import dataclass
from typing import Type

@dataclass
class ColorScheme:
    PRIMARY: str
    SECONDARY: str
    BURGER: str
    NAV: str
    NAV_ICONS: str
    ACCENT: str
    BACKGROUND: str
    CARD_BG: str
    TEXT_PRIMARY: str
    TEXT_SECONDARY: str
    INPUT_BG: str
    ERROR: str
    WHITE: str
    HOVER: str

class AppColors:
    LIGHT = ColorScheme(
        PRIMARY="#fff5dc",
        SECONDARY="#bcad8c",
        BURGER="#9d3f09",
        NAV="#d7c8a1",
        NAV_ICONS="#ef9d67",
        ACCENT="#b2b07c",
        BACKGROUND="#fff5dc",
        CARD_BG="#9c9892",
        TEXT_PRIMARY="#9d3f09",
        TEXT_SECONDARY="#ef9d67",
        INPUT_BG="#f4f4ce",
        ERROR="#B00020",
        WHITE="#FFFFFF",
        HOVER="#67564a",
    )

    DARK = ColorScheme(
        PRIMARY="#141519",
        SECONDARY="#ecaf6a",
        BURGER="#f7a24c",
        NAV="#4f4a37",
        NAV_ICONS="#ecaf6a",
        ACCENT="#a57846",
        BACKGROUND="#141519",
        CARD_BG="#141519",
        TEXT_PRIMARY="#f1bb7e",
        TEXT_SECONDARY="#eabd8a",
        INPUT_BG="#3b3728",
        ERROR="#CF6679",
        WHITE="#f2efec",
        HOVER="#2c2c2c",
    )

    @classmethod
    def get_colors(cls, is_dark: bool) -> ColorScheme:
        return cls.DARK if is_dark else cls.LIGHT