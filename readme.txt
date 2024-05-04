1.Clone the Project:
    git clone <git url>
2.Install Django and Django REST Framework:
    pip install django
    pip install djangorestframework
3.Install Project Dependencies:
    pip install -r requirements.txt
4.Update Database Configuration:
    Navigate to the VendorManagement/settings.py file in your Django project.
    Locate the DATABASES setting.
    Update the database configuration, change the database engine (ENGINE), database name (NAME), username (USER), password (PASSWORD), host (HOST), and port (PORT).
5.Generate Migrations:
    python manage.py makemigrations
    already migrations are there in code, if any error got just skip it and follow next step.
6.Apply Migrations:
    python manage.py migrate
7.Run the Project:
    python manage.py runserver
    access the project using url: http://127.0.0.1:8000
    -------------
    if default port not working or no access use custom port and runserver using below command
        python manage.py runserver <port_number>
        EX: python manage.py runserver 8080
        access the project using url: http://127.0.0.1:8080
8.Documentation
    You can utilize the Swagger UI available at <base_url>/docs/. This interface allows you to interact with all APIs, including their requests and responses. When using Swagger for authentication, remember to prepend "Bearer" before the token, like so: "Bearer rajaramesh". To access APIs, use the bearer token "rajaramesh". Additionally, you can add new tokens in VendorManagement/settings.py (TOKENS).
    In Swagger, there is a detailed explanation or description with request and responce of APIs available. Please refer to it.
