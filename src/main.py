# All of our imports
import sqlite3

# Step 1 - Setup / Initialize Database
def get_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"Error: {e}")
        raise

# Step 2 - Create a Table in the Database
def create_table(connection):
    query = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        position TEXT NOT NULL,
        nationality TEXT NOT NULL,
        number INTEGER
        )
    """
    try:
        with connection:
            connection.execute(query)
        print("Table was created!")
    except Exception as e:
        print(e)
    
# Step 3 - add User to Database
def insert_user(connection, name:str, age:int, position:str, nationality:str, number:int):
    query = "INSERT INTO users (name, age, position, nationality, number) VALUES (?, ?, ?, ?, ?)"
    try:
        with connection:
            connection.execute(query, (name, age, position, nationality, number))
            print(f"User: {name} was added to your database!")
    except Exception as e:
        print(e)

# Step 4 - Query all users in Database
def fetch_users(connection, condition: str = None) -> list[tuple]:
    query = "SELECT *FROM users"
    if condition:
        query += f" WHERE {condition}"

    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print(e)

# Step 5 - Delete a User from the Database
def delete_user(connection, user_id:int):
    query = "DELETE FROM users WHERE id = ?"
    try: 
        with connection:
            connection.execute(query, (user_id,))
        print(f"USer ID: {user_id} was deleted!")
    except Exception as e:
        print(e)

# Step 6 - Update an existing User
def update_user(connection, user_id:int, position:str):
    query = "UPDATE users SET position = ? WHERE id = ?"

    try:
        with connection:
            connection.execute(query, (position, user_id))
        print(f"User ID {user_id} has a new position of {position}")
    except Exception as e:
        print(e)

# Bonus - Ability to add Multiple Users
def insert_more_users(connection, users:list[tuple[str, int, str, str, int]]):
    query = "INSERT INTO users (name, age, position, nationality, number) VALUES (?, ?, ?, ?, ?)"

    try:
        with connection:
            connection.executemany(query, users)
        print(f"{len(users)} users were added to the database!")
    except Exception as e:
        print(e)

def main():
    connection = get_connection("Players.db")

    try:
        # Create table
        create_table(connection)
        x = int(input("1 - Activate, 2 - freeze: "))
        while x != 2:
            start = input("Enter option (Add, Delete, Update, Search, Add Many): ").lower()
            if start == 'add':
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                position = input("Enter Position: ")
                nationality = input("Enter nationality: ")
                number = int(input("Enter number: "))
                insert_user(connection, name, age, position, nationality, number)

            elif start == 'search':
                print("All Users:")
                for user in fetch_users(connection):
                    print(user)
        
            elif start == "delete":
                user_id = int(input("Enter the User ID: "))
                delete_user(connection, user_id)
        
            elif start == "update":
                user_id = int(input("Enter User ID: "))
                new_position = input("Enter a new position: ")
                update_user(connection, user_id, new_position)
        
            elif start == "add many":
                users = [("Lionel Messi", 36, "Winger", "Argentinian", 10),
                      ("Pedri Gonzalez", 23, "Midfielder", "Spanish", 8),
                      ("Robert Lewandowski", 37, "Striker", "Polish", 9)]
                insert_more_users(connection, users)
            
            x = int(input("1 - Activate, 2 - freeze: "))


    finally:
        connection.close()

        

       

if __name__ == '__main__':
    main()