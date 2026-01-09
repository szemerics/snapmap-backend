import sys
import asyncio
from pathlib import Path
from typing import List
import io
from fastapi import UploadFile
from bson import ObjectId
# Add src directory to Python path
src_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_path))

from app.utils.auth import auth
from app.models.user import Camera, UserRegister, User, UserRole, Gear
from app.views.user import UserView
from app.models.photo import Photo
from app.config import configure_cloudinary, engine
from app.views.photo import PhotoView
from app.models.photo import CreatePhoto, Location
from datetime import datetime


class PhotoEntry():
    def __init__(self, file_path: str, data: CreatePhoto):
        self.file_path = file_path
        self.data = data


async def main():  
    configure_cloudinary()
    await __creating_users()
    admin_user = await engine.find_one(User, (User.username == 'adminuser'))
    moderator_user = await engine.find_one(User, (User.username == 'moderatoruser'))
    default_user = await engine.find_one(User, (User.username == 'testuser'))

    # token_response = await auth.login_auth('adminuser@example.com', 'adminuser123')
    # token = token_response.access_token if token_response else None
    
    admin_user.role = UserRole.ADMIN
    await engine.save(admin_user)
    moderator_user.role = UserRole.MODERATOR
    await engine.save(moderator_user)

    await __upload_photos(default_user, moderator_user, admin_user)


async def __upload_photos(default_user: User, moderator_user: User, admin_user: User):
    print('Uploading photos...')
    to_upload_photos: List[PhotoEntry] = []

    to_upload_photos.append(PhotoEntry('src/app/utils/init/lib/photos/csepel.jpg', CreatePhoto(
        user_id=default_user.id,
        location=Location(
            lat=47.444531981994814,
            lng=19.07154301874141
        ),
        date=datetime.now(),
        category='trainspotting',
        gear=Gear(
            camera=Camera(
                brand='Nikon',
                model='D3500',
                type='DSLR'
            ),
            lens='AF-P DX NIKKOR 18-55mm f/3.5-5.6G VR',
            extra_attachment='ND Filter'
        )
    )))

    to_upload_photos.append(PhotoEntry('src/app/utils/init/lib/photos/miskolc.jpg', CreatePhoto(
        user_id=moderator_user.id,
        location=Location(
            lat=48.09937752341158,
            lng=20.77555906988592
        ),
        date=datetime.now(),
        category='street',
        gear=Gear(
            camera=Camera(
                brand='Canon',
                model='EOS 250D',
                type='DSLR'
            ),
            lens='EF-S 18-55mm f/4-5.6 IS STM',
            extra_attachment=None
        )
    )))

    to_upload_photos.append(PhotoEntry('src/app/utils/init/lib/photos/szeged.jpg', CreatePhoto(
        user_id=admin_user.id,
        location=Location(
            lat=46.25372456930462,
            lng=20.14891582649533
        ),
        date=datetime.now(),
        category='street',
        gear=Gear(
            camera=Camera(
                brand='Sony',
                model='Alpha a7 IV',
                type='Mirrorless'
            ),
            lens='FE 24-70mm f/2.8 GM II',
            extra_attachment='DJI Ronin-S Gimbal'
        )
    )))

    for photo in to_upload_photos:
      is_existing_photo = await engine.find_one(Photo, (Photo.location.lat == photo.data.location.lat) & (Photo.location.lng == photo.data.location.lng))

      if is_existing_photo:
          print(f"Photo {photo.file_path} already exists, skipping...")
          continue
      
      user_to_upload = await engine.find_one(User, (User.id == photo.data.user_id))

      file_path = photo.file_path
      with open(file_path, 'rb') as f:
          file_content = f.read()
          upload_file = UploadFile(file=io.BytesIO(file_content))
          await PhotoView.create_photo(photo.data, upload_file, user_to_upload)
        


async def __creating_users():
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