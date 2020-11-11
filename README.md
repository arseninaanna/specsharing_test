
Run web server
```bash
python manage.py runserver
```

Run Celery beat
```bash
celery -A specsharing_test beat -l info
```

Run Celery worker
```bash
celery -A specsharing_test worker --scheduler django --loglevel=info
```