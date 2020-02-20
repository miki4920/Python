import tcod
import tcod.console
import tcod.event

from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location, check_entity_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog, Message
from game_states import GameStates, MenuState
from input_handlers import handle_keys, handle_mouse
from map_objects.game_map import GameMap
from render_functions import render_all, clear_all, RenderOrder


def main():
    # Screen Resolution
    screen_width = 80
    screen_height = 50
    # Bar Resolution
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    # Map Resolution
    map_width = 80
    map_height = 43
    # Message Resolution
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    # Room Statistics
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    # Field of View
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    # Entities
    monster_difficulty = 1
    max_items_per_room = 2
    # Color
    colors = {
        'dark_wall': tcod.Color(13, 13, 13),
        'dark_ground': tcod.Color(25, 25, 38),
        'light_wall': tcod.Color(0, 0, 26),
        'light_ground': tcod.Color(50, 50, 77)
    }
    # Initiate entities
    fighter_component = Fighter("player")
    inventory_component = Inventory(26)
    player = Entity(0, 0, "@", tcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state
    entities = [player]

    tcod.console_set_custom_font("arial10x10.png", tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      monster_difficulty, max_items_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    root_con = tcod.console_init_root(screen_width, screen_height,
                                      "First Game", order="C", renderer=tcod.RENDERER_SDL2, vsync=True)
    con = tcod.console.Console(screen_width, screen_height)
    panel = tcod.console.Console(screen_width, panel_height)
    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                   screen_height, bar_width, panel_y, colors, root_con, game_state)
        tcod.console_flush()
        clear_all(con, entities)
        for event in tcod.event.get():
            move = None
            pickup = None
            look_enemy = None
            left_click = None
            right_click = None
            show_inventory = None
            drop_inventory = None
            inventory_index = None
            leave = None
            fullscreen = None
            look_enemy = None
            player_turn_results = []
            targeting_item = None
            if isinstance(event, tcod.event.KeyDown):
                action = handle_keys(event, game_state)
                move = action.get("move")
                pickup = action.get("pickup")
                look_enemy = action.get("look_enemy")
                show_inventory = action.get("show_inventory")
                drop_inventory = action.get("drop_inventory")
                inventory_index = action.get("inventory_index")
                leave = action.get("leave")
                fullscreen = action.get("fullscreen")
                look_enemy = action.get("look_enemy")
            if isinstance(event, tcod.event.MouseButtonDown):
                mouse_action = handle_mouse(event, game_state)
                left_click = mouse_action.get("left_click")
                right_click = mouse_action.get("right_click")
            if look_enemy and game_state == GameStates.PLAYER_TURN:
                game_state = GameStates.LOOK_ENEMY
                player_turn_results.extend([{'message': Message('You are in the looking mode', tcod.green)}])
            elif look_enemy and game_state == GameStates.LOOK_ENEMY:
                game_state = GameStates.PLAYER_TURN
            elif left_click and game_state == GameStates.LOOK_ENEMY:
                entities_at_location = check_entity_at_location(entities, left_click[0], left_click[1])
                player_turn_results.extend(entities_at_location)
            elif pickup and game_state == GameStates.PLAYER_TURN:
                for entity in entities:
                    if entity.item and entity.x == player.x and entity.y == player.y:
                        pickup_results = player.inventory.add_item(entity)
                        player_turn_results.extend(pickup_results)
                        break
                else:
                    message_log.add_message(Message('There is nothing here to pick up.', tcod.yellow))
            elif show_inventory:
                previous_game_state = game_state
                game_state = GameStates.SHOW_INVENTORY
                MenuState.menu_state = 0
            elif drop_inventory:
                previous_game_state = game_state
                game_state = GameStates.DROP_INVENTORY
            elif inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                    player.inventory.items):
                item = player.inventory.items[inventory_index]
                if game_state == GameStates.SHOW_INVENTORY:
                    player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
                elif game_state == GameStates.DROP_INVENTORY:
                    player_turn_results.extend(player.inventory.drop_item(item))
            elif game_state == GameStates.TARGETING:
                if left_click:
                    target_x, target_y = left_click

                    item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                            target_x=target_x, target_y=target_y)
                    player_turn_results.extend(item_use_results)
                elif right_click:
                    player_turn_results.append({'targeting_cancelled': True})
            elif move and game_state == GameStates.PLAYER_TURN:
                dx, dy = move
                destination_x = player.x + dx
                destination_y = player.y + dy
                if not game_map.is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)
                    else:
                        player.move(dx, dy)

                        fov_recompute = True
                    game_state = GameStates.ENEMY_TURN
            if leave:
                if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                    game_state = previous_game_state
                elif game_state == GameStates.TARGETING:
                    player_turn_results.append({'targeting_cancelled': True})
                else:
                    return True

            if fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            for player_turn_result in player_turn_results:
                message = player_turn_result.get('message')
                dead_entity = player_turn_result.get('dead')
                entity_identified = player_turn_result.get("entity_identified")
                item_added = player_turn_result.get('item_added')
                item_consumed = player_turn_result.get('consumed')
                item_dropped = player_turn_result.get('item_dropped')
                targeting = player_turn_result.get('targeting')
                targeting_cancelled = player_turn_result.get('targeting_cancelled')
                if message:
                    message_log.add_message(message)

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_monster(dead_entity)

                    message_log.add_message(message)

                if item_added:
                    entities.remove(item_added)
                    game_state = GameStates.ENEMY_TURN

                if item_consumed:
                    game_state = GameStates.ENEMY_TURN

                if item_dropped:
                    entities.append(item_dropped)
                    game_state = GameStates.ENEMY_TURN

                if entity_identified:
                    game_state = GameStates.PLAYER_TURN

                if targeting:
                    previous_game_state = GameStates.PLAYER_TURN
                    game_state = GameStates.TARGETING

                    targeting_item = targeting

                    message_log.add_message(targeting_item.item.targeting_message)

                if targeting_cancelled:
                    game_state = previous_game_state
                    message_log.add_message(Message('Targeting cancelled'))

            if game_state == GameStates.ENEMY_TURN:
                for entity in entities:
                    if entity.ai:
                        enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                        for enemy_turn_result in enemy_turn_results:
                            message = enemy_turn_result.get('message')
                            dead_entity = enemy_turn_result.get('dead')

                            if message:
                                message_log.add_message(message)

                            if dead_entity:
                                if dead_entity == player:
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)

                                message_log.add_message(message)

                                if game_state == GameStates.PLAYER_DEAD:
                                    break

                        if game_state == GameStates.PLAYER_DEAD:
                            break
                else:
                    game_state = GameStates.PLAYER_TURN


if __name__ == "__main__":
    main()
