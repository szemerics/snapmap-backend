from bson import ObjectId
from app.models.photo import Comment, CreatePhoto, Location
from app.models.additional_data import Camera, Gear, Settings
from app.models.user import UserSummary
from datetime import datetime
from typing import List, Optional


class PhotoEntry():
    def __init__(self, file_path: str, user_id: ObjectId, data: CreatePhoto, init_id: str, likes: int = 0, comments: Optional[List[Comment]] = None):
        self.file_path = file_path
        self.user_id = user_id
        self.data = data
        self.init_id = init_id
        self.likes = likes
        self.comments = comments or []


def get_photo_entries(default_user, moderator_user, admin_user) -> List[PhotoEntry]:
    """Get the list of photo entries to upload during initialization."""
    photo_entries: List[PhotoEntry] = []

    photo_entries.append(PhotoEntry(
        'src/app/utils/init/lib/photos/csepel.jpg',
        default_user.id,
        CreatePhoto(
            location=Location(
                lat=47.444531981994814,
                lng=19.07154301874141
            ),
            date_captured=datetime.now(),
            category='trainspotting',
            gear=Gear(
                camera=Camera(
                    brand='Nikon',
                    model='D3500',
                    type='DSLR'
                ),
                lens='AF-P DX NIKKOR 18-55mm f/3.5-5.6G VR',
                extra_attachment='ND Filter'
            ),
            settings_used=Settings(
                iso=100, 
                shutter_speed='1/1000s', 
                aperture='f/1.8'
                ),
            caption='A beautiful day at Csepel station.'
        ),
        init_id='csepel',
        likes=10,
        comments=[Comment(
            user_summary=UserSummary(
                user_id=moderator_user.id,
                username=moderator_user.username,
                profile_picture_url=moderator_user.profile_picture_url,
                bio=moderator_user.bio
            ),
            comment_date=datetime.now(),
            content='Great shot!',
            likes=2,
            replies=[Comment(
                user_summary=UserSummary(
                    user_id=default_user.id,
                    username=default_user.username,
                    profile_picture_url=default_user.profile_picture_url,
                    bio=default_user.bio
                ),
                comment_date=datetime.now(),
                content='I agree, stunning view!',
                likes=1
            )]
        )]
    ))

    photo_entries.append(PhotoEntry(
        'src/app/utils/init/lib/photos/miskolc.jpg',
        moderator_user.id,
        CreatePhoto(
            location=Location(
                lat=48.09937752341158,
                lng=20.77555906988592
            ),
            date_captured=datetime.now(),
            category='street',
            gear=Gear(
                camera=Camera(
                    brand='Canon',
                    model='EOS 250D',
                    type='DSLR'
                ),
                lens='EF-S 18-55mm f/4-5.6 IS STM',
                extra_attachment=None
            ),
            settings_used=Settings(
                iso=200,
                shutter_speed='1/500s',
                aperture='f/2.8'
            ),
            caption='Exploring the streets of Miskolc.'
        ),
        init_id='miskolc',
        likes=42,
        comments=[Comment(
            user_summary=UserSummary(
                user_id=admin_user.id,
                username=admin_user.username,
                profile_picture_url=admin_user.profile_picture_url,
                bio=admin_user.bio
            ),
            comment_date=datetime.now(),
            content='Nice composition!',
            likes=1,
        )]
    ))

    photo_entries.append(PhotoEntry(
        'src/app/utils/init/lib/photos/szeged.jpg',
        admin_user.id,
        CreatePhoto(
            location=Location(
                lat=46.25372456930462,
                lng=20.14891582649533
            ),
            date_captured=datetime.now(),
            category='street',
            gear=Gear(
                camera=Camera(
                    brand='Sony',
                    model='Alpha a7 IV',
                    type='Mirrorless'
                ),
                lens='FE 24-70mm f/2.8 GM II',
                extra_attachment='DJI Ronin-S Gimbal'
            ),
            settings_used=Settings(iso=100, shutter_speed='1/200s', aperture='f/1.8'),
            caption='Sunset vibes in Szeged.'
        ),
        init_id='szeged',
        likes=2
    ))

    photo_entries.append(PhotoEntry(
        'src/app/utils/init/lib/photos/sopron.jpg',
        admin_user.id,
        CreatePhoto(
            location=Location(
                lat=47.6866944,
                lng=16.5912778
            ),
            date_captured=datetime.now(),
            category='landscape',
            gear=Gear(
                camera=Camera(
                    brand='Fujifilm',
                    model='X-T30 II',
                ),
                lens='XF 18-55mm f/2.8-4 R LM OIS',
                extra_attachment=None
            ),
            settings_used=Settings(
                iso=400,
                shutter_speed='1/125s',
                aperture='f/4.0'
            ),
            caption='Foggy morning over Sopron.'
        ),
        init_id='sopron',
        likes=17,
        comments=[
            Comment(
                user_summary=UserSummary(
                    user_id=moderator_user.id,
                    username=moderator_user.username,
                    profile_picture_url=moderator_user.profile_picture_url,
                    bio=moderator_user.bio
                ),
                comment_date=datetime.now(),
                content='Those tones are unreal.',
                likes=3,
                replies=[
                    Comment(
                        user_summary=UserSummary(
                            user_id=admin_user.id,
                            username=admin_user.username,
                            profile_picture_url=admin_user.profile_picture_url,
                            bio=admin_user.bio
                        ),
                        comment_date=datetime.now(),
                        content='Right? This makes me want to visit Sopron.',
                        likes=1
                    )
                ]
            ),
            Comment(
                user_summary=UserSummary(
                    user_id=default_user.id,
                    username=default_user.username,
                    profile_picture_url=default_user.profile_picture_url,
                    bio=default_user.bio
                ),
                comment_date=datetime.now(),
                content='Shot this handheld with no filters.',
                likes=0
            )
        ]
    ))
    photo_entries.append(PhotoEntry(
        'src/app/utils/init/lib/photos/gyor.jpg',
        moderator_user.id,
        CreatePhoto(
            date_captured=datetime.now(),
            category='city',
            gear=Gear(
                camera=Camera(
                    brand='Canon',
                    model='EOS R6',
                ),
                lens='RF 24-70mm f/2.8L IS USM',
                extra_attachment='Polarizing Filter'
            )
        ),
        init_id='gyor'
    ))

    photo_entries.append(PhotoEntry(
        'src/app/utils/init/lib/photos/deg.jpg',
        admin_user.id,
        CreatePhoto(
            location=Location(
                lat=46.874836,
                lng=18.433508
            ),
            date_captured=datetime.now(),
            category='automotive',
            gear=Gear(
                camera=Camera(
                    brand='Nikon',
                    model='Z6 II',
                    type='Mirrorless'
                ),
                lens='NIKKOR Z 24-70mm f/2.8 S',
                extra_attachment='Polarizing Filter'
            ),
            settings_used=Settings(
                iso=320,
                shutter_speed='1/250s',
                aperture='f/2.8'
            ),
            caption='Heavily modified BMW E30 at sunset during the IDOLZ event at Festetics Kastély in Dég.'
        ),
        init_id='deg',
        likes=8
    ))

    return photo_entries
