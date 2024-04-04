# Krish Dhansinghani

# Ticket-API-Mini-Project
A mini ticker api project to lookup, find min price, and max price of given stock ticker

# Instructions:

1. make sure you cd into the main tickerProject directory (the one that contains both the solution directory and second tickerProject directory)
2. make sure dependencies are installed
   - run:
     pip install -r requirements.txt - if that doesnt work the requirements.txt file has all dependencies
3. make sure all database migrations are made

   - run:
     python manage.py makemigrations
     python manage.py migrate

   - if you want to check the database run:
     python manage.py createsuperuser - follow instructions then go to this site and login:
     http://localhost:8000/admin/

4. to view the code and the api calls you can go to these files where comments will show my process

   - for the api calls and data class go to the solutions directory and look at:
     views.py
     urls.py
   - to see database model for stock data go to the solutions directory and look at:
     models.py
   - to see the settings for the project go to the second tickerProject directory and look at:
     settings.py
   - to see the problem statement go to:
     problems.md

5. run django server in tickerProject directory (the one that contains both the solution directory and second tickerProject directory)

   - run:
     python manage.py runserver

6. test each api call using the following format:

   - run:
     curl http://localhost:8000/api/v1.0/lookup/TSLX/2024-02-22/
     curl http://localhost:8000/api/v1.0/min/TSLX/20/
     curl http://localhost:8000/api/v1.0/max/TSLX/20/

   - for lookup:
     - you can replace "TSLX" with a stock symbol of your choice
   - for min and max
     - you can replace "TSLX" with a stock symbol of your choice
     - you can replace "20" with a int or range of your choice

