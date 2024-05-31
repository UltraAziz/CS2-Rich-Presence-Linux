import time
from pypresence import Presence
from server import GSIServer
import struct
import os
import shutil
import json

game_state_config = 'gamestate_integration_GSI.cfg'
def get_steam_path():
    with open("config.json", "r") as read_file:
     config = json.load(read_file)
     path = config["directory"]
    
     return str(path)


# Initial setup
game_state_path = get_steam_path() + '/game/csgo/cfg/' + game_state_config
cfg_exists = os.path.isfile(game_state_path)

if not cfg_exists:
    print(f'Game State Integration file not found in CS2 directory, cloning file to {game_state_path}')
    shutil.copyfile(game_state_config, game_state_path)

# Start GSI Server
server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()

# Start Discord RPC
client_id = '613057930992025640'
RPC = Presence(client_id)
RPC.connect()

game_mode_names = {
    'scrimcomp2v2': 'Wingman',
}

while True:
    activity = server.get_info("player", "activity")

    if activity == "playing":
        game_mode_type = server.get_info('map', 'mode')
        t_wins = server.get_info('map', 'team_t')['score']
        ct_wins = server.get_info('map', 'team_ct')['score']
        map_name = server.get_info('map', 'name')
        team = server.get_info("player", "team")

        try:
            game_mode = game_mode_names[game_mode_type]
        except KeyError:
            # All other game modes have a proper name, as long as they're capitalized
            game_mode = game_mode_type.capitalize()

        large_image = map_name
        details = f'{activity.capitalize()} {game_mode}'
        state = f'[ {ct_wins} : {t_wins} ]' if team == 'CT' else f'[ {t_wins} : {ct_wins} ]'
        small_image = 'ct_logo' if team == 'CT' else 't_logo'

    elif activity == "menu":
        large_image = "menu"
        details = "In main menu"
        state = "  "
        small_image = None

    RPC.update(state=state, details=details, large_image=large_image, small_image=small_image)
    time.sleep(15)
