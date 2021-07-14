export ENV='test'

echo 'Drop tables'
python manage.py db downgrade
echo 'Create tables'
python manage.py db upgrade
echo 'Seed database'
python manage.py seed
echo 'Data seeded. Begin testing...'
python test_app.py