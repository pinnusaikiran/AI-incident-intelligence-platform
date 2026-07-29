import pandas as pd
from sklearn.pipeline import Pipeline

from api.schemas.prediction import PredictionRequest

class FeaturePreparer:
    """
    Converts a validated PredictionRequest into model-ready features.
    """
    def __init__(self,pipeline:Pipeline):
        self.pipeline=pipeline


    def prepare(self,request:PredictionRequest)-> pd.DataFrame:
        """
        Prepare model input from the validate request
        """
        data = request.model_dump(mode="json")
        df=pd.DataFrame([data])
        transformed_features=self.pipeline.transform(df)
        return transformed_features
    
