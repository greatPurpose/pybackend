# Protecton backend

### Run tests and flake8:

    docker-compose run --rm app sh -c "coverage run manage.py test && coverage report && coverage html && flake8"

And then you can open htmlcov/index.html to view the detailed coverage report.

### Create superuser:

    docker-compose run --rm app sh -c "python manage.py createsuperuser"
