FROM python:3.9.15

WORKDIR /app
RUN pip3 install discord --no-cache-dir
RUN pip3 install requests --no-cache-dir
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["app.py"]
