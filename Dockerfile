FROM python:3.9

WORKDIR /django-ecom-app

COPY . /django-ecom-app
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
#Remember to open port 8000 in Ec2 Instance
