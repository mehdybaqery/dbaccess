import mysql.connector
from termcolor import colored
import os

# Define colors for output
RED = 'red'
GREEN = 'green'
BLUE = 'blue'
YELLOW = 'yellow'
CYAN = 'cyan'
NC = None  # No Color

# MySQL credentials
CREDENTIALS_FILE = "/path/to/secure/.my.cnf/.p"

# Check if the credentials file exists
if not os.path.isfile(CREDENTIALS_FILE):
    print(colored("Credentials file not found. Exiting.", RED))
    exit(1)

# Read credentials from the file (implementing a simple logic here, could be more sophisticated based on your needs)
def read_credentials():
    with open(CREDENTIALS_FILE, 'r') as f:
        return f.read().strip()

# Get MySQL credentials (username, password, host, etc.)
mysql_credentials = read_credentials()

# Prompt user to select a database
print(colored("Which database do you want to use?", CYAN))
print(colored("1. db1", YELLOW))
print(colored("2. db2", YELLOW))

choice = input("Enter the number corresponding to your choice: ")

# Determine the selected database
if choice == '1':
    DATABASE = "db1"
elif choice == '2':
    DATABASE = "db2"
else:
    print(colored("Invalid choice. Exiting.", RED))
    exit(1)

print(colored(f"You selected database: {DATABASE}", GREEN))

# Connect to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            user=mysql_credentials,
            host='localhost',  # Replace with your MySQL server address
            database=DATABASE
        )
        return connection
    except mysql.connector.Error as err:
        print(colored(f"Error: {err}", RED))
        exit(1)

# Display all tables in the selected database
def list_tables(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(colored(f"Listing all tables in {DATABASE}:", CYAN))
        for table in tables:
            print(table[0])
    except mysql.connector.Error as err:
        print(colored(f"Failed to retrieve tables. Exiting.\nError: {err}", RED))
        exit(1)
    finally:
        cursor.close()

# Continuously prompt user for SQL queries
def run_sql_queries(connection):
    while True:
        query = input(colored(f"Enter the SQL query to run on {DATABASE} (or type 'exit' to quit): ", CYAN))

        if query.lower() == 'exit':
            print(colored("Exiting the script. Goodbye!", BLUE))
            break

        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print(colored("Query executed successfully.", GREEN))
        except mysql.connector.Error as err:
            print(colored(f"Failed to execute the query. Error: {err}", RED))
        finally:
            cursor.close()

# Main flow
connection = connect_to_database()
list_tables(connection)
run_sql_queries(connection)
connection.close()

