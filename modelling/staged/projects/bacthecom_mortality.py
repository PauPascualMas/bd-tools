"""Bacthecom staged mortality project adapter.

Defaults align with the BAcTHECOM mortality-preprocessed dataset.
"""

from __future__ import annotations

import argparse

from three_level.cli import build_arg_parser as build_base_parser

PROJECT_NAME = "bacthecom_mortality"


def build_parser() -> argparse.ArgumentParser:
    parser = build_base_parser()
    parser.set_defaults(
        sepsis_target="mortalidad",
        hemo_target="resultado_hemo_grouped",
        cef_target="mortalidad_30_dias",
        optuna_study_prefix="bacthecom_mortality",
    )
    return parser


def run(args: argparse.Namespace) -> None:
    from three_level.modelling import run_training

    run_training(args)
