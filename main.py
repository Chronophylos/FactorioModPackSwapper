import yaml
from termcolor import cprint, colored
from colorama import init
import os
import shutil
init()

class ConfigError(Exception):
    pass

class Config:
    symlink: bool
    dir: str
    mods: str
    backup: str
    modpacks = list()

    def __init__(self, yml):
        self.symlink = yml['symlink'] if 'symlink' in yml else True

        if not 'config' in yml:
            raise ConfigError('Missing key "config".')
        self.dir = Config.parse_path(yml['config'])
        if not os.path.exists(self.dir):
            raise ConfigError(f'Could not locate factorio config directory ({self.dir}).')
        if not os.path.isdir(self.dir):
            raise ConfigError(f'Factorio config directory ({self.dir}) is not a directory.')
        print(self.dir)

        self.mods = os.path.join(self.dir, 'mods')
        if not os.path.exists(self.dir):
            raise ConfigError(f'Could not locate mods directory ({self.mods}).')
        if not os.path.isdir(self.dir):
            raise ConfigError(f'Mods directory ({self.mods}) is not a directory.')

        self.backup = os.path.join(self.dir, 'backup')

        if not 'modpacks' in yml:
            raise ConfigError('Missing key "modpacks".')
        for k, v in yml['modpacks'].items():
            try:
                self.modpacks.append(ModPack(k, v, self))
            except ConfigError as e:
                cprint("[WARNING] " + str(e), "yellow")
    
    @staticmethod
    def parse_path(path):
        path = os.path.expandvars(path)
        path = os.path.expanduser(path)
        return os.path.normpath(path)

class ModPack:
    name: str
    symlink: bool
    dir: str
    mods: list

    def __init__(self, name, yml, config):
        self.name = name
        self.symlink = yml['symlink'] if 'symlink' in yml else config.symlink

        if not 'directory' in yml:
            raise ConfigError(f'Missing key "directory" in "{name}" in "modpacks".')
        self.dir = Config.parse_path(os.path.join(config.dir, 'modpacks', yml['directory']))
        if not os.path.exists(self.dir):
            raise ConfigError(f'Could not locate modpack directory ({self.dir}).')
        if not os.path.isdir(self.dir):
            raise ConfigError(f'Modpack directory ({self.dir}) is not a directory.')

        self.mods = yml['mods'] if 'mods' in yml else None

def load_config(config_file="fmps.yml"):
    with open(config_file, 'r+') as config_file:
        config = yaml.load(config_file)
        try:
            config = Config(config)
        except ConfigError as e:
            cprint('[ERROR] ' + str(e), 'red')
            return
        main(config)

def main(config):
    print('Select modpack to load:')
    for i, modpack in enumerate(config.modpacks):
        print(f'{i}: {modpack.name}')
    try:
        selection = input('Select a modpack to load or type exit to quit: ')
    except AttributeError:
        main(config)
    if selection in ['exit', 'quit']:
        return
    try:
        modpack = config.modpacks[int(selection)]
    except KeyError:
        main(config)
    
    load(modpack, config)

def clear_mods(target, backup):
    print('Backing up mods directory to ' + backup)
    try:
        shutil.rmtree(backup)
    finally:
        os.mkdir(backup)
    try:
        for mod_file in os.listdir(target):
            mod_file = os.path.join(target, mod_file)
            shutil.move(mod_file, backup)
    except FileNotFoundError as e:
        print(e)


def load(modpack, config):
    print(f'Loading \'{colored(modpack.name, "green")}\'')
    if input('continue? [Y/n]: ').lower() in ['y', '']:
       
        clear_mods(config.mods, config.backup)
        if config.symlink:
            print('Linking files')
        else:
            print('Copying files')
        for mod_file in os.listdir(modpack.dir):
            try:
                mod_path = os.path.join(modpack.dir, mod_file)
                if config.symlink:
                    print(mod_file +  ' -> ' + os.symlink(mod_path, config.mods))
                else:
                    print(mod_file + ' -> ' + shutil.copy2(mod_path, config.mods))
            except FileNotFoundError as e:
                print(e)


if __name__ == '__main__':
    try:
        load_config()
    except FileNotFoundError as e:
        cprint('[Error] No config file.', 'red')
        link = colored('https://github.com/Chronophylos/FactorioModPackSwapper', attrs=['underline'])
        print(f'Checkout the example config at {link}.')