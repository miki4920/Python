from random import randint

import tcod

from components.ai import BasicMonster
from components.dice import DiceRoll
from components.fighter import Fighter
from components.item import Item
from components.item_functions import heal, cast_spell
from create_monster import generate_creatures
from entity import Entity
from game_messages import Message
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from render_functions import RenderOrder


def place_entities(room, entities, monster_difficulty, max_items_per_room):
    # Get a random number of monsters
    monsters = generate_creatures(monster_difficulty)
    number_of_items = randint(0, max_items_per_room)
    for monster in monsters:
        # Choose a random location in the room
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)
        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            fighter_component = Fighter(monster)
            ai_component = BasicMonster()
            monster = Entity(x, y, f'{monster[0]}', tcod.desaturated_green, f"{monster}", blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            entities.append(monster)
    for i in range(number_of_items):
        item_chance = randint(0, 100)
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)
        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            if item_chance < 50:
                item_component = Item(use_function=heal, amount="2d4+2")
                item = Entity(x, y, '+', tcod.pink, 'Healing Potion', render_order=RenderOrder.ITEM,
                              item=item_component)
            else:
                item_component = Item(spell_name="fireball", use_function=cast_spell, targeting=True,
                                      targeting_message=Message(
                                          'Left-click a target tile for the fireball, or right-click to cancel.',
                                          tcod.light_cyan),
                                      damage=DiceRoll("2d12"), radius=3)
                item = Entity(x, y, '#', tcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                              item=item_component)
            entities.append(item)


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                 monster_difficulty, max_items_per_room):
        rooms = []
        num_rooms = 0
        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    prev_x, prev_y = rooms[num_rooms-1].center()
                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                if num_rooms != 0:
                    place_entities(new_room, entities, monster_difficulty, max_items_per_room)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1+1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2)):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False
