import json

# Function to save game data
def save_game_json(filename, game_state):
    with open(filename, 'w') as save_file:
        json.dump(game_state, save_file)

# Function to load game data
def load_game_json(filename):
    try:
        with open(filename, 'r') as save_file:
            return json.load(save_file)
    except FileNotFoundError:
        return None

# Example usage  
game_state = {
  'player_score': 100, 
  'level': 3, 
  'inventory': ['sword', 'potion']
}

save_game_json('my_save_game.json', game_state)
loaded_state = load_game_json('my_save_game.json') 

import csv

# Save high scores
def save_high_scores_csv(filename, high_scores):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Score'])  # Write header row
        for name, score in high_scores:
            writer.writerow([name, score])

# Load high scores        
def load_high_scores_csv(filename):
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            return [(name, int(score)) for name, score in reader]
    except FileNotFoundError:
        return []  # Return empty if no file
