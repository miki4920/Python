import tcod
from game_messages import Message


def point_in_range(entities, attack_range, target_x, target_y):
    for entity in entities:
        if entity.name == 'Player':
            if entity.distance(target_x, target_y) <= attack_range:
                return True
    return False


def cast_sphere(attack_name, entities, fov_map, damage, attack_range, radius, target_x, target_y):
    results = []
    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results
    elif not point_in_range(entities, attack_range, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message(f'You cannot target a tile outside of attack range ({attack_range})', tcod.yellow)})
        return results
    if radius > 0:
        results.append({'consumed': True,
                        'message': Message(f'The {attack_name} damages everyone within {radius} tiles!',
                                           tcod.orange)})
        for entity in entities:
            if entity.distance(target_x, target_y) <= radius and entity.fighter:
                rolled_damage = damage.roll_dice()
                results.append(
                    {'message': Message('The {0} gets damaged for {1} hit points.'.format(entity.name, rolled_damage),
                                        tcod.orange)})
                results.extend(entity.fighter.take_damage(rolled_damage))
    elif radius == 0:
        for entity in entities:
            if entity.distance(target_x, target_y) == 0 and entity.fighter:
                rolled_damage = damage.roll_dice()
                results.append({'consumed': True,
                                'message': Message(f'The {attack_name} damages a single creature!',
                                                   tcod.orange)})
                results.append(
                    {'message': Message('The {0} gets damaged for {1} hit points.'.format(entity.name, rolled_damage),
                                        tcod.orange)})
                results.extend(entity.fighter.take_damage(rolled_damage))
                break
        else:
            results.append({'consumed': True,
                            'message': Message(f'The {attack_name} does not hit a thing!',
                                               tcod.orange)})
    return results
