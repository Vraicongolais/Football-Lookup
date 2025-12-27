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
            CREATE TABLE IF NOT EXISTS players(
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


    
class Player:
    def __init__(self, data):
        if isinstance(data, dict):
           self.id = data['id']
           self.name = data['name']
           self.age = data['age']
           self.position = data['position']
           self.nationality = data['nationality']
           self.number = data.get('number')

        elif isinstance(data, tuple):
            self.id = data[0]
            self.name = data[1]
            self.age = data[2]
            self.position = data[3]
            self.nationality = data[4]
            self.number = data[5]

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age} years old, Position: {self.position}, Nationality: {self.nationality}, Number: {self.number}"

    # send constructor objects to dictionary
    def to_dictionary(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Age": self.age, 
            "Position": self.position,
            "Nationality": self.nationality,
            "Number": self.number
        }
    # return what the constructor expects the information to look like
    @classmethod
    def from_dictionary(cls, data):
        return cls({
            'id': int(data["ID"]),
            'name': data["Name"],
            'age': int(data["Age"]),
            'position': data["Position"],
            'nationality': data["Nationality"],
            'number': data["Number"] if data["Number"] else None
        })
    
    def enter_players(self, connection):
        query = "INSERT INTO players (id, name, age, position, nationality, number) VALUES (?,?,?,?,?,?)"
    
        try:
            with connection:
                connection.execute(query, (self.id, self.name, self.age, self.position, self.nationality, self.number))
            print(f"{self.name} was added to your database")
    
        except Exception as e:
            print(e)

def fetch_players(connection, condition: str = None) -> list[tuple]:
    query = "SELECT * FROM  players"
    if condition:
        query += f"WHERE {condition}"
    
    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
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
            options = input("Enter option: (Add player, Search player, close): ").lower()

            if options == "add":
                player_id = int(input("Enter the player ID: "))
                player_data = client.get_players(player_id)
                if player_data and player_data['response']:
                    player_list = player_data['response'][0]['player']
                    player_info = Player(player_list)
                    player_info.enter_players(connection)

            elif options == "search":
                print("All Players: ")
                for player in fetch_players(connection):
                    print(player)
            
            elif options == "close":
                break
    
    finally:
        connection.close()

if __name__ == '__main__':
    main()

