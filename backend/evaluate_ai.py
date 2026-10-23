"""
CivicShield AI Model Evaluation Runner
Run this script to show model training performance, accuracy, precision, recall, F1-scores, and live inference tests to your faculty/guide.
Usage:
    python evaluate_ai.py
"""
import sys
import os

# Add backend root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ai.evaluate_model import print_cli_evaluation

if __name__ == "__main__":
    print_cli_evaluation()
