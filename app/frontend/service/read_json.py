import json

class ReadJSON:
    def __init__(self, file_path):
        self.file_path = file_path

    def json_to_list(self):
        # Read the JSON file and return the list of valid item IDs.
        with open(self.file_path, 'r') as file:  # Open the JSON file for reading
            data = json.load(file)  # Load the JSON data into a dictionary
        return data['valid_item_ids']  # Return the list of valid item IDs