from utility_functions.random_generator import NumberGenerator
import tcod


class BasicMonster(object):
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.melee_attack(target)
                results.extend(attack_results)
        return results


class SkirmishMonster(object):
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            target_distance = monster.distance_to(target)
            if target_distance >= 4:
                monster.move_astar(target, entities, game_map)
            elif target_distance < 4:
                attack_chance = NumberGenerator.random_integer(1, 2)
                if attack_chance < 2 and target.fighter.hp > 0:
                    attack_results = monster.fighter.range_attack(target)
                    results.extend(attack_results)
                else:
                    monster.move_away(target.x, target.y, game_map, entities)
        return results


class ChargerMonster(object):
    def __init__(self):
        self.thrown = False

    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) == 2 and not self.thrown:
                attack_results = monster.fighter.range_attack(target)
                results.extend(attack_results)
                self.thrown = True
            elif monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.melee_attack(target)
                results.extend(attack_results)
        return results
