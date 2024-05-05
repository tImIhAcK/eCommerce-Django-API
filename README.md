# Django E-Commerce Backend API

To Start

> Create virtual enviroment

```
python -m venv <vitual envinromrnt name>
```

> Activate virtual enviroment,

```
source <vitual envinromrnt name>/bin/activate # Linux
\venv\Scripts\activate # Windows
```

> Install requirements

```
pip install -r requirements.txt
```

> Make migrations

```
python manage.py makemigrations
python manage.py migrate
```

> Create superuser

```
python manage.py createsuperuser
```

> Execute the following command in the shell to start the RabbitMQ server with Docker:

```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672
rabbitmq:management
```

> Open another shell and start the Celery worker from project directory with the following command:

```
celery -A myshop worker -l info
```

> Start server

```
python manage.py runserver
```
