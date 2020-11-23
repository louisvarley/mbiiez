import os

class globals:

    verbose = False
    script_path = os.path.dirname(os.path.realpath(__file__ + "/../../"))
    game_path = "/opt/openjk"
    mbii_path = game_path + "/MBII"
    base_path = game_path + "/opt/openjk/base"
    config_path = script_path + "/configs"
    engine = "openjkded.i386"
    game = "MBII"