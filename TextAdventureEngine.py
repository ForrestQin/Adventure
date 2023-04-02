import sys


class TextAdventureEngine:
	def __init__(self, game_map):
		self.is_game_over = False
		self.game_map = game_map
		self.current_room = self.game_map.starting_room
		self.inventory = []
		self.show_room = True

	def process_command(self, command):
		command_array = command.lower().split()

		verb = command_array[0]
		verb_map = {
			"go": "go",
			"get": "get",
			"look": "look",
			"inventory": "inventory",
			"quit": "quit",
			"help": "help",
			"drop": "drop",
			"lock": "lock",
			"unlock": "unlock"
		}
		direction_map = {
			"north": "north",
			"south": "south",
			"east": "east",
			"west": "west",
			"northeast": "northeast",
			"northwest": "northwest",
			"southeast": "southeast",
			"southwest": "southwest",
		}

		verb = self.find_unambiguous_abbreviation(verb, verb_map)
		if verb == None:
			return
		elif verb in verb_map:
			verb = verb_map[verb]
		else:
			print("Unknown command:", command)
			return

		if verb == 'go':
			if len(command_array) > 1:
				# print(f"You {verb} {command_array[1]}")
				direction = command_array[1]
				if direction not in self.current_room.exits:
					direction = self.find_unambiguous_abbreviation(command_array[1], self.current_room.exits)
					if direction is None:
						return
				self.move(direction)
				# self.show_room = True
			else:
				self.show_room = False
				print(f"Sorry, you need to '{verb}' somewhere.")
		elif verb == 'get':
			if len(command_array) > 1:
				# print(f"You {verb} {command_array[1]}")
				self.show_room = True
				self.take(command_array[1])
			else:
				self.show_room = False
				print(f"Sorry, you need to '{verb}' something.")
		elif verb == 'drop':
			if len(command_array) > 1:
				self.show_room = True
				self.drop(command_array[1])
			else:
				self.show_room = False
				print(f"Sorry you need to '{verb}' somewhere")
		elif verb == 'inventory':
			self.show_inventory()
		elif verb == 'look':
			self.show_room = True
		elif verb == 'quit':
			raise KeyboardInterrupt
		elif verb == "lock":
			if len(command_array) > 1:
				self.show_room = True
				self.handle_lock_unlock(verb, command_array[1])
			else:
				self.show_room = False
				print(f"Sorry you need to '{verb}' somewhere")
		elif verb == "unlock":
			if len(command_array) > 1:
				self.show_room = True
				self.handle_lock_unlock(verb, command_array[1])
			else:
				self.show_room = False
				print(f"Sorry you need to '{verb}' somewhere")
		elif verb == "help":
			self.show_room = False
			self.help()
		else:
			print('Unknown command: ', command)

	def find_unambiguous_abbreviation(self, word, options):
		matches = [option for option in options if option.startswith(word)]
		if len(matches) == 1:
			self.show_room = True
			return matches[0]
		elif len(matches) > 1:
			print(f"Did you want to {word} {', '.join(matches[:-1])} or {matches[-1]}?")
			self.show_room = False
			return None
		else:
			self.show_room = False
			return word

	def handle_lock_unlock(self, action, direction):

		if direction in self.current_room.exits:
			if action == "lock":
				if direction not in self.current_room.locked_exits:
					# Add the direction to locked_exits
					self.current_room.locked_exits[direction] = self.current_room.exits[direction]
					print(f"The {direction} door is now locked.")
				else:
					print(f"The {direction} door is already locked.")
			elif action == "unlock":
				if "key" in self.inventory:
					if direction in self.current_room.locked_exits:
						del self.current_room.locked_exits[direction]
						print(f"The {direction} door is now unlocked.")
						self.inventory.remove("key")
					else:
						print(f"The {direction} door is not locked.")
				else:
					print("You don't have a key to unlock the door.")
		else:
			print("There is no door in that direction.")

	def move(self, direction):

		if direction in self.current_room.locked_exits:
			print("The door is locked. You need a key to unlock it.")
			return

		if direction in self.current_room.exits:
			self.show_room = True
			print(f"You go {direction}.\n")
			next_room_id = self.current_room.exits[direction]

			self.current_room = self.game_map.rooms[next_room_id]
			if self.current_room.winning_items:
				print("Pay attention! You enter the Boss room!")
				if all(item in self.inventory for item in self.current_room.winning_items):
					print("Congratulations, you have won the game!")
					self.is_game_over = True
				else:
					print("Unfortunately, you have lost the game.")
					self.is_game_over = True
		else:
			self.show_room = False
			print(f"There's no way to go {direction}.")

	def take(self, item_name):

		item_name = self.find_unambiguous_abbreviation(item_name, self.current_room.items)
		if item_name in self.current_room.items:
			self.current_room.items.remove(item_name)
			self.inventory.append(item_name)
			print(f"You pick up the {item_name}.")
		else:
			print(f"There's no {item_name} anywhere.")

	def drop(self, item_name):
		if item_name in self.inventory:
			self.inventory.remove(item_name)
			self.current_room.items.append(item_name)
			print(f"You drop the {item_name}.")
		else:
			print(f"You don't have a {item_name} in your inventory.")

	def show_inventory(self):
		if len(self.inventory) == 0:
			print("You're not carrying anything.")
		else:
			print("Inventory:", ', '.join(self.inventory))

	def find_item_in_room(self, item_name):
		for item in self.current_room.items:
			if item.name.lower() == item_name.lower():
				return item
		return None

	def find_item_in_inventory(self, item_name):
		for item in self.inventory:
			if item.name.lower() == item_name.lower():
				return item
		return None

	def display_room(self):
		print(f"> {self.current_room.name}\n")
		print(f"{self.current_room.description}\n")
		exits_item = [f"{dir}" for dir, index in self.current_room.exits.items()]
		exits = " ".join(exits_item)
		if self.current_room.items:
			print(f"Items: {', '.join(self.current_room.items)}\n")
		if self.current_room.locked_exits:
			print("Locking rooms: ", end="")
			for direction, lock_type in self.current_room.locked_exits.items():
				print(f"{direction} ", end="")
			print()  # Print a newline after locked_exits
		print(f"Exits: {exits}\n")

	def quit_game(self):
		print("Goodbye!")
		self.is_game_over = True
		sys.exit(0)

	def help(self):
		help_text = [
			"go ...",
			"get ...",
			"look",
			"inventory",
			"quit",
			"help",
			"drop ...",
			"lock ...",
			"unlock ..."
		]
		print("You can run the following commands:")
		for line in help_text:
			print(" ", line)

