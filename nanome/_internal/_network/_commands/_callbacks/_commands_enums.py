from nanome.util import Logs, IntEnum, auto

try:
    from nanome.util import reset_auto
except:
    def reset_auto():
        pass

import sys

class __CommandEnum(IntEnum):
    if sys.version_info >= (3, 6): # Tmp hack
        # Override for auto()
        @staticmethod
        def _generate_next_value_(name, start, count, last_values):
            return IntEnum._generate_next_value_(name, 0, count, last_values)
    else:
        pass

# /!\ /!\ /!\
# Values names are really important here, as they are hashed, and need to match Nanome
class _Commands(__CommandEnum):
    #Control Commands
    connect = auto()
    run = auto()
    advanced_settings = auto()
    controller_response = auto()

    #Workspace Commands
    workspace_receive = auto()
    complex_add = auto()
    complex_remove = auto()
    complexes_receive = auto()
    complex_list_receive = auto()
    bonds_add_result = auto()
    stream_create_result = auto()
    stream_interrupt = auto()

    #UI Commands======
    menu_receive = auto()
    menu_toggle = auto()
    button_press = auto()
    slider_release = auto()
    text_submit = auto()
    text_change = auto()
    slider_change = auto()
    image_press = auto()
    image_hold = auto()
    image_release = auto()

    #File Commands
    directory_receive = auto()
    file_receive = auto()
    file_save_result_receive = auto()

    #Done Commands
    structures_deep_update_done = auto()
    position_structures_done = auto()
    stream_feed_done = auto()

# /!\ /!\ /!\
# Values names are really important here, as they are hashed, and need to match Nanome
class _Messages(__CommandEnum):
    # Tmp hack
    reset_auto()

    #Control Messages
    connect = auto()
    plugin_list_button_set = auto()
    notification_send = auto()
    controller_request = auto()

    #Workspace Messages
    workspace_request = auto()
    workspace_update = auto()
    add_to_workspace = auto()
    structures_deep_update = auto()
    structures_shallow_update = auto()
    structures_zoom = auto()
    structures_center = auto()
    complex_list_request = auto()
    complexes_request = auto()
    bonds_add = auto()

    stream_create = auto()
    stream_destroy = auto()
    stream_feed = auto()

    #UI Messages
    menu_update = auto()
    content_update = auto()

    #File Messages
    directory_request = auto()
    file_request = auto()
    file_save = auto()

class _Hashes():
    CommandHashes = [None] * len(_Commands)
    MessageHashes = [None] * len(_Messages)

a_char_value = ord('a')
z_char_value = ord('z')

def hash_command(str):
    result = 0
    hit = 0
    for i in range(6):
        idx = i * 3 % len(str)
        char_value = ord(str[idx].lower()) - a_char_value
        result <<= 5
        if char_value < 0 or char_value > z_char_value - a_char_value:
            continue
        result |= char_value + 1
        hit += 1
        if hit >= 6:
            break
    return result

def init_hashes():
    hashes = dict()
    i = -1
    for command in _Commands:
        i += 1
        hash = hash_command(command.name)
        if hash in hashes:
            Logs.error("Command hash collision detected:", command.name, "and", hashes[hash])
            continue
        hashes[hash] = command.name
        _Hashes.CommandHashes[i] = hash

    hashes.clear()
    i = -1

    for command in _Messages:
        i += 1
        hash = hash_command(command.name)
        if hash in hashes:
            Logs.error("Message hash collision detected:", command.name, "and", hashes[hash])
            continue
        hashes[hash] = command.name
        _Hashes.MessageHashes[i] = hash

init_hashes()