[![Build Status](https://travis-ci.org/nishanthvijayan/ERP.svg?branch=master)](https://travis-ci.org/nishanthvijayan/ERP)
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


