# re_2023_t1
RE 2023 Project T1

This project is writen in Python 3.10.6, and can be executed in python 3.^10.^6

The objective of this project is develop a system for a fictional hardware store, a CRUD of products and category.
## Instalation prerequisites
This project requires [Python 3.10](https://www.python.org/) or newer and `pip 8.x.x`.

Install venv package with `python3 -m pip install venv`
## Instalation

1. Create a virtual enviroment using the next command:

    `python3 -m venv env`.
    
    This will create a virtual enviroment called env.

2. Activate the virtual enviroment 
    ### Windows 
    `.\env\Scripts\activate.bat`

    ### Linux and Mac OS
    `source ./env/bin/activate`
3. Clone the repo using git
4. Enter the directory
5. Install dependencies

    `pip install -r requirements.txt`
6. Generate the database migrations

    `python manage.py migrate`

7. Create a superuser account (This will be used for logging in).

    `python manage.py createsuperuser`
8. Run the webscrapping script (Optional).

    `python manage.py articles`
9. Run the server on the desired port (Default: 127.0.0.1:8000)

    `python manage.py runserver [port]`
## ENJOY
This project was developed by:
- David Cano
- Brandon Venegas
- Leonardo Pantoja
- Fernando Ponce
