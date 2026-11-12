# Game library

Project work for the University of Helsinki's Introduction to Cyber Security
course. Based on [Pelikirjasto](https://github.com/iita-mari/pelikirjasto).


## Installation and running
### Linux
1. Create and activate a virtual environment:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Install Flask:
```
$ pip install flask
```

3. Initialize the database:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

4. Start the application:
```
$ flask run
```
### macOS
1. Create and activate a virtual environment:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Install Flask:
```
$ python -m pip install flask
```

3. Initialize the database:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

4. Start the application:
```
$ flask run
```
### Windows

1. Create and activate a virtual environment:

   ```
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install Flask:

   ```
   python -m pip install flask
   ```

3. Initialize the database:

   ```
   Get-Content schema.sql | sqlite3 database.db
   Get-Content init.sql | sqlite3 database.db
   ```

4. Start the application:

   ```
   flask run
   ```