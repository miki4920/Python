import tcod

from game_messages import Message
from components.range_functions import cast_sphere


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', tcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', tcod.green)})

    return results


def range_attack(*args, **kwargs):
    attack_name = kwargs.get("attack_name")
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    attack_range = kwargs.get('range')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    attack_type = kwargs.get('attack_type')
    if attack_type == 'sphere':
        results = cast_sphere(attack_name, entities, fov_map, damage, attack_range, radius, target_x, target_y)
    return results




