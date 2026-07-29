from src.inference.prediction import PredictionResult
from src.inference.explanation import ExplanationResult
from src.inference.response import APIResponse,PredictionInfo,ModelInfo

def build_response(prediction:PredictionResult,explanation:ExplanationResult,metadata:dict)-> APIResponse:
    prediction_response=PredictionInfo(
        prediction_class=prediction.prediction,
        prediction_label=(metadata["positive_class"] if prediction.prediction==1 else "No SLA Breach"),
        probability=prediction.probability
        )
    model_info=ModelInfo(name=metadata["model_name"],version=metadata["model_version"])

    return APIResponse(prediction=prediction_response,explanation=explanation,model=model_info)
