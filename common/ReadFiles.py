import yaml

from run import DIR, Environ


class YamlRead:
    @staticmethod
    def env_config():
        with open(file=r'{}/config/env/{}/test_env.yml'.format(DIR,Environ), mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def data_config():
        with open(file=r'{}/config/env/{}/test_env.yml'.format(DIR,Environ), mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
