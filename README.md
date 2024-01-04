# Application in Django

Se debe declarar la variable DJANGO_SETTINGS_MODULE en el ambiente, con el valor correspondiente para que apunte al archivo de settings correspondiente. De esa manera se puede correr la app directamente con el comando
*python manage.py runserver*

Running the docker:

docker run -dp 8000:8000 workwiseapp

Define the settings filename with the environment variable:

`export DJANGO_SETTINGS_MODULE=app.settings_dev_local`


## Requisitos
Python 3.11.x o superior
Django 4.2.8 o superior
PostgreSQL 14.x o superior
