virtualenv -p /usr/bin/python2.7 env &&
source env/bin/activate &&
pip install -r requirements.txt &&
python civ/manage.py runserver 127.0.0.1:8000