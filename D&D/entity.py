from math import ceil

import tcod

from fov_functions import initialize_fov
from game_messages import Message
from render_functions import RenderOrder


class Entity(object):
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

    def move(self, dx, dy):
        # Moves the entity by a given amount
        self.x += dx
        self.y += dy

    def calculate_movement(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = max(abs(dx), abs(dy))
        dx = int(ceil(dx / distance))
        dy = int(ceil(dy / distance))
        return dx, dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx, dy = self.calculate_movement(target_x, target_y)
        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_away(self, target_x, target_y, game_map, entities):
        dx, dy = self.calculate_movement(target_x, target_y)
        if self.blocked(game_map, entities, -dx, -dy):
            self.move(-dx, -dy)
        elif self.blocked(game_map, entities, -dx, dy):
            self.move(-dx, dy)
        elif self.blocked(game_map, entities, dx, -dy):
            self.move(dx, -dy)

    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = initialize_fov(game_map)
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)
        my_path = tcod.path_new_using_map(fov, 1)
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)
        tcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return max(abs(dx), abs(dy))

    def distance(self, x, y):
        dx = x - self.x
        dy = y - self.y
        return max(abs(dx), abs(dy))

    def blocked(self, game_map, entities, dx, dy):
        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            return True
        return False


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None


def get_all_entities_at_location(entities, destination_x, destination_y):
    return [entity for entity in entities if destination_x == entity.x and destination_y == entity.y]


def check_entity_at_location(entities, x, y):
    results = []
    entities = get_all_entities_at_location(entities, x, y)
    if entities:
        for entity in entities:
            if entity.render_order in (RenderOrder.CORPSE, RenderOrder.ACTOR, RenderOrder.ITEM):
                results.append({'message': Message(entity.name, tcod.yellow)})
    else:
        results.append({'message': Message(f'There is nothing here', tcod.yellow)})
    return results
