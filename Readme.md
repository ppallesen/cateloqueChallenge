# The catalogue challenge

## Setup
Install python 3.9 or later on your machine

then run 
`pip install -r requirements.txt`

To test the app run `uvicorn main:app`

and go to `http://localhost:8000/docs` to get an overview of the app and to test it

To run the tests run `pytest`

## Design choices
In order to make the smallest MVP I choose to not make a SQL-database. Since it wasn't needed to fullfill the requirements of the challenge. 

I made the most minimalistic file setup, since I can refactor it later

I choose FastApi because it gives auto-documentation

I choose to use pytest from the start, because it is just faster and easier to develop backend with automated tests
