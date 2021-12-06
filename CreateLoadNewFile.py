#CreateLoadNewFile

from ds_messenger import DirectMessenger
import os
from pathlib import Path

def C_command(user, pwd, server, user_input):
    """
    Accept a string. Create a new file, append it with the suffix
    .dsu, and return the path of the newly created file. Also collects
    user data to build a profile including a username, password, dsueserver,
    and optional bio.
    """
    username = user
    password = pwd
    dsuserver = server
    current_profile = DirectMessenger(server, user, pwd)
    user_path = user_input[:user_input.rfind('-n') - 1]
    file_name = user_input[user_input.rfind('-n') + 3:]
    path = os.path.join(user_path, file_name + '.dsu')
    Path(path).touch()
    current_profile.save_profile(path)
    return path


def O_command(user_input):
    p = Path(user_input)
    if os.path.exists(p) and p.suffix == '.dsu':
        f = open(p)
        print(p, 'has been successfully loaded.\n')
