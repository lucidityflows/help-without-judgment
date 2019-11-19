**Help Without Judgment README.md**

*How to Clone*

- Clone to Pycharm using the git url
- Setup as a python project named 'hwj'
	- Make sure to use a python 3.6+ interpreter w/a virtual envirnonment
	- Check that you select ok to run the browser at 'http://127.0.0.1:8000/'
- Get your SECRET KEY and paste it in the appropriate spot in settings.py
- Go to the PyCharm project terminal after the project is set up.
	- You are in an activate virtual environment if there are () around your virtual environment name (ex. (venv))
- Do: 'pip3 install --upgrade pip (you may have to do this a few times to get it updated
- Do: 'pip3 install django'
- Do: 'pip3 install mysqlclient'
- Do: 'pip3 install channels'
- Do: 'brew install redis' (you may have to download redis and install for real server)
- Do: 'pip3 install pytz'

- Go the folder with manage.py
	- Do: python3 manage.py migrate (you will do this anytime you change anything)
	- Do: python3 manage.py runserver
- All done!

*When you make changes to models or the database, 'python3 manage.py migrate', and then 'python3 manage.py runserver'