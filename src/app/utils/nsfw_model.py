from transformers import pipeline, AutoModelForImageClassification, ViTImageProcessor
import torch


MODEL_PATH = './nsfw_model'

nsfw_model = AutoModelForImageClassification.from_pretrained(MODEL_PATH)

nsfw_processor = ViTImageProcessor.from_pretrained(MODEL_PATH)

nsfw_pipeline = pipeline(
  "image-classification", 
  model=nsfw_model,
  feature_extractor=nsfw_processor,
  device= 0 if torch.cuda.is_available() else -1)