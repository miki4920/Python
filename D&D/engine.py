import tcod
import tcod.event
import tcod.console
from game_states import GameStates
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap
from components.fighter import Fighter


def main():
    # Screen Resolution
    screen_width = 80
    screen_height = 50
    # Map Resolution
    map_width = 80
    map_height = 45
    # Room Statistics
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    # Field of View
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    # Monsters
    max_monsters_per_room = 3
    # Color
    colors = {
        'dark_wall': tcod.Color(13, 13, 13),
        'dark_ground': tcod.Color(25, 25, 38),
        'light_wall': tcod.Color(0, 0, 26),
        'light_ground': tcod.Color(50, 50, 77)
    }

    # Initiate entities
    fighter_component = Fighter(hp=8, armor_class=10, strength=12)
    player = Entity(0, 0, "@", tcod.white, "Player", blocks=True, fighter=fighter_component)
    game_state = GameStates.PLAYER_TURN
    entities = [player]

    tcod.console_set_custom_font("arial10x10.png", tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    root_con = tcod.console_init_root(screen_width, screen_height,
                                      "First Game", order="C", renderer=tcod.RENDERER_SDL2, vsync=True)
    con = tcod.console.Console(screen_width, screen_height)
    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors, root_con)
        tcod.console_flush()
        clear_all(con, entities)
        for event in tcod.event.get():
            if isinstance(event, tcod.event.KeyDown):
                action = handle_keys(event)

                move = action.get("move")
                leave = action.get("leave")
                fullscreen = action.get("fullscreen")

                if move and game_state == GameStates.PLAYER_TURN:
                    dx, dy = move
                    destination_x = player.x + dx
                    destination_y = player.y + dy
                    if not game_map.is_blocked(destination_x, destination_y):
                        target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                        if target:
                            print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                        else:
                            player.move(dx, dy)

                            fov_recompute = True
                        game_state = GameStates.ENEMY_TURN

                if leave:
                    return True

                if fullscreen:
                    tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                if game_state == GameStates.ENEMY_TURN:
                    for entity in entities:
                        if entity.ai:
                            if entity.ai.take_turn(player, fov_map, game_map, entities):
                                print('The ' + entity.name + ' ponders the meaning of its existence.')

                    game_state = GameStates.PLAYER_TURN


if __name__ == "__main__":
    main()