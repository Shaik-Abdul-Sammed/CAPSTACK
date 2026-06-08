#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.security.enanced_models import EnhancedFinancialModels
from app.security.real_world_data_generator import RealWorldDataGenerator

def main():
    """Train all enhanced models with real-world data"""
    print("=== Training Enhanced Financial Models ===")

    print("Generating training datasets...")
    generator = RealWorldDataGenerator()
    generator.save_datasets()
    print("✅ Datasets generated under data/real_world")
    
    trainer = EnhancedFinancialModels()
    
    # Train all models
    results = {}
    
    try:
        print("Training Fraud Detection Model...")
        results['fraud_detection'] = trainer.train_fraud_detection_model()
        print("✅ Fraud Detection Model Trained Successfully")
    except Exception as e:
        print(f"❌ Fraud Detection Model Training Failed: {e}")
    
    try:
        print("Training Crisis Prediction Models...")
        results['crisis_prediction'] = trainer.train_crisis_prediction_model()
        print("✅ Crisis Prediction Models Trained Successfully")
    except Exception as e:
        print(f"❌ Crisis Prediction Models Training Failed: {e}")
    
    try:
        print("Training Income Volatility Model...")
        results['income_volatility'] = trainer.train_income_volatility_model()
        print("✅ Income Volatility Model Trained Successfully")
    except Exception as e:
        print(f"❌ Income Volatility Model Training Failed: {e}")
    
    try:
        print("Training Anomaly Detection Model...")
        results['anomaly_detection'] = trainer.train_anomaly_detection_model()
        print("✅ Anomaly Detection Model Trained Successfully")
    except Exception as e:
        print(f"❌ Anomaly Detection Model Training Failed: {e}")
    
    # Save summary
    summary = trainer.get_model_summary()
    import json
    import pandas as pd
    
    with open(f"{trainer.model_dir}/training_summary.json", 'w') as f:
        json.dump({
            'training_results': results,
            'model_summary': summary,
            'timestamp': pd.Timestamp.now().isoformat()
        }, f, indent=2, default=str)
    
    print("=== Enhanced Model Training Complete ===")
    print(f"Models saved to: {trainer.model_dir}")
    return results

if __name__ == "__main__":
    main()
