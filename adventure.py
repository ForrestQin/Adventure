# This is a sample Python script.
from BuildMap import BuildMap
import sys
import json

from TextAdventureEngine import TextAdventureEngine


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def print_room(room):
	print(f"> {room.name}\n")
	print(f"{room.description}\n")
	exits = " ".join(f"{k} {v.name}" for k, v in room.exits.items())
	print(f"Exits: {exits}\n")


def main():
	if len(sys.argv) == 1:
		print("Miss the map file.")
		sys.exit(1)
	map_file_name = sys.argv[1]
	game_map = BuildMap(map_file_name)
	engine = TextAdventureEngine(game_map)
	try:
		while not engine.is_game_over:
			if engine.show_room:
				engine.display_room()
			command = input("What would you like to do? ").strip()
			try:
				engine.process_command(command)
			except KeyboardInterrupt:
				print("Goodbye!")
				break
			except EOFError:
				print("Use 'quit' to exit.")
	except KeyboardInterrupt:
		print("\nGoodbye!")


if __name__ == '__main__':
	main()
