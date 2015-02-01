# django-dbmgmt #
Database Management through manage.py

### What is django-dbmgmt? ###

ORMs are great, but sometimes more custom SQL is needed to return the data your project needs. `django-dbmgmt` is a Django [manage.py command](
https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/) written to manage and track database stored procedures, functions and tasks as part of your Django project.

### Setup ###

Create a directory in your Django project where you would like to store your SQL files:

    mkdir myproject/sql

In your project's `settings.py` file, assign the directory to the `SQL_DIR` variable:

    SQL_DIR = os.path.join(BASE_DIR, 'sql')
    
Now navigate to any of your project's app directories and extract the `django-dbmgmt` code. The directory structure should look like this:

    myproject/myapp/management/commands/dbmgmt.py
    
### SQL Files ###

In your `myproject/sql folder`, store text files of the database stored procedures, functions and/or tasks you would like to be uploaded to the database used in your Django project. For example the following PostgreSQL function could be stored as `myproject/sql/firstnames.sql`:

    CREATE OR REPLACE FUNCTION
        firstnames(lastname character varying)
        RETURNS TABLE (
          firstname varchar(120)
        )
        AS
        $$
        BEGIN
        RETURN QUERY
        EXECUTE 'select firstname from 
                  names where lastname = $1'
        USING lastname;
        END
        $$ language plpgsql;
        
For functions and stored procedures, it is recommended to use the `CREATE OR REPLACE` syntax.        

### Usage ###

To upload a function to the database, pass the filename without an extension to `manage.py dbmgmt`:

    manage.py dbmgmt firstnames
    
More than one file can also be passed in one command:

    manage.py dbmgmt firstnames otherfunction
    
You can also run all of the SQL files in the folder by passing `--all`:

    manage.py dbmgmt --all
    
### Goal ###

The goal of `django-dbmgmt` is to keep database queries and code in your Django project and trackable in version control. Integration into `manage.py` also makes handling this database code a bit more streamlined.

### Other usage ideas ###

- Common DBA tasks (`VACUUM`, `REINDEX`, etc.)
- Running database reports
- Managing data updates


#### Written and tested with: ####

Python 3.4

Django 1.7

PostgreSQL 9.4
