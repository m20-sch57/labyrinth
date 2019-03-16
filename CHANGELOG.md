## ChangeLog v0.1

#### Labyrinth

- **Added** message priorities.
- **Added** turns log. method `get_turns`.
- **Added** methods `get_object`, `get_all_objects`.
- **Added** unique objects concept. method `get_unique`.
- **Added** method `set_settings`.
- **Added** "load" and "save" functionality.
- **Added** buttons api. method `get_buttons`
    - **Added** `CommonButton`.
    - **Added** `DirectionButton`.
    - **Added** `ListButton`.
- **Removed** `ObjectID`.


#### Labyrinth objects

- **Added** vanilla objects:
    - Locations:
        - Arsenal
        - First Aid Post
        - Exit
        - Wall
    - Items:
        - Ammo
        - Health
        - Gun
        - Bomb
    - Creatures:
        - Bear


#### WebSite 

+ **Added** password hashing.
+ **Added** paginatin in room list.
+ **Added** ability to change username.
+ **Added** ability to change password.
- **Added** game and waiting room.
- **Added** players list in the rooms.
- **Added** ability to change the name of the room.
- **Added** ability to change the description of the room.
- **Added** switchable interface for changing the settings of the room.
- **Added** multiplayer mode for labyrinth.

#### Server

- **Added** data structure for storing active labyrinths.
- **Changed** database.. (see more in [#40](https://github.com/m20-sch57/labyrinth/pull/40))

#### Design
- **Added** template for waiting room.
- **Added** template for game room.
