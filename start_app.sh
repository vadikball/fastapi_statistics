while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

gunicorn main:app --preload --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010