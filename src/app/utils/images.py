import cloudinary.uploader

# image_tag = cloudinary.CloudinaryImage('main-sample').image()
# image_upload = cloudinary.uploader.upload(r'S:\Git\snapmap-backend\src\app\images\d621e80b76b6f70da84656e33e9e6e45.jpg', folder='snapmap')
# image_info = cloudinary.api.resource('main-sample')

class CloudinaryService:

  def upload_image(file, folder: str):
    result = cloudinary.uploader.upload(file, folder=folder)

    return result