import tcod
from utility_functions.random_generator import NumberGenerator
from components.dice import DiceRoll
from components.fighter import Fighter
from components.item import Item
from components.item_functions import heal, range_attack
from monster_functions import get_monster_ai, get_monster_arrangement
from entity import Entity
from game_messages import Message
from map_objects.map_classes import *
from render_functions import RenderOrder


def place_monster(room, entities, monster):
    # Choose a random location in the room
    x = NumberGenerator.random_integer(room.x1 + 1, room.x2 - 1)
    y = NumberGenerator.random_integer(room.y1 + 1, room.y2 - 1)
    if not any([entity for entity in entities if entity.x == x and entity.y == y]):
        fighter_component = Fighter(monster)
        ai_component = get_monster_ai(monster)
        monster = Entity(x, y, f'{monster[0]}', tcod.desaturated_green, f"{monster}", blocks=True,
                         render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
        return monster


def place_item(room, entities):
    item_chance = NumberGenerator.random_integer(0, 100)
    x = NumberGenerator.random_integer(room.x1 + 1, room.x2 - 1)
    y = NumberGenerator.random_integer(room.y1 + 1, room.y2 - 1)
    if not any([entity for entity in entities if entity.x == x and entity.y == y]):
        if item_chance < 50:
            item_component = Item(use_function=heal, amount="2d4+2")
            item = Entity(x, y, '+', tcod.pink, 'Healing Potion', render_order=RenderOrder.ITEM,
                          item=item_component)
        elif item_chance < 60:
            item_component = Item(attack_name="fireball", use_function=range_attack, targeting=True,
                                  targeting_message=Message(
                                      'Left-click a target tile for the fireball, or right-click to cancel.',
                                      tcod.light_cyan),
                                  damage=DiceRoll("2d12"), radius=3, range=10, attack_type='sphere')
            item = Entity(x, y, '#', tcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                          item=item_component)
        else:
            item_component = Item(attack_name="dart", use_function=range_attack, targeting=True,
                                  targeting_message=Message(
                                      'Left-click a target tile for the dart, or right-click to cancel.',
                                      tcod.light_cyan),
                                  damage=DiceRoll("2d12"), radius=0, range=3, attack_type='sphere')
            item = Entity(x, y, '>', tcod.red, 'Dart', render_order=RenderOrder.ITEM,
                          item=item_component)
        return item


def place_entities(room, entities, monster_difficulty, max_items_per_room):
    # Get a random number of monsters
    monsters = get_monster_arrangement(monster_difficulty)
    number_of_items = NumberGenerator.random_integer(0, max_items_per_room)
    for monster in monsters:
        monster = place_monster(room, entities, monster)
        if monster:
            entities.append(monster)
    for i in range(number_of_items):
        item = place_item(room, entities)
        if item:
            entities.append(item)


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                 monster_difficulty, max_items_per_room):
        rooms = []
        num_rooms = 0
        center_of_last_room_x = None
        center_of_last_room_y = None
        for r in range(max_rooms):
            # random width and height
            w = NumberGenerator.random_integer(room_min_size, room_max_size)
            h = NumberGenerator.random_integer(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = NumberGenerator.random_integer(0, map_width - w - 1)
            y = NumberGenerator.random_integer(0, map_height - h - 1)
            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    prev_x, prev_y = rooms[num_rooms - 1].center()
                    # flip a coin (random number that is either 0 or 1)
                    if NumberGenerator.random_integer(0, 1) == 1:
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
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', tcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

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

    def next_floor(self, player, message_log, constants):
        NumberGenerator()
        self.dungeon_level += 1
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities,
                      float(player.fighter.cr), constants['max_items_per_room'])
        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(Message('You take a moment to rest, and recover your strength.', tcod.light_violet))
        return entities
