This is a flask app.

No setup needed.
Run app.py from the home directory to run the app.
The server runs on http://127.0.0.1:5000

/wallet/<:id> endpoint is used for all the transactions with separate HTTP verbs for various actions. 
Postman collection is shared for samples. Requirements file is added.

The wallet server uses a local database SQLite for storing the data. The wallet starts with an initial funding of
atleast the minimum amount to keep the state consistent.

Basic thread locking is used to ensure state consistency.

Transaction records are kept and are returned as soon as a transaction is done on the database.

For the sake of simplicity, the minimum amount is taken as 10 and hardcoded. However, for ease of use and management, it'll be taken from a
database in a real life scenario.
