# room_game.py

class Door:
    def __init__(self, color, leads_to, locked=False):
        self.color = color
        self.leads_to = leads_to
        self.locked = locked


class Key:
    def __init__(self, color, found_in, description=""):
        self.color = color
        self.found_in = found_in
        self.description = description

    def describe(self):
        print(f"A {self.color} key — {self.description}")


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.doors = []
        self.keys = []
        self.actions = {}
        self.state = {}  # Stores arbitrary room state (like "light_on": False)

    def add_door(self, color, room, locked=False):
        self.doors.append(Door(color, room, locked))

    def add_key(self, key):
        self.keys.append(key)

    def remove_key(self, key):
        if key in self.keys:
            self.keys.remove(key)

    def add_action(self, command, function):
        """Register a custom action for this room."""
        self.actions[command.lower()] = function

    def describe(self):
        print(f"\nYou are in the {self.name}.")
        print(self.description)

        if self.doors:
            print("\nYou see doors in these colors:")
            for door in self.doors:
                lock_status = " (locked)" if door.locked else ""
                print(f"- {door.color.capitalize()}{lock_status}")
        else:
            print("\nThere are no doors here!")

        if self.keys:
            print("\nYou see some keys:")
            for key in self.keys:
                print(f"- {key.color.capitalize()} key")

        if self.actions:
            print("\nYou can also try actions like:")
            for action in self.actions:
                print(f"- {action}")


class Player:
    def __init__(self, start_room):
        self.current_room = start_room
        self.inventory = []

    def take_key(self):
        if not self.current_room.keys:
            print("There are no keys here to take.")
            return
        for key in list(self.current_room.keys):
            print(f"You picked up the {key.color} key.")
            self.inventory.append(key)
            self.current_room.remove_key(key)

    def use_key(self, color):
        key = next((k for k in self.inventory if k.color == color), None)
        if not key:
            print(f"You don’t have a {color} key.")
            return

        door = next((d for d in self.current_room.doors if d.color == color), None)
        if not door:
            print(f"There is no {color} door here.")
            return

        if not door.locked:
            print(f"The {color} door is already unlocked.")
            return

        door.locked = False
        print(f"You used the {color} key to unlock the door!")

    def list_inventory(self):
        if not self.inventory:
            print("You’re not carrying any keys.")
        else:
            print("\nYou have the following keys:")
            for key in self.inventory:
                print(f"- {key.color.capitalize()} key")


class Game:
    def __init__(self):
        self.keys = []
        self.create_world()

    # --- Room-specific actions can be defined as methods here ---
    def toggle_light(self, room):
        """Toggle a room's light on/off."""
        light_on = room.state.get("light_on", False)
        room.state["light_on"] = not light_on
        if room.state["light_on"]:
            print("You pull the string — the light flickers on, revealing shelves of old clothes.")
        else:
            print("You pull the string again — the light clicks off, and the closet goes dark.")

    def create_world(self):
        kitchen = Room("Kitchen", "A bright kitchen with the smell of fresh bread.")
        living_room = Room("Living Room", "A cozy space with a roaring fireplace.")
        study = Room("Study", "A quiet study filled with dusty books.")
        garden = Room("Garden", "A lush garden buzzing with bees and sunlight.")
        bed_room = Room("Bedroom", "A dim room with clothes scattered about.")
        bedroom_closet = Room("Bedroom Closet", "A walk-in closet with a single pull-string light.")

        # Connect rooms
        kitchen.add_door("red", living_room)
        kitchen.add_door("blue", study, locked=True)
        living_room.add_door("green", kitchen)
        living_room.add_door("yellow", garden)
        study.add_door("purple", kitchen)
        garden.add_door("orange", living_room, locked=True)
        living_room.add_door("cyan", bed_room)
        bed_room.add_door("black", living_room)
        bed_room.add_door("white", bedroom_closet)
        bedroom_closet.add_door("white", living_room)

        # Create and place keys
        key_blue = Key("blue", found_in=living_room, description="engraved with a small 'S'.")
        key_cyan = Key("orange", found_in=garden, description="it sparkles faintly in the sunlight.")


        living_room.add_key(key_blue)
        garden.add_key(key_cyan)
        self.keys.extend([key_blue, key_cyan])

        # Add light toggle action (now cleanly referencing a Game method)
        bedroom_closet.state["light_on"] = False
        bedroom_closet.add_action("pull string", lambda: self.toggle_light(bedroom_closet))

        self.player = Player(start_room=kitchen)

    def play(self):
        print("Welcome to the Color Door Adventure!")
        print("Commands: [color] (to move), 'take key', 'use [color] key', 'inventory', 'quit'")
        print("Some rooms have unique actions — try typing them!\n")

        while True:
            self.player.current_room.describe()
            command = input("\n> ").strip().lower()

            if command == "quit":
                print("\nThanks for playing!")
                break

            elif command == "take key":
                self.player.take_key()

            elif command.startswith("use "):
                parts = command.split()
                if len(parts) == 3 and parts[2] == "key":
                    color = parts[1]
                    self.player.use_key(color)
                else:
                    print("Try 'use [color] key'.")

            elif command == "inventory":
                self.player.list_inventory()

            elif command in self.player.current_room.actions:
                action = self.player.current_room.actions[command]
                action()

            else:
                color = command
                door = next((d for d in self.player.current_room.doors if d.color == color), None)
                if not door:
                    print("There is no door of that color here.")
                    continue

                if door.locked:
                    print("That door is locked. You need the matching key.")
                    continue

                self.player.current_room = door.leads_to


if __name__ == "__main__":
    game = Game()
    game.play()

