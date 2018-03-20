__author__ = 'shy'
__date__ = '2018/3/20 10:41'

INSTALLED_APPS = (
    # Using the Django ORM/Cache as a result backend; python manage.py migrate django_celery_results;
    'django_celery_results',

    # Stores the schedule in the Django database, and presents an admin interface to manage periodic tasks at runtime; \
    # python manage.py migrate django_celery_beat;\
    # celery -A proj beat -l info -S django;\
    # Visit the Django-Admin interface to set up some periodic tasks;\
    # Start celery beat and worker
    'django_celery_beat',
)

CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'

