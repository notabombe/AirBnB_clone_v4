#!/usr/bin/python3
""" Test .get() and .count() methods
"""

from models import storage

print(f"All objects: {storage.count()}")
print(f'State objects: {storage.count("State")}')

first_state_id = list(storage.all("State").values())[0].id
print(f'First state: {storage.get("State", first_state_id)}')
