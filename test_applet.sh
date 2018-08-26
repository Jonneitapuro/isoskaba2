#!/bin/sh


activate () {
      . .env/Scripts/activate
}
clear

echo "This is a script that does the following things:"

echo "* activate virtualenv"
activate
echo "* run Django migrations"
python manage.py makemigrations --merge
python manage.py makemigrations
python manage.py migrate
echo "* start Django devserver"
python manage.py runserver
echo "* deactivate virtualenv"
deactivate
