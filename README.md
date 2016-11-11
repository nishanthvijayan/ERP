# ERP

## Installation and set-up  
  
Install Django (preferably 1.10.0+)  
  
`sudo pip install django`
  
    
Clone/Download this repository and cd into the project  
  
To setup the database run
```
python manage.py makemigrations forms
python manage.py migrate
```

Now, to run the app  
`python manage.py runserver`  
  
If everything went weel upto this point, go to http://127.0.0.1:8000/forms/  to see the app running
  
### Django Admin
Currently there is no proper CRUD interface for any of the models. So to see the app in action use Django Admin interface to add items manually.
To use Django admin, a superuser should be create via the command line.
  
`python manage.py createsuperuser`   
  
Once the superuser has been created you can log into the Admin interface by visiting http://127.0.0.1:8000/admin with the server running


