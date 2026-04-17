# Funções para ler/escrever em ficheiro (JSON ou CSV)
import json

# Create template for saving the data
data = {"passengers": [], "flights": [], "tickets": []}


# Function to read json files
def load_data():
    """Try to open the file, if not create it"""

    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("database.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Database created")
        return data.copy()


# Function to save json
def save_data(data):
    """Save data to JSON file"""

    with open("database.json", "w") as f:
        json.dump(data, f, indent=2)
