import cloudinary.uploader

# image_tag = cloudinary.CloudinaryImage('main-sample').image()
# image_upload = cloudinary.uploader.upload(r'S:\Git\snapmap-backend\src\app\images\d621e80b76b6f70da84656e33e9e6e45.jpg', folder='snapmap')
# image_info = cloudinary.api.resource('main-sample')

class CloudinaryService:

  def upload_image(file, folder: str, public_id: str = None):
    """
    Upload an image to Cloudinary.
    If public_id is provided, it will overwrite the existing image with that public_id.
    """
    upload_options = {"folder": folder}
    
    if public_id:
      # Overwrite existing image with the same public_id
      upload_options["public_id"] = public_id
      upload_options["overwrite"] = True
      upload_options["invalidate"] = True
    
    result = cloudinary.uploader.upload(file, **upload_options)
    return result
  
  def delete_image(public_id: str):
    """Delete an image from Cloudinary using its public_id"""
    result = cloudinary.uploader.destroy(public_id)
    return result