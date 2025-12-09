from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils.logger import get_logger

from src.database.db_operations import fetch_all_candidates


logger = get_logger(__name__)


def export_ranked_candidates_csv(output_dir: str | Path = "output", filename: str = "ranked_candidates.csv") -> Path:
    """Fetch candidates from DB, sort by score, and export to CSV."""

    rows = fetch_all_candidates()
    if not rows:
        logger.warning("No candidates found in database; CSV will not be created.")
        raise RuntimeError("No candidates available for ranking.")

    columns = ["id", "name", "email", "phone", "skills", "experience", "score", "resume_path"]

    df = pd.DataFrame(rows, columns=columns)
    df.sort_values(by="score", ascending=False, inplace=True)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    csv_path = output_path / filename

    df.to_csv(csv_path, index=False)

    logger.info("Exported ranked candidates to %s", csv_path)
    return csv_path
