# ERP

## Installation and set-up

Follow the below mentioned steps :
  
1. Install Django (preferably 1.10.0+)  
  
	`sudo pip install django`

2. Install django-positions (version 0.5.4)  
  
	`sudo pip install django-positions`
    
3. Now, clone or download this repository

	`git clone https://github.com/nishanthvijayan/ERP.git`

Done. Installation is complete
  
To setup the database, cd into the project folder and run
```
python manage.py makemigrations
python manage.py migrate
```

Now, to run the app  
`python manage.py runserver`  
  
If everything went weel upto this point, go to http://127.0.0.1:8000/forms/  to see the app running


