#!/bin/bash

echo "arg:${1}"

if [ "${1}" = "--develop" ];then
    SETTINGS="amazon_web.settings_dev"
else
    SETTINGS="amazon_web.settings"
fi

echo $SETTINGS

python manage.py makemigrations --settings $SETTINGS
python manage.py migrate --settings $SETTINGS
