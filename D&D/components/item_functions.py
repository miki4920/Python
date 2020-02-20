import tcod

from game_messages import Message


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


def make_range_attack(*args, **kwargs):
    pass


def cast_spell(*args, **kwargs):
    spell_name = kwargs.get("spell_name")
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results

    results.append({'consumed': True,
                    'message': Message(f'The {spell_name} explodes, burning everything within {radius} tiles!',
                                       tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            rolled_damage = damage.roll_dice()
            results.append(
                {'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, rolled_damage),
                                               tcod.orange)})
            results.extend(entity.fighter.take_damage(rolled_damage))

    return results
