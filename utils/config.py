import json
import os

# Import values from config file
with open("config.json") as json_file:
    for key, value in json.load(json_file).items():
        locals()[key.strip().upper()] = value.strip() if type(value) == str else value

# Import values from ENV (overwrite config file)
for key, value in os.environ.items():
    locals()[key.strip().upper()] = value.strip()
