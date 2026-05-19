#!/usr/bin/env python3
"""Run BAcTHECOM staged mortality modelling from a preprocessed CSV.

This wrapper mirrors the MePRAM-style staged workflow but pins BAcTHECOM-
specific target defaults:
- Gate target: ``mortalidad``
- Final stage target: ``mortalidad_30_dias`` or ``mortalidad_14_dias``
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import csv

ROOT = Path(__file__).resolve().parent.parent
MODELLING_ENTRYPOINT = ROOT / "modelling" / "modelling.py"

TARGET_BY_HORIZON = {
    30: "mortalidad_30_dias",
    14: "mortalidad_14_dias",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run BAcTHECOM staged mortality model using a preprocessed dataset."
    )
    parser.add_argument(
        "--database-file",
        "-db",
        type=Path,
        required=True,
        help="Path to preprocessed BAcTHECOM CSV used by the staged modelling pipeline.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        required=True,
        help="Output directory for modelling artifacts.",
    )
    parser.add_argument(
        "--mortality-horizon-days",
        type=int,
        choices=sorted(TARGET_BY_HORIZON.keys()),
        default=30,
        help="Final mortality horizon target (14 or 30 days).",
    )
    parser.add_argument("--model-type", choices=["xgb", "lgbm", "rf", "catb"], default="xgb")
    parser.add_argument("--binary-trials", type=int, default=50)
    parser.add_argument("--cv-splits", type=int, default=5)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--na-perc-limit", type=float, default=0.7)
    parser.add_argument("--max-features", type=int, default=20)
    parser.add_argument("--max-corr", type=float, default=0.95)
    parser.add_argument("--skip-optuna", action="store_true")
    parser.add_argument("--skip-rfecv", action="store_true")
    return parser.parse_args()


def validate_input_columns(path: Path, final_target: str) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    missing = [column for column in ["mortalidad", final_target] if column not in header]
    if missing:
        raise ValueError(
            "Input file is missing required target columns for staged mortality modelling: "
            + ", ".join(missing)
        )


def main() -> None:
    args = parse_args()
    final_target = TARGET_BY_HORIZON[args.mortality_horizon_days]
    validate_input_columns(args.database_file, final_target)

    cmd = [
        sys.executable,
        str(MODELLING_ENTRYPOINT),
        "--project",
        "bacthecom_mortality",
        "--database-file",
        str(args.database_file),
        "--output-dir",
        str(args.output_dir),
        "--sepsis-target",
        "mortalidad",
        "--cef-target",
        final_target,
        "--model-type",
        args.model_type,
        "--binary-trials",
        str(args.binary_trials),
        "--cv-splits",
        str(args.cv_splits),
        "--test-size",
        str(args.test_size),
        "--random-state",
        str(args.random_state),
        "--na-perc-limit",
        str(args.na_perc_limit),
        "--max-features",
        str(args.max_features),
        "--max-corr",
        str(args.max_corr),
    ]
    if args.skip_optuna:
        cmd.append("--skip-optuna")
    if args.skip_rfecv:
        cmd.append("--skip-rfecv")

    print("Running BAcTHECOM staged mortality modelling command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
