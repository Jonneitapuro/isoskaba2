#!/bin/sh


activate () {
      . .env/bin/activate
}
clear

echo "This is a script that does the following things:"
echo "* activate virtualenv"
echo "* run Django migrations"
echo "* start Django devserver"
echo "* deactivate virtualenv"

activate
python manage.py makemigrations --merge
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
deactivate
