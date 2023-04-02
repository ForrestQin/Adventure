import json


class BuildMap:
	def __init__(self, map_file):
		with open(map_file, 'r') as file:
			self.rooms_data = json.load(file)
			self.rooms = self.create_rooms()
			self.starting_room = self.rooms[0]

	def create_rooms(self):
		rooms = {}
		for idx, room_data in enumerate(self.rooms_data):
			room_id = idx
			name = room_data["name"]
			desc = room_data["desc"]
			nei_exits = {dir: index for dir, index in room_data["exits"].items()}
			items = [item for item in room_data.get("items", [])]
			locked_exits = room_data.get("locked_exits", {})
			winning_items = room_data.get("winning_items", [])
			room = Room(room_id, name, desc, items, nei_exits, locked_exits, winning_items)
			rooms[idx] = room
		return rooms

	def get_room(self, room_id):
		return self.rooms[room_id]


# class Item:
# 	def __init__(self, name, description):
# 		self.name = name
# 		self.description = description
#
# 	def __str__(self):
# 		return self.name
#
# 	def __repr__(self):
# 		return f"Item({self.name}, {self.description})"


class Room:
	def __init__(self, room_id, name, description, items=None, exits=None, locked_exits=None, winning_items=None):
		self.room_id = room_id
		self.name = name
		self.description = description
		self.items = items if items is not None else []
		self.exits = exits if exits is not None else {}
		self.locked_exits = locked_exits if locked_exits is not None else {}
		self.winning_items = winning_items if winning_items is not None else []

	def __str__(self):
		return self.name

	def __repr__(self):
		return f"Room({self.name}, {self.description}, {self.items}, {self.exits}, {self.locked_exits})"

	def unlock_exit(self, direction, inventory):
		if direction in self.locked_exits and inventory.has_item("key"):
			del self.locked_exits[direction]
			return True
		return False

	def lock_exit(self, direction, inventory):
		if direction not in self.locked_exits and direction in self.exits and inventory.has_item("key"):
			self.locked_exits[direction] = True
			return True
		return False

