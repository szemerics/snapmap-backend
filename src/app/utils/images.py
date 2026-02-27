import cloudinary.uploader
from PIL import Image
import io
from app.utils.nsfw_model import nsfw_pipeline
from fastapi import File

# image_tag = cloudinary.CloudinaryImage('main-sample').image()
# image_upload = cloudinary.uploader.upload(r'S:\Git\snapmap-backend\src\app\images\d621e80b76b6f70da84656e33e9e6e45.jpg', folder='snapmap')
# image_info = cloudinary.api.resource('main-sample')


class CloudinaryService:

  async def upload_image(file: File, folder: str, public_id: str = None):
    """
    Upload an image to Cloudinary.
    If public_id is provided, it will overwrite the existing image with that public_id.
    """
    file_content = await file.read()

    # Convert raw bytes to a PIL image for classification
    try:
        image = Image.open(io.BytesIO(file_content))
    except Exception as e:
        print(f"Error loading image: {e}")
        raise ValueError("Uploaded file is not a valid image")


    classifications = nsfw_pipeline(image)
    if (classifications[0]["label"].lower() == "nsfw") and (classifications[0]["score"] > 0.7):
      raise ValueError("Uploaded image is classified as NSFW")

    upload_options = {}
    if folder and not public_id: 
      upload_options = {"folder": folder}
    if public_id:
      upload_options["public_id"] = public_id
      upload_options["overwrite"] = True
    
    result = cloudinary.uploader.upload(file_content, **upload_options)
    return result
  
  
  def delete_image(public_id: str):
    """Delete an image from Cloudinary using its public_id"""
    result = cloudinary.uploader.destroy(public_id)
    return result