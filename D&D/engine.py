import tcod
import tcod.console
import tcod.event

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location, check_entity_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates, MenuState
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from render_functions import render_all, clear_all
from components.dice import DiceRoll


def main():
    constants = get_constants()

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    root_con = tcod.console_init_root(constants["screen_width"], constants["screen_height"],
                                      constants["window_title"], order="C", renderer=tcod.RENDERER_SDL2, vsync=True)

    con = tcod.console.Console(constants['screen_width'], constants['screen_height'])
    panel = tcod.console.Console(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = tcod.image_load('menu_background.png')
    while show_main_menu:
        main_menu(con, main_menu_background_image, constants['screen_width'],
                  constants['screen_height'], root_con)

        if show_load_error_message:
            message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'],
                        root_con)

        tcod.console_flush()
        action = {}
        for event in tcod.event.get():
            if isinstance(event, tcod.event.KeyDown):
                action = handle_main_menu(event)

        new_game = action.get('new_game')
        load_saved_game = action.get('load_game')
        exit_game = action.get('exit')

        if show_load_error_message and (new_game or load_saved_game or exit_game):
            show_load_error_message = False
        elif new_game:
            player, entities, game_map, message_log, game_state = get_game_variables(constants)
            game_state = GameStates.PLAYER_TURN
            show_main_menu = False
        elif load_saved_game:
            try:
                player, entities, game_map, message_log, game_state = load_game()
                show_main_menu = False
            except FileNotFoundError:
                show_load_error_message = True
        elif exit_game:
            quit()
    else:
        con.clear()
        play_game(player, entities, game_map, message_log, game_state, con, panel, constants, root_con)
        main()


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants, root_con):
    tcod.console_set_custom_font("arial10x10.png", tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE)
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    previous_game_state = game_state
    targeting_item = None
    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants["screen_width"],
                   constants["screen_height"], constants["bar_width"], constants["panel_y"], constants["colors"],
                   root_con, game_state)
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
            take_stairs = None
            leave = None
            fullscreen = None
            show_character_screen = None
            player_turn_results = []
            if isinstance(event, tcod.event.KeyDown):
                action = handle_keys(event, game_state)
                move = action.get("move")
                pickup = action.get("pickup")
                look_enemy = action.get("look_enemy")
                show_inventory = action.get("show_inventory")
                drop_inventory = action.get("drop_inventory")
                inventory_index = action.get("inventory_index")
                take_stairs = action.get('take_stairs')
                leave = action.get("leave")
                fullscreen = action.get("fullscreen")
                show_character_screen = action.get('show_character_screen')
            if isinstance(event, tcod.event.MouseButtonDown):
                mouse_action = handle_mouse(event, game_state)
                left_click = mouse_action.get("left_click")
                right_click = mouse_action.get("right_click")
            if look_enemy and game_state == GameStates.PLAYER_TURN:
                game_state = GameStates.LOOK_ENEMY
                player_turn_results.extend([{'message': Message('You are in the looking mode', tcod.green)}])
            elif look_enemy and game_state == GameStates.LOOK_ENEMY:
                game_state = GameStates.PLAYER_TURN
                player_turn_results.extend([{'message': Message('You left the looking mode', tcod.green)}])
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
                if left_click and targeting_item:
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
                        attack_results = player.fighter.melee_attack(target)
                        player_turn_results.extend(attack_results)
                    else:
                        player.move(dx, dy)

                        fov_recompute = True
                    game_state = GameStates.ENEMY_TURN
            elif take_stairs and game_state == GameStates.PLAYER_TURN:
                for entity in entities:
                    if entity.stairs and entity.x == player.x and entity.y == player.y:
                        entities = game_map.next_floor(player, message_log, constants)
                        fov_map = initialize_fov(game_map)
                        fov_recompute = True
                        con.clear(fg=(63, 127, 63))

                        break
                else:
                    message_log.add_message(Message('There are no stairs here.', tcod.yellow))
            elif game_state == GameStates.LEVEL_UP:
                player.fighter.max_hp += DiceRoll("1d8").roll_dice()
                game_state = previous_game_state
            elif show_character_screen:
                previous_game_state = game_state
                game_state = GameStates.CHARACTER_SCREEN
            if leave:
                if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                    game_state = previous_game_state
                elif game_state == GameStates.TARGETING:
                    player_turn_results.append({'targeting_cancelled': True})
                else:
                    save_game(player, entities, game_map, message_log, game_state)
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
                xp = player_turn_result.get('xp')
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

                if xp:
                    leveled_up = player.level.add_xp(xp)
                    message_log.add_message(Message('You gain {0} experience points.'.format(xp)))

                    if leveled_up:
                        message_log.add_message(Message(
                            'Your battle skills grow stronger! You reached level {0}'.format(
                                player.level.current_level) + '!', tcod.yellow))
                        player.fighter.cr = str(player.level.current_level/4)
                        previous_game_state = game_state
                        game_state = GameStates.LEVEL_UP

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
