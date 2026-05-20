"""
Prediction Engine - Core prediction logic with SHAP explanations
"""
import numpy as np
import shap
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PredictionEngine:
    def __init__(self, models_loader):
        self.models_loader = models_loader
        # Prefer the calibrated LR when available; fall back to the tuned
        # variant, then the base model.
        self.lr_model = (
            models_loader.get_model('logistic_regression_calibrated')
            or models_loader.get_model('logistic_regression_tuned')
            or models_loader.get_model('logistic_regression')
        )
        if self.lr_model is None:
            raise RuntimeError(
                "No logistic regression model found in models directory. "
                "Expected one of: logistic_regression_calibrated.pkl, "
                "logistic_regression_tuned.pkl, logistic_regression.pkl"
            )
        self.rf_model = (
            models_loader.get_model('random_forest_tuned')
            or models_loader.get_model('random_forest')
        )
        self.label_encoder = models_loader.get_label_encoder()
        if self.label_encoder is None:
            raise RuntimeError("label_encoder.pkl not found in models directory")
        self.risk_labels = self.label_encoder.classes_

    def predict_with_confidence(self, features):
        """
        Make prediction with calibrated confidence scores
        features: np.array of shape (1, 8)
        """
        try:
            # Get calibrated probabilities
            probabilities = self.lr_model.predict_proba(features)[0]

            # Get predicted class
            predicted_class = np.argmax(probabilities)
            confidence = probabilities[predicted_class]

            # Map to risk label
            risk_label = self.risk_labels[predicted_class]

            # Create probability distribution dict
            prob_dict = {
                self.risk_labels[i]: probabilities[i]
                for i in range(len(self.risk_labels))
            }

            return {
                'risk_level': risk_label,
                'confidence': confidence,
                'probabilities': prob_dict,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise

    def get_shap_explanation(self, features):
        """
        Generate SHAP-based feature importance explanation
        """
        try:
            # Make prediction
            prediction = self.lr_model.predict(features)[0]
            risk_label = self.risk_labels[prediction]

            # Create SHAP explainer
            explainer = shap.LinearExplainer(self.lr_model, features)
            shap_values = explainer.shap_values(features)

            # Feature names
            feature_names = ['stunting', 'wasting', 'underweight', 'overweight',
                           'stunting_avg', 'wasting_avg', 'underweight_avg', 'undernourishment_pct']

            # Get top contributing features
            feature_importance = {}
            for i, fname in enumerate(feature_names):
                if isinstance(shap_values, list):
                    importance = np.abs(shap_values[prediction][0][i])
                else:
                    importance = np.abs(shap_values[0][i])
                feature_importance[fname] = float(importance)

            # Sort and get top 3
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            top_drivers = [{'feature': f[0], 'importance': f[1]} for f in sorted_features[:3]]

            return {
                'prediction': risk_label,
                'feature_importance': feature_importance,
                'top_drivers':top_drivers
            }

        except Exception as e:
            logger.error(f"SHAP explanation error: {str(e)}")
            raise

    def ensemble_predict(self, features):
        """
        Ensemble prediction combining Calibrated LR + Random Forest
        """
        try:
            # LR prediction
            lr_proba = self.lr_model.predict_proba(features)[0]
            lr_pred = np.argmax(lr_proba)

            # RF prediction
            rf_proba = self.rf_model.predict_proba(features)[0]
            rf_pred = np.argmax(rf_proba)

            # Weighted average (LR weight: 0.6, RF weight: 0.4)
            ensemble_proba = 0.6 * lr_proba + 0.4 * rf_proba
            ensemble_pred = np.argmax(ensemble_proba)
            confidence = ensemble_proba[ensemble_pred]

            return {
                'risk_level': self.risk_labels[ensemble_pred],
                'confidence': confidence,
                'lr_prediction': self.risk_labels[lr_pred],
                'rf_prediction': self.risk_labels[rf_pred]
            }

        except Exception as e:
            logger.error(f"Ensemble prediction error: {str(e)}")
            raise

    @staticmethod
    def validate_features(data):
        """Validate input features"""
        required_fields = ['stunting', 'wasting', 'underweight', 'overweight',
                          'stunting_avg', 'wasting_avg', 'underweight_avg', 'undernourishment_pct']

        for field in required_fields:
            if field not in data:
                return False, f"Missing field: {field}"
            if not isinstance(data[field], (int, float)):
                return False, f"Invalid type for {field}: expected number"
            if data[field] < 0 or data[field] > 100:
                return False, f"Invalid range for {field}: expected 0-100"

        return True, "Valid"
