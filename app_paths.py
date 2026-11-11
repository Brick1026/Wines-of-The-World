import os
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def resource_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)


if getattr(sys, "frozen", False):
    local_app_data = os.environ.get("LOCALAPPDATA")
    data_root = (
        Path(local_app_data)
        if local_app_data
        else Path.home() / "AppData" / "Local"
    )
    DATA_DIR = data_root / "Wines of The World" / "Data"
else:
    DATA_DIR = PROJECT_ROOT / "Data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

MASTER_WINE_DATA_PATH = DATA_DIR / "master_wine_data.json"
PAST_RECOMMENDATIONS_PATH = DATA_DIR / "past_recommendations.json"

if getattr(sys, "frozen", False):
    for data_path in (MASTER_WINE_DATA_PATH, PAST_RECOMMENDATIONS_PATH):
        bundled_path = resource_path("Data", data_path.name)
        if not data_path.exists() and bundled_path.exists():
            shutil.copy2(bundled_path, data_path)

if not PAST_RECOMMENDATIONS_PATH.exists():
    PAST_RECOMMENDATIONS_PATH.write_text("[]", encoding="utf-8")
