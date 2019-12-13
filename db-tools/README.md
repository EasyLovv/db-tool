# DB-Tool

## Easy test
1. Navigate to project root directory
2. type `docker-compose run client bash` this command will run the database container and the client container which would have everything needed for testing.
3. The opened container would be ready for testing
4. To access to the project use `dbtool` from the command line. 

##Examples:
Create database:

`dbtool -h database -p 5432 -d dbtool --password dbtool --user dbtool create_db`

Fill the database from files located n the `/r3/` directory:

`dbtool -h database -p 5432 -d dbtool --password dbtool -u dbtool --threads 4 --bulk_size 500 load /r3/`

To see all posible options:

`dbtool --help`

 project is suitable for setuptools, so you could install it locally with pip globally:
`pip install /path/to/project`
or in editable mode:
`pip install -e /path/to/project`
