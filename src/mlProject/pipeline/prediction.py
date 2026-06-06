import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from mlProject.components.data_transformation import NUMERIC_FEATURES

class PredictionPipeline:
    def __init__(self):
        self.model = None
        self.preprocessor = None

    def predict(self, data):
        if self.model is None:
            model_path = Path('artifacts/model_trainer/model.joblib')
            self.model = joblib.load(model_path)
        if self.preprocessor is None:
            preprocessor_path = Path('artifacts/data_transformation/preprocessor.joblib')
            if preprocessor_path.exists():
                self.preprocessor = joblib.load(preprocessor_path)

        if isinstance(data, np.ndarray):
            if self.preprocessor is not None:
                processed = self.preprocessor.transform(data)
            else:
                processed = data
        elif isinstance(data, pd.DataFrame):
            if self.preprocessor is not None:
                try:
                    numeric_data = data[NUMERIC_FEATURES]
                except (KeyError, ValueError):
                    numeric_data = data
                processed = self.preprocessor.transform(numeric_data)
            else:
                processed = data.values
        else:
            processed = data

        prediction = self.model.predict(processed)
        return prediction