import yaml
import logging


class Config:

    @staticmethod
    def get_param(section, param):
        """
        Static method for getting param from config.yaml
        :param section:
        :param param:
        :return: Getting param
        """
        config = Config.get_config()
        return config[section][param]

    @staticmethod
    def get_config():
        """
        Trying open config file or errors logging
        :return: Set - config params
        """
        with open("config.yaml") as file_handler:
            try:
                config = yaml.load(file_handler, Loader=yaml.FullLoader)
            except yaml.YAMLError as e:
                logging.error("Can't load config file " + str(e))

        return config
