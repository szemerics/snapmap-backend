import tempfile
from PIL import Image
from huggingface_hub import InferenceClient
from app import settings

class NSFWModel:
    def __init__(self):
        self._local_pipeline = None
        self._api_client = None

    def classify_image(self, image: Image.Image):
        if settings.NSFW_MODE == "api":
            return self._classify_with_api(image)
        return self._classify_with_local_pipeline(image)

    def _get_local_pipeline(self):
        if self._local_pipeline is None:
            from transformers import pipeline, AutoModelForImageClassification, ViTImageProcessor
            import torch

            model = AutoModelForImageClassification.from_pretrained(settings.NSFW_LOCAL_MODEL_PATH)
            processor = ViTImageProcessor.from_pretrained(settings.NSFW_LOCAL_MODEL_PATH)
            self._local_pipeline = pipeline(
                "image-classification",
                model=model,
                feature_extractor=processor,
                device=0 if torch.cuda.is_available() else -1,
            )
        return self._local_pipeline


    def _get_api_client(self):
        if not settings.NSFW_API_TOKEN:
            raise ValueError("NSFW_API_TOKEN is required when NSFW_MODE=api")
        if self._api_client is None:
            self._api_client = InferenceClient(
                provider="hf-inference",
                api_key=settings.NSFW_API_TOKEN,
                timeout=30,
            )
        return self._api_client


    def _classify_with_api(self, image: Image.Image):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
            image.convert("RGB").save(tmp.name, format="JPEG")
            results = self._get_api_client().image_classification(tmp.name, model="Falconsai/nsfw_image_detection")
        return [{"label": item.label, "score": item.score} for item in results]

    def _classify_with_local_pipeline(self, image: Image.Image):
        return self._get_local_pipeline()(image)