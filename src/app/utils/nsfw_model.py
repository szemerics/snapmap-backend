import tempfile
from PIL import Image
from huggingface_hub import InferenceClient
from app import settings

_local_pipeline = None
_api_client = None


def _get_local_pipeline():
    global _local_pipeline
    if _local_pipeline is None:
        from transformers import pipeline, AutoModelForImageClassification, ViTImageProcessor
        import torch

        model = AutoModelForImageClassification.from_pretrained(settings.NSFW_LOCAL_MODEL_PATH)
        processor = ViTImageProcessor.from_pretrained(settings.NSFW_LOCAL_MODEL_PATH)
        _local_pipeline = pipeline(
            "image-classification",
            model=model,
            feature_extractor=processor,
            device=0 if torch.cuda.is_available() else -1,
        )
    return _local_pipeline


def _get_api_client():
    global _api_client
    if not settings.NSFW_API_TOKEN:
        raise ValueError("NSFW_API_TOKEN is required when NSFW_MODE=api")
    if _api_client is None:
        _api_client = InferenceClient(
            provider="hf-inference",
            api_key=settings.NSFW_API_TOKEN,
            timeout=30,
        )
    return _api_client


def _classify_with_api(image: Image.Image):
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        image.convert("RGB").save(tmp.name, format="JPEG")
        results = _get_api_client().image_classification(tmp.name, model="Falconsai/nsfw_image_detection")
    return [{"label": item.label, "score": item.score} for item in results]


def classify_image(image: Image.Image):
    if settings.NSFW_MODE == "api":
        return _classify_with_api(image)
    return _get_local_pipeline()(image)