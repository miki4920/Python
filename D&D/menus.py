import tcod

from game_states import MenuState


def menu(con, header, options, width, screen_width, screen_height, root):
    if len(options) > 25:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.console_new(width, height)

    # print the header, with auto-wrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)
    # print all the options
    y = header_height
    letter_index = 1
    if len(options) > 0:
        MenuState.menu_state = MenuState.menu_state % len(options)
    for option_index in range(0, len(options)):
        if option_index == MenuState.menu_state and MenuState.menu_state < len(options):
            text = '(' + "X" + ') ' + options[option_index]
        else:
            text = '(' + " " + ') ' + options[option_index]
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, root, x, y, 1.0, 0.7)


def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height, root):
    # show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]

    menu(con, header, options, inventory_width, screen_width, screen_height, root)


def main_menu(con, background_image, screen_width, screen_height, root):
    tcod.image_blit_2x(background_image, root, 0, 0)

    tcod.console_set_default_foreground(root, tcod.light_yellow)
    tcod.console_print_ex(root, int(screen_width / 2), int(screen_height / 2) - 4, tcod.BKGND_NONE, tcod.CENTER,
                          'GOBLINS & CAVERNS')
    tcod.console_print_ex(root, int(screen_width / 2), int(screen_height - 2), tcod.BKGND_NONE, tcod.CENTER,
                          'By Nicolas Grobelny')

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height, root)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = tcod.console_new(character_screen_width, character_screen_height)

    tcod.console_set_default_foreground(window, tcod.white)
    messages = ['Character Information', f'Level: {player.level.current_level}',
                f'Experience: {player.level.current_xp}',
                f'Experience to Level: {player.level.experience_to_next_level}', f'Maximum HP: {player.fighter.max_hp}',
                f'Damage: {player.fighter.actions["0"].get("DAMAGE")}', f'AC: {player.fighter.ac}']
    for i in range(1, 8):
        tcod.console_print_rect_ex(window, 0, i, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                                   tcod.LEFT, messages[i - 1])
    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    tcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height, root):
    menu(con, header, [], width, screen_width, screen_height, root)
