#!/usr/bin/env python3

"""
Local workflow for CAPSTACK ML service.

This script can:
- generate smaller training datasets for local iteration,
- train the enhanced models,
- evaluate the trained outputs,
- choose the best overall model for the current dataset run,
- optionally start the FastAPI service on localhost.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

from app.security.enanced_models import EnhancedFinancialModels
from app.security.real_world_data_generator import RealWorldDataGenerator


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data" / "real_world"


def generate_local_datasets(crisis_samples: int, fraud_samples: int, income_samples: int) -> None:
    generator = RealWorldDataGenerator(seed=42)
    generator.save_datasets(
        output_dir=str(DATA_DIR),
        crisis_samples=crisis_samples,
        fraud_samples=fraud_samples,
        income_samples=income_samples,
    )


def score_training_result(model_name: str, result: Dict[str, Any]) -> float:
    if model_name == "fraud_detection":
        return float(result.get("roc_auc", 0.0)) * 0.4 + float(result.get("accuracy", 0.0)) * 0.6

    if model_name == "crisis_prediction":
        targets = result.get("targets", {})
        if not targets:
            return 0.0
        r2_scores = [float(target_result.get("r2", 0.0)) for target_result in targets.values()]
        return sum(r2_scores) / len(r2_scores)

    if model_name == "income_volatility":
        return float(result.get("accuracy", 0.0))

    if model_name == "anomaly_detection":
        anomaly_rate = float(result.get("anomaly_rate", 0.0))
        return max(0.0, 1.0 - abs(anomaly_rate - 0.05) * 10)

    return 0.0


def score_profile_results(results: Dict[str, Dict[str, Any]]) -> float:
    return sum(score_training_result(name, result) for name, result in results.items()) / max(len(results), 1)


def train_and_rank_models(profile: str = "balanced", compare_profiles: bool = False) -> Tuple[Dict[str, Any], Dict[str, float]]:
    trainer = EnhancedFinancialModels()

    if compare_profiles:
        comparison = trainer.compare_training_profiles(
            data_paths={
                "fraud_detection": str(DATA_DIR / "fraud_detection_enhanced.csv"),
                "crisis_prediction": str(DATA_DIR / "financial_crisis_dataset.csv"),
                "income_volatility": str(DATA_DIR / "income_volatility_dataset.csv"),
                "anomaly_detection": str(DATA_DIR / "financial_crisis_dataset.csv"),
            },
            crisis_rows=2500,
        )
        profile_scores = {name: score_profile_results(bundle["results"]) for name, bundle in comparison.items()}
        selected_profile = max(profile_scores, key=profile_scores.get)
        print(f"Selected training profile: {selected_profile} ({profile_scores[selected_profile]:.4f})")
        results = comparison[selected_profile]["results"]
        scores = comparison[selected_profile]["scores"]
    else:
        print(f"Using training profile: {profile}")
        results = trainer.train_all_models_with_profile(profile=profile, crisis_rows=2500)
        scores = {name: score_training_result(name, result) for name, result in results.items()}

    report = {
        "scores": scores,
        "best_model": max(scores, key=scores.get),
        "model_summary": trainer.get_model_summary(),
        "training_profile": profile,
        "metrics": {
            name: {
                key: value
                for key, value in result.items()
                if key in {"train_accuracy", "accuracy", "roc_auc", "anomaly_rate"}
            }
            for name, result in results.items()
        },
    }

    report_path = trainer.model_dir + "/local_training_report.json"
    with open(report_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, default=str)

    print(f"Best overall model: {report['best_model']} ({scores[report['best_model']]:.4f})")
    print(f"Report saved to: {report_path}")

    return results, scores


def serve_localhost(host: str, port: int) -> int:
    command = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        host,
        "--port",
        str(port),
        "--reload",
    ]
    print(f"Starting local server at http://{host}:{port}")
    return subprocess.call(command, cwd=str(ROOT_DIR))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train, rank, and optionally serve CAPSTACK ML models locally.")
    parser.add_argument("--train-only", action="store_true", help="Train and rank models without starting the server.")
    parser.add_argument("--serve", action="store_true", help="Start the local FastAPI server after training.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the local server to.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the local server to.")
    parser.add_argument("--profile", choices=["fast", "balanced", "thorough"], default="balanced", help="Training profile to use for the model suite.")
    parser.add_argument("--compare-profiles", action="store_true", help="Train all profiles and automatically select the best one.")
    parser.add_argument("--crisis-samples", type=int, default=5000, help="Rows to generate for the crisis dataset.")
    parser.add_argument("--fraud-samples", type=int, default=10000, help="Rows to generate for the fraud dataset.")
    parser.add_argument("--income-samples", type=int, default=5000, help="Rows to generate for the income volatility dataset.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    os.chdir(ROOT_DIR)

    print("Generating local training datasets...")
    generate_local_datasets(args.crisis_samples, args.fraud_samples, args.income_samples)

    print("Training and ranking models...")
    train_and_rank_models(profile=args.profile, compare_profiles=args.compare_profiles)

    if args.train_only and not args.serve:
        print("Local training complete. Server not started because --train-only was used.")
        return 0

    if args.serve or not args.train_only:
        return serve_localhost(args.host, args.port)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())