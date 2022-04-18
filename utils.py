import yaml


def read_yaml(path):
    with open(path, 'rb') as f:
        y = yaml.load(f.read(), Loader=yaml.FullLoader)
    return y