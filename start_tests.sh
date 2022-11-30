pip install -r tests/functional/requirements.txt

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 1
done

cd tests/functional

pytest src