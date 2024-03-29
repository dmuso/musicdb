# Music DB

A simple Django app to manage a sheet music database.

## Notes and Feature Requests

* Add images of book
* Find catalogue numbers that are not used
* Add barcode field
* Add notes by teacher
* Add/protect notes by library staff

## Common Commands

    # Start app server
    docker-compose up app

    # Start standalone database server
    docker-compose up -d db

    # Run tests
    docker-compose run test

    # Generate migrations
    docker-compose run app python manage.py makemigrations piece

    # Apply migrations
    docker-compose run app python manage.py migrate

    # Console CLI
    docker-compose run app python manage.py shell

    # Create superuser
    docker-compose run app python manage.py createsuperuser

    # Executing the import script
    docker-compose exec -T app python manage.py shell < import-all.py
