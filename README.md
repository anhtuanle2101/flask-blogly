# flask-blogly

## Install required dependencies using pip
    pip3 install -r requirements.txt

## Create the correct Postgres database and check if the database exists
    createdb blogly
    psql
    \c blogly

## Run the seed.py to populate the seeds into the database
    python3 seed.py
    
## Run the flask app
    flask run
    
## Then go to the URL 'localhost:5000'
    
