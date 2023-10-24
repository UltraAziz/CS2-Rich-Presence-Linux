import time
from pypresence import Presence
from server import GSIServer
import winreg
import struct
import os
import shutil

game_state_config = 'gamestate_integration_GSI.cfg'
def get_steam_path():
    try:
        hKey = None
        if (8 * struct.calcsize("P")) == 64:
            hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Wow6432Node\\Valve\\Steam')
        else:
            hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Valve\\Steam')

        path = winreg.QueryValueEx(hKey, "InstallPath")
        winreg.CloseKey(hKey)
        return str(path[0])
    except:
        return None


# Initial setup
game_state_path = get_steam_path() + '\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\cfg\\' + game_state_config
cfg_exists = os.path.isfile(game_state_path)

if not cfg_exists:
    with open(game_state_config, 'r'):
        print(f'Game State Integration file not found in CS2 directory, cloning file to {game_state_path}')
        shutil.copyfile(game_state_config, game_state_path)

# Start GSI Server
server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()

# Start Discord RPC
client_id = '613057930992025640'
RPC = Presence(client_id)
RPC.connect()

while True:
    activity = server.get_info("player", "activity").capitalize()

    if activity == "Playing":
        game_mode = server.get_info('map', 'mode').capitalize()
        t_wins = server.get_info('map', 'team_t')['score']
        ct_wins = server.get_info('map', 'team_ct')['score']
        map_name = server.get_info('map', 'name')
        team = server.get_info("player", "team")

        large_image = map_name
        details = f'{activity} {game_mode}'
        state = f'[ {t_wins} : {ct_wins} ]'
        small_image = 'ct_logo' if 'CT' else 't_logo'

    elif activity == "Menu":
        large_image = "menu"
        details = "In main menu"
        state = "  "
        small_image = None

    RPC.update(state=state, details=details, large_image=large_image, small_image=small_image)
    time.sleep(15)
