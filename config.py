import yaml
class Config():
    def __init__(self):
        self.options_dict = {}
        with open('config.yaml') as file:
            self.options_dict = yaml.load(file, Loader=yaml.Loader)