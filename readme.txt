1.Clone the Project:
    git clone <git url>
2.Install Django and Django REST Framework:
    pip install django
    pip install djangorestframework
3.Install Project Dependencies:
    pip install -r requirements.txt
4.Run the Project:
    python manage.py runserver
    access the project using url: http://127.0.0.1:8000
    -------------
    if default port not working or no access use custom port and runserver using below command
        python manage.py runserver <port_number>
        EX: python manage.py runserver 8080
        access the project using url: http://127.0.0.1:8080

To access APIs, use the bearer token "rajaramesh". You can utilize the Swagger UI available at <base_url>/docs/. This interface allows you to interact with all APIs, including their requests and responses. When using Swagger for authentication, remember to prepend "Bearer" before the token, like so: "Bearer rajaramesh".

In Swagger, there is a detailed explanation or description of APIs available. Please refer to it.