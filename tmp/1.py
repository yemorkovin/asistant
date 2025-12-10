import json

with open('../data.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
print(config)
