Before running this application (and after installing django) you have to copy the .env.temp file and rename it to .env
then generate and paste inside new SECRET_KEY using following command
```
python -c 'from django.core.management.utils import get_random_secret_key; \
            print(get_random_secret_key())'
```

commands

```
pip install -r requirements.txt

python manage.py migrate  # use this command to create database file
python manage.py createsuperuser 
python manage.py runserver 0.0.0.0:8000
```