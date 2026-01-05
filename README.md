## Installation

1. Create python virtual environment

```
python3.13 -m venv .venv
```

2. Activate venv and install dependencies

```
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create .env file in the root folder and insert the followings

```
MONGODB_URI = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.10'
DATABASE_NAME = 'snapmap_db'
```

You can get your connection string from your terminal after connecting with the 'mongosh' command.
Make sure that your mongo service is running.

4. Run the initialization script

```
python src/app/utils/init/create_init_state.py
```

5. Finally start project

```
fastapi dev src/main.py
```
