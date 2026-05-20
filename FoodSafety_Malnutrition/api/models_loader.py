"""
Models Loader - Load and manage all trained models
"""
import os
import pickle
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Default to <repo>/FoodSafety_Malnutrition/models (relative to this file).
DEFAULT_MODELS_PATH = Path(__file__).resolve().parent.parent / "models"


class ModelsLoader:
    def __init__(self, models_path=None):
        resolved = models_path or os.environ.get('MODELS_PATH') or DEFAULT_MODELS_PATH
        self.models_path = str(resolved)
        self.models = {}
        self.label_encoder = None
        self.scaler = None

    def load_all_models(self):
        """Load all available models into memory. Missing files are skipped."""
        logger.info(f"Loading models from: {self.models_path}")

        # Classification models (pickle)
        for key, filename in [
            ('logistic_regression', 'logistic_regression.pkl'),
            ('logistic_regression_tuned', 'logistic_regression_tuned.pkl'),
            ('logistic_regression_calibrated', 'logistic_regression_calibrated.pkl'),
            ('random_forest', 'random_forest.pkl'),
            ('random_forest_tuned', 'random_forest_tuned.pkl'),
            ('xgboost', 'xgboost.pkl'),
            ('xgboost_tuned', 'xgboost_tuned.pkl'),
        ]:
            model = self._try_load_pickle(filename)
            if model is not None:
                self.models[key] = model

        # Deep learning models (Keras). Import lazily so the API can start
        # without TensorFlow installed when only classical models are used.
        try:
            import tensorflow as tf
            keras_loader = tf.keras.models.load_model
        except Exception as e:
            logger.warning(f"TensorFlow unavailable, skipping Keras models: {e}")
            keras_loader = None

        if keras_loader is not None:
            for key, filename in [
                ('ann', 'ann_model.h5'),
                ('ann_mc_dropout', 'ann_mc_dropout.h5'),
                ('bilstm', 'bilstm_model.h5'),
                ('bilstm_attention', 'bilstm_attention.h5'),
                ('rcnn', 'rcnn_model.h5'),
                ('cnn', 'cnn_model.h5'),
                ('cnn_resnet50', 'cnn_resnet50_transfer.h5'),
                ('cnn_production', 'cnn_best_model_production.h5'),
            ]:
                model = self._try_load_keras(filename, keras_loader)
                if model is not None:
                    self.models[key] = model

        # Label encoder
        self.label_encoder = self._try_load_pickle('label_encoder.pkl')

        logger.info(f"Loaded {len(self.models)} model(s); label_encoder={'ok' if self.label_encoder else 'missing'}")
        return len(self.models) > 0

    def _try_load_pickle(self, filename):
        path = os.path.join(self.models_path, filename)
        if not os.path.exists(path):
            logger.debug(f"Skipping missing pickle: {filename}")
            return None
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return None

    def _try_load_keras(self, filename, keras_loader):
        path = os.path.join(self.models_path, filename)
        if not os.path.exists(path):
            logger.debug(f"Skipping missing keras model: {filename}")
            return None
        # compile=False skips re-materialising the training loss/metrics, which
        # avoids Keras 3 deserialisation errors for models saved under Keras 2
        # (e.g. 'keras.metrics.mse' is no longer a KerasSaveable subclass).
        try:
            return keras_loader(path, compile=False)
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return None

    def get_model(self, model_name):
        return self.models.get(model_name)

    def get_all_models(self):
        return self.models

    def get_status(self):
        status = {name: 'loaded' for name in self.models}
        status['label_encoder'] = 'loaded' if self.label_encoder is not None else 'missing'
        return status

    def get_label_encoder(self):
        return self.label_encoder
