FROM django:19-alpine3.15

WORKDIR /django-ecom-app

COPY . /django-ecom-app
RUN pip install

EXPOSE 3000
CMD ["python","manage.py","runserver"]