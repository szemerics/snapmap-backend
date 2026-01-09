import sys
import asyncio
from pathlib import Path
from typing import List
import io
from fastapi import UploadFile
# Add src directory to Python path
src_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_path))

from app.models.user import User, UserRegister, UserRole
from app.utils.auth import auth

from app.models.photo import Photo
from app.config import configure_cloudinary, engine
from app.views.photo import PhotoView
from app.utils.init.lib.photo_entries import PhotoEntry, get_photo_entries


async def main():  
    configure_cloudinary()
    await __creating_users()
    admin_user = await engine.find_one(User, (User.username == 'adminuser'))
    moderator_user = await engine.find_one(User, (User.username == 'moderatoruser'))
    default_user = await engine.find_one(User, (User.username == 'testuser')) 
    admin_user.role = UserRole.ADMIN
    await engine.save(admin_user)
    moderator_user.role = UserRole.MODERATOR
    await engine.save(moderator_user)

    await __upload_photos(default_user, moderator_user, admin_user)


async def __upload_photos(default_user: User, moderator_user: User, admin_user: User):
    """Upload initial photos for testing purposes."""
    print('Uploading photos...')
    to_upload_photos: List[PhotoEntry] = get_photo_entries(default_user, moderator_user, admin_user)

    for photo_entry in to_upload_photos:
      query = {
          "location.lat": photo_entry.data.location.lat,
          "location.lng": photo_entry.data.location.lng,
      }
      is_existing_photo = await engine.find_one(Photo, query) is not None

      if is_existing_photo:
          print(f"Photo {photo_entry.file_path} already exists, skipping...")
          continue
      
      user_to_upload = await engine.find_one(User, (User.id == photo_entry.user_id))

      print(f'Uploading photo from {photo_entry.file_path}')
      file_path = photo_entry.file_path
      with open(file_path, 'rb') as f:
          file_content = f.read()
          upload_file = UploadFile(file=io.BytesIO(file_content))
          created_photo = await PhotoView.create_photo(photo_entry.data, upload_file, user_to_upload)
          
          # Set likes and comments after photo creation
          await __set_photo_metadata(created_photo, photo_entry)


async def __set_photo_metadata(photo: Photo, photo_entry: PhotoEntry):
    """Set likes and comments on a photo after creation."""
    if photo_entry.likes > 0:
        photo.likes = photo_entry.likes
    
    if photo_entry.comments:
        photo.comments = photo_entry.comments
    
    await engine.save(photo)
        


async def __creating_users():
    """Create initial users for testing purposes."""
    print('Creating users...')      
    to_register_users: List[UserRegister] = []

    to_register_users.append(UserRegister(
        username='testuser',
        email='testuser@example.com',
        password='testuser123'
    ))
    to_register_users.append(UserRegister(
        username='moderatoruser',
        email='moderatoruser@example.com',
        password='moderatoruser123'
    ))
    to_register_users.append(UserRegister(
        username='adminuser',
        email='adminuser@example.com',
        password='adminuser123'
    ))

    for user in to_register_users:
        print(f'Registering user with email {user.email}...')
        new_user = await auth.register_auth(user)
        if not new_user:
            print(f'User with email {user.email} already exists, skipping...')
            continue

    
if __name__ == "__main__":
    asyncio.run(main())