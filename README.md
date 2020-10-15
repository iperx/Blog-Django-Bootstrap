# Blog-Django-Bootstrap
## Description
This django project is made for educational purposes. It contains: implementation of CRUD operations for posts and tags, pagination, slugs, simple search engine and snippets. This application is not perfect, but it works.

* Python version is 3.5.2
* Frontend framework - Bootstrap v4.5.2
* Default DBMS - sqlite3
* Django version 2.2.13
## Installation:
1. Clone this repository to your computer and open the folder
2. Install _pipenv_:  
```pip install pipenv```
3. Install required packages using pipenv (keep staying in the root folder of the project):  
```pipenv install```
4. Launch virtual environment:  
```pipenv shell```
5. Synchronize the database state with the current set of models and migrations:
```./app/blogengine/manage.py migrate```
6. Create superuser (create an admin account):
```./app/blogengine/manage.py createsuperuser```
7. Run server:
```./app/blogengine/manage.py runserver 5000```
8. Log in to your admin account on 'http://localhost:5000/admin/' to access the admin panel (access to CRUD)