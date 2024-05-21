import yaml

from run import DIR, Environ


class YamlRead:
    @staticmethod
    def env_config():
        with open(file=f'{DIR}/config/env_data/{Environ}/data_env.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def data_config():
        with open(file=f'{DIR}/config/data/config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)