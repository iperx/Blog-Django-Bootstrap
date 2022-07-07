# Blog-Django-Bootstrap
## Description
This django project is made for educational purposes. It contains: implementation of CRUD operations for posts and tags, authentication, pagination, slugs, snippets.

* Python version is 3.9.13
* Frontend framework - Bootstrap v4.5.2
* Default DBMS - sqlite3
* Django version 4.0

## Installation:
1. Clone this repository to your computer and open the folder

2. Create virtual environment and activate it:  
```python3 -m venv venv && source venv/bin/activate```

3. Install required packages from requirements.txt:  
```pip install -r requirements.txt```

4. Make migrations:  
```./app/blogengine/manage.py makemigrations```

5. Synchronize the database schema with the current set of models:  
```./app/blogengine/manage.py migrate```

6. Create superuser (create an admin account):  
```./app/blogengine/manage.py createsuperuser```

7. Run server:  
```./app/blogengine/manage.py runserver```

8. Log in to your admin account on http://localhost:5000/admin/ to become able to access the admin panel on http://localhost:5000/blog/ (access to CRUD)
