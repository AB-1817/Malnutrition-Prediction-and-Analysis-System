"""
Model Monitoring & Drift Detection
Tracks model performance, data drift, and triggers retraining when needed.
"""
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import pickle
import logging
from scipy.stats import entropy

logger = logging.getLogger(__name__)

class ModelMonitor:
    def __init__(self, predictions_log_path='monitoring/predictions.csv',
                 drift_threshold=0.1, performance_threshold=0.02):
        self.predictions_log = predictions_log_path
        self.drift_threshold = drift_threshold
        self.performance_threshold = performance_threshold
        self.baseline_metrics = self._load_baseline()

    def log_prediction(self, features, prediction, confidence, actual_label=None):
        """Log a prediction for monitoring"""
        try:
            prediction_record = {
                'timestamp': datetime.now().isoformat(),
                'features': json.dumps(features.tolist()),
                'prediction': prediction,
                'confidence': confidence,
                'actual_label': actual_label,
                'is_correct': prediction == actual_label if actual_label else None
            }

            # Append to CSV
            df = pd.DataFrame([prediction_record])
            if not os.path.exists(self.predictions_log):
                df.to_csv(self.predictions_log, index=False)
            else:
                df.to_csv(self.predictions_log, mode='a', header=False, index=False)

        except Exception as e:
            logger.error(f"Error logging prediction: {str(e)}")

    def detect_data_drift(self, new_data, baseline_data):
        """
        Detect if new data distribution has drifted from baseline
        Using Kullback-Leibler divergence
        """
        try:
            drifts = {}

            for feature in new_data.columns:
                # Compute distributions
                baseline_hist, bins = np.histogram(baseline_data[feature], bins=20)
                new_hist, _ = np.histogram(new_data[feature], bins=bins)

                # Normalize
                baseline_dist = baseline_hist / baseline_hist.sum()
                new_dist = new_hist / new_hist.sum()

                # KL divergence
                kl_div = entropy(new_dist + 1e-10, baseline_dist + 1e-10)
                drifts[feature] = kl_div

            # Check if drift exceeded threshold
            mean_drift = np.mean(list(drifts.values()))
            drift_detected = mean_drift > self.drift_threshold

            return {
                'drift_detected': drift_detected,
                'mean_drift': mean_drift,
                'feature_drifts': drifts,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error detecting drift: {str(e)}")
            return None

    def detect_performance_degradation(self, recent_predictions):
        """
        Detect if model performance has degraded
        Compares recent accuracy against baseline
        """
        try:
            recent_df = pd.read_csv(self.predictions_log).tail(recent_predictions)

            # Calculate accuracy if we have actual labels
            if 'is_correct' in recent_df.columns:
                recent_accuracy = recent_df['is_correct'].mean()

                # Compare to baseline
                accuracy_drop = self.baseline_metrics['accuracy'] - recent_accuracy

                degradation_detected = accuracy_drop > self.performance_threshold

                return {
                    'degradation_detected': degradation_detected,
                    'baseline_accuracy': self.baseline_metrics['accuracy'],
                    'recent_accuracy': recent_accuracy,
                    'accuracy_drop': accuracy_drop,
                    'timestamp': datetime.now().isoformat()
                }

            return {'warning': 'No actual labels available for degradation check'}

        except Exception as e:
            logger.error(f"Error detecting degradation: {str(e)}")
            return None

    def _load_baseline(self):
        """Load baseline metrics for comparison"""
        return {
            'accuracy': 0.9788,  # LR accuracy from Notebook 9
            'precision': 0.97,
            'recall': 0.97,
            'f1': 0.97
        }

    def get_monitoring_report(self, days=7):
        """Generate monitoring report for last N days"""
        try:
            df = pd.read_csv(self.predictions_log)
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Filter by date
            cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            recent_df = df[df['timestamp'] >= cutoff_date - pd.Timedelta(days=days)]

            report = {
                'period': f'Last {days} days',
                'total_predictions': len(recent_df),
                'avg_confidence': recent_df['confidence'].mean(),
                'std_confidence': recent_df['confidence'].std(),
                'timestamp': datetime.now().isoformat()
            }

            # Add accuracy if available
            if 'is_correct' in recent_df.columns:
                report['accuracy'] = recent_df['is_correct'].mean()
                report['error_rate'] = 1 - report['accuracy']

            return report

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return None

class DriftAlert:
    """Alert system for drift and degradation"""

    @staticmethod
    def send_alert(alert_type, message, severity='warning'):
        """Send alert (can be extended to email, Slack, etc.)"""
        alert = {
            'type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        }

        logger.warning(f"ALERT [{severity.upper()}]: {message}")

        # Save alert to file
        with open('monitoring/alerts.json', 'a') as f:
            f.write(json.dumps(alert) + '\n')

        return alert

    @staticmethod
    def check_and_alert(monitor, criteria):
        """Check criteria and send alert if met"""
        if criteria.get('drift_detected'):
            DriftAlert.send_alert(
                'DATA_DRIFT',
                f"Data drift detected (KL divergence: {criteria['mean_drift']:.4f})",
                severity='high'
            )

        if criteria.get('degradation_detected'):
            DriftAlert.send_alert(
                'PERFORMANCE_DEGRADATION',
                f"Performance dropped by {criteria['accuracy_drop']*100:.2f}%",
                severity='high'
            )
