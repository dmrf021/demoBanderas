import os
import json

def create_flags_json():
    # Directory containing the flag images
    flags_dir = "assets/banderas"
    
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Dictionary to store country-flag mappings
    flags_dict = {}
    
    # Get all files in the flags directory
    for filename in os.listdir(flags_dir):
        if filename.endswith(".png") or filename.endswith(".svg"):
            # Get country name from filename (remove extension and capitalize)
            country_name = filename.split('.')[0].capitalize()
            # Create the path
            flag_path = f"{flags_dir}/{filename}"
            # Add to dictionary
            flags_dict[country_name] = flag_path
    
    # Write to JSON file
    with open("data/flags.json", "w", encoding="utf-8") as f:
        json.dump(flags_dict, f, indent=4)

if __name__ == "__main__":
    create_flags_json()