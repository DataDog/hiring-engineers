FROM python:3.5
ADD main.py /
RUN pip install datadog ddtrace flask
ENTRYPOINT [ "ddtrace-run" ]
CMD [ "python3", "main.py" ]
