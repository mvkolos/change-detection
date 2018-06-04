FROM aeronetlab/prod:gpu

## Additional packages etc.

RUN pip install flask

## App

ADD . /change-detection

WORKDIR /change-detection

CMD ["python3","app.py"]