# Flaskblog

This repository created for learning Flask framework by building blogging web application. The application is deployed to Heroku and can be accessed via this address: https://aman-flask-blog.herokuapp.com/home.

## Installation

To run the applicatin in local environment. Make directory flaskblog [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
$ mkdir flaskblog
$ cd flaskblog
```
Create virtual environment with built in python venv module and activate it
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```
Clone the repository with command:
```bash
(venv)$ git clone git@github.com:amangeldyshalginbayev/Blogging_Application.git
```
Install all dependencies of the project via pip:
```bash
(venv)$ pip install requirements.txt
```
You can check all installed dependencies via command
```bash
(venv)$ pip list
```
To run the project you need to create development_config.cfg file inside flaskblog package with the following values:

flaskblog/development_config.cfg
```bash
SECRET_KEY=''
SQLALCHEMY_DATABASE_URI=''
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER=''
MAIL_PORT=
MAIL_USE_TLS=
MAIL_USERNAME=''
MAIL_PASSWORD=''
MAIL_DEFAULT_SENDER =('Flask Blog', 'flaskblog-noreply@demo.com')
MESSENTE_API_USERNAME=''
MESSENTE_API_PASSWORD=''
```
For security reasons, this file excluded from version control and used only for local development.

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)