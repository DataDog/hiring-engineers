# This is for deployment inside Pycharm
# from https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html
FROM python:3.8.1

WORKDIR /app

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY .. /app
EXPOSE 8000
# for Django: CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
