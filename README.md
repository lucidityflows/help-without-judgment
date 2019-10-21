**Help Without Judgment README.md**

*How to Clone**

- 1. Clone to Pycharm using the git url
- 2. Setup as a python project named 'hwj'
	- Make sure to use a python 3.6+ interpreter w/a virtual envirnonment
	- Check that you select ok to run the browser at 'http://127.0.0.1:8000/'
- 3. Get your SECRET KEY and paste it in the appropriate spot in settings.py
- 4. Go to the PyCharm project terminal after the project is set up.
	- You are in an activate virtual environment if there are () around your virtual environment name (ex. (venv))
- 5. Do: 'pip3 install --upgrade pip (you may have to do this a few times to get it updated
- 6. Do: 'pip3 install django'
- 7. Do: 'pip3 install mysqlclient'
- 8. Go the folder with manage.py
	- Do: python3 manage.py migrate (you will do this anytime you change anything)
	- Do: python3 manage.py runserver 
- 9. All done!

*When you want to check your changes locally repeat step 8 again