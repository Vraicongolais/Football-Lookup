# Programmer : Landry 
# Football-Lookup
import sqlite3
import requests

def get_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"Error: {e}")
        raise

def create_table(connection):
    query = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
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

class API_Client:
    BASE_URL = "https://v3.football.api-sports.io/"

    def __init__(self, API_KEY):
        self.headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
    
    def get_players(self, player_id):
        endpoint = f"{self.BASE_URL}/players/profiles"
        params = {"player": player_id}
        player_response = requests.get(endpoint, headers=self.headers, params=params)

        if player_response.status_code == 200:
            player_data = player_response.json()
            return player_data
        else:
            print(f"Failed to retrieve data {player_response.status_code}")


def enter_players(self, connection):
    query = "INSERT INTO players (id, name, age, position, nationality, number) VALUES (?,?,?,?,?,?)", (self.id, self.name, self.age, self.position, self.nationality, self.number)
    
    try:
        with connection:
            connection.execute(query, (id, self.name, self.age, self.position, self.nationality, self.number))
            print(f"{self.name} was added to your database")
    
    except Exception as e:
        print(e)

    
def main():
    API_KEY = ""
    client = API_Client(API_KEY)
    connection = get_connection("Players.db")
    done = False

    try:
        create_table(connection)
        while not done:
            options = input("Enter option: (Add player, Search player): ").lower()

            if options == "add":
                player_id = int(input("Enter the player ID: "))
                player_data = client.get_players(player_id)
                enter_players(connection,)

            elif options == "search":
                break
    
    finally:
        connection.close

if __name__ == '__main__':
    main()

