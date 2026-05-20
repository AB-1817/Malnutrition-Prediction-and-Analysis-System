"""
Automated Retraining Trigger
Detects when model retraining is needed and initiates the process
"""
import logging
import pickle
import os
from datetime import datetime
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class RetrainingTrigger:
    def __init__(self, models_path='models', data_path='data/processed'):
        self.models_path = models_path
        self.data_path = data_path
        self.history_file = 'monitoring/retraining_history.json'

    def should_retrain(self, drift_detected, degradation_detected, avg_drift, accuracy_drop):
        """
        Determine if retraining should be triggered
        Uses drift detection and performance degradation as signals
        """
        criteria = {
            'drift_threshold_exceeded': avg_drift > 0.15,  # Significant drift
            'performance_threshold_exceeded': accuracy_drop > 0.03,  # 3% accuracy drop
            'drift_detected': drift_detected,
            'degradation_detected': degradation_detected
        }

        # Trigger retraining if any combined criteria met
        should_retrain = (
            (drift_detected and accuracy_drop > 0.01) or  # Drift + small accuracy drop
            degradation_detected or  # Performance degradation
            avg_drift > 0.15  # Significant drift alone
        )

        return should_retrain, criteria

    def retrain_models(self, new_data, y_column='risk_label'):
        """
        Retrain classification models on new data
        Saves models with version suffix
        """
        try:
            logger.info("Starting model retraining...")

            # Get current model versions
            version = self._get_next_version()

            # Prepare data
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()

            X = new_data.drop(columns=[y_column])
            y = le.fit_transform(new_data[y_column])

            # Retrain models
            lr_model = LogisticRegression(max_iter=1000, random_state=42)
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='mlogloss')

            lr_model.fit(X, y)
            rf_model.fit(X, y)
            xgb_model.fit(X, y)

            # Save new models
            lr_path = f"{self.models_path}/logistic_regression_v{version}.pkl"
            rf_path = f"{self.models_path}/random_forest_v{version}.pkl"
            xgb_path = f"{self.models_path}/xgboost_v{version}.pkl"

            with open(lr_path, 'wb') as f:
                pickle.dump(lr_model, f)
            with open(rf_path, 'wb') as f:
                pickle.dump(rf_model, f)
            with open(xgb_path, 'wb') as f:
                pickle.dump(xgb_model, f)

            # Evaluate models
            lr_score = lr_model.score(X[:100], y[:100])
            rf_score = rf_model.score(X[:100], y[:100])
            xgb_score = xgb_model.score(X[:100], y[:100])

            logger.info(f"✓ Models retrained (v{version})")
            logger.info(f"  LR Accuracy: {lr_score:.4f}")
            logger.info(f"  RF Accuracy: {rf_score:.4f}")
            logger.info(f"  XGB Accuracy: {xgb_score:.4f}")

            # Log retraining event
            self._log_retraining_event(version, {
                'lr_accuracy': lr_score,
                'rf_accuracy': rf_score,
                'xgb_accuracy': xgb_score,
                'samples': len(X)
            })

            return True, version

        except Exception as e:
            logger.error(f"Retraining failed: {str(e)}")
            return False, None

    def _get_next_version(self):
        """Get next model version number"""
        existing_versions = []
        for f in os.listdir(self.models_path):
            if '_v' in f:
                try:
                    version = int(f.split('_v')[1].split('.')[0])
                    existing_versions.append(version)
                except:
                    pass

        return max(existing_versions) + 1 if existing_versions else 1

    def _log_retraining_event(self, version, metrics):
        """Log retraining event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'version': version,
            'metrics': metrics
        }

        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                history = json.load(f)

        history.append(event)

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def get_retraining_history(self):
        """Get retraining history"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def rollback_model(self, version):
        """Rollback to previous model version"""
        try:
            lr_path = f"{self.models_path}/logistic_regression_v{version}.pkl"
            rf_path = f"{self.models_path}/random_forest_v{version}.pkl"

            if os.path.exists(lr_path) and os.path.exists(rf_path):
                # Copy to current model paths
                import shutil
                shutil.copy(lr_path, f"{self.models_path}/logistic_regression.pkl")
                shutil.copy(rf_path, f"{self.models_path}/random_forest.pkl")

                logger.info(f"✓ Rolled back to version {version}")
                return True
            else:
                logger.error(f"Version {version} not found")
                return False

        except Exception as e:
            logger.error(f"Rollback failed: {str(e)}")
            return False

class ABTesting:
    """A/B Testing framework for model versions"""

    @staticmethod
    def route_prediction(request_id, new_model_traffic_pct=10):
        """
        Route prediction to v1 or v2 model
        new_model_traffic_pct: % of traffic to route to new model
        """
        import random
        return random.random() < (new_model_traffic_pct / 100)

    @staticmethod
    def compare_models(results_v1, results_v2):
        """Compare performance between model versions"""
        accuracy_v1 = results_v1['correct'] / len(results_v1)
        accuracy_v2 = results_v2['correct'] / len(results_v2)

        improvement = (accuracy_v2 - accuracy_v1) * 100

        return {
            'v1_accuracy': accuracy_v1,
            'v2_accuracy': accuracy_v2,
            'improvement_pct': improvement,
            'recommend_promotion': improvement > 0.5  # 0.5% improvement threshold
        }
