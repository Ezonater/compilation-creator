import yaml
class Config():
    def __init__(self):
        self.options_dict = {}
        with open('config.yaml') as file:
            self.options_dict = yaml.load(file, Loader=yaml.Loader)

    def edit_config(self, key, value):
        self.options_dict[key] = value
        with open('config.yaml', 'w') as outfile:
            yaml.dump(self.options_dict, outfile, default_flow_style=False)
        print(self.options_dict)