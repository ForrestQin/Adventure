1. Name: Honglin Qin, hqin4@stevens.edu
2. Url: https://github.com/ForrestQin/Adventure
3. Hours spent: 10 hrs+
4. How to test my code:
   ### Game Commands

Here are the available commands in the game:

### Room information

Every has its information, and all this information is from the map file

```
Name: the room's name
Desc: Provide a brief description about this room
Item: List of items the current room has.
Locking rooms (if applicable): Mention any locked doors or pathways in the room, and specify the direction.
Exits: The available exits from the room, including their direction
Winning items (if applicable): If the room is a boss room, list the items required to win the game when entering the room.
                               If the player enter a boss room without all winning items required, the player will loss.
```

1. go [direction]: Move to the specified direction (e.g., "go east").

   ```
    > Gray room

    You are in a room with gray walls.

    There is no item
    Exits: east

    What would you like to do? go east
    You go east
    > Yellow room

    You are in a room with yellow walls.

    Item: magic wand
    Locking rooms: east 
    Exits: east west

    What would you like to do? 
   ```

2. get [item]: Pick up the specified item (e.g., "get key").
    ```> Gray room
    You are in a room with gray walls.
    Item: key
    Exits: east

    What would you like to do? get key
    You pick up the key.
   ```
3. look: Inspect the current room.
   ```
      What would you like to do? look
      > Yellow room

      You are in a room with yellow walls.

      Item: magic wand
      Locking rooms: east 
      Exits: east west
   ```
4. inventory: Check your inventory.
   ```
   What would you like to do? inventory
   Inventory: key, magic wand
   ```
5. quit: Quit the game.
   ```
   What would you like to do? quit
   Goodbye!
   ```
6. help: Display the list of available commands.
   ```
   What would you like to do? help
   You can run the following commands:
   go ...
   get ...
   look
   inventory
   quit
   help
   drop ...
   lock ...
   unlock ...
   ```
7. drop [item]: Drop the specified item from your inventory (e.g., "drop key") and leave it to the current room.
   ```
   What would you like to do? drop key
   You drop the key.
   ```
8. lock [direction]: Lock the door in the specified direction (e.g., "lock east").
   ```
   What would you like to do? lock east
   The east door is now locked.
   > Gray room

   You are in a room with gray walls.

   Item: key
   Locking rooms: east 
   Exits: east
   ```
9. unlock [direction]: Unlock the door in the specified direction (e.g., "unlock east").
   ```
   What would you like to do? unlock east
   The east door is now unlocked.
   > Gray room

   You are in a room with gray walls.

   There is no item
   Exits: east
   ```

### bugs

#### bug one

    When we enter an ambiguous word, I don't want to show room again. But my original design will show room's detail once I enter a command

#### Solved

    I set a show_room flag, if and only if the show_room flag is True, we will show room's detail before we enter a command

#### bug two

    When I build the game map in my game engine, I cannot build the map correctly.

#### Solved

    I made a typo when I build the map.

### Difficult issue

    I picked 'Abbreviations for verbs, directions, and items' as an extention.
    When I try to implement, I found it's difficult to implement. At first, I put all terms into a dict. 
    But I found if verbs and items have a common prefix, I will show them all, it's not what we want.

### How to solve this issue

    I use different ways to deal with different situation. 
    For verbs, I create a verb_dict to check if a verb have a common prefix in this verb_dict.
    For direction, I create a direction_dict to get common prefix direction
    For items, I directly check the current room's items. If there are multiple items, we show them to the player.
    Else, we pick the only one.

## Extensions

1. Abbreviations for verbs, directions, and items
   ```
   In this game, players can use abbreviations for certain verbs, directions, and items.
   Abbreviations are accepted only when the entered command is a vaild prefix
   For example, we have command 'go' and 'get', so when we just enter g, 
   It will show 'Did you want to g go or get?'
   But if you enter an invalid abbreviation, like 's'
   If will show 'Unknown command: s'
   And the abbreviation only have one choice, we will directly use the one.
   Like if we enter 'go e', since there is only one direction 'east', we directly go east. 
   Same as when we get items.
   When we enter a room with item 'sword'
   If we enter 'get s', since there is only one choice, we directly pick it up.
   ```
2. A drop verb
   ```
   I implment drop verb in this game. The plalyer has a inventory 
   (we could use 'inventory' verb to check what the player carry now.)
   If the play get an item before, and the player could drop the item to the current room.
   At this time, the player's inventory will remove the item, and the current room will have this item.
   ```
3. Locked doors
   ```
   I implement lock and unlock verbs in my game.
   In any room, if we see there are locking rooms, it means we cannot go that directly, 
   we have to unlock the room first. In order to unlock the room, we have to have a key first.
   After we unlock a locking room, we could go that direction.
   ```
4. Winning and losing conditions
   ``` 
   I set a winning condition. There is a boss room in my map, and it has winning_items.
   If the player enter a boss room without all winning_items, the player will loss.
   So the player need to collect all winning items before we go to the boss room.
   ```
5. A help verb
   ```
   If the playen enter the verb 'help', it will shows:
   What would you like to do? help
   You can run the following commands:
   go ...
   get ...
   look
   inventory
   quit
   help
   drop ...
   lock ...
   unlock ...
   ```

## Test Step

In my repo, I attached a map.json file, it could follow following instruction to test:

### Test Win

```
Start the game.
Test look verb: look
Test get verb: get key
Test inventory verb: inventory or i
Test go verb: go east
Test look verb: look
Test get verb: get magic wand
Test inventory verb: inventory or i
Test unlock verb: unlock east
Test go verb: go east
Test look verb: look
Test get verb: get sword
Test inventory verb: inventory or i
Test go verb: go north
At this point, you should enter the boss room with all the winning items, and the game will automatically quit after displaying the victory message.
```

### Test Loss

```
Start the game.
Test look verb: look
Test get verb: get key
Test inventory verb: inventory or i
Test go verb: go east
Test look verb: look
Test get verb: get magic wand
Test inventory verb: inventory or i
Test unlock verb: unlock east
Test go verb: go east
Test look verb: look
Test get verb: get sword
Test inventory verb: inventory or i
Test drop verb: drop sword (this will simulate not having all the winning items)
Test go verb: go north
At this point, you should enter the boss room without all the winning items, and the game will automatically quit after displaying the losing message.
```