FROM python
RUN pip install ddtrace flask
COPY app.py /app/app.py
CMD  [ "/usr/local/bin/ddtrace-run", "python", "/app/app.py" ]
EXPOSE 5050