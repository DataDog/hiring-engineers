#!/bin/bash
docker-compose down
docker rmi -f hiringengineers_web
rm -Rf datadog_lab & rm -f manage.py;
docker-compose run web django-admin startproject datadog_lab .;
cp django_preconfig/* datadog_lab/;
docker-compose up -d;
#docker exec django_container python manage.py migrate;
#docker exec django_container bash -c "echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('presales', 'presales@mdatadoghq.com', 'mypassword')\" | python manage.py shell";
# sleep 2
# clear
# printf "\n\n
# ===============================================
# \nDjango Admin, would shortly open.
# \nPlease user the following credentials:
# \n\nUsername: presales / Password: mypassword
# \n=============================================\n\n";

# sleep 5
# open http://localhost:8000/admin/login/?next=/admin/
# open https://app.datadoghq.eu/
