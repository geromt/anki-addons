from aqt import mw
import os.path


def get_config():
    config = mw.addonManager.getConfig("AutomaticBackup")
    config = validate_config(config)
    return config


def validate_config(config):
    # Validate the user
    if mw.pm.name in config:
        conf = config[mw.pm.name]
    else:
        conf = config

    if conf.get("backup_dir"):
        if not os.path.isdir(conf["backup_dir"]):
            raise ConfigError("backup_dir is not a directory")
    else:
        raise ConfigError("You must provide a directory for the backup")

    if not config.get("compress_colpkg"):
        conf["compress_colpkg"] = False

    if config.get("include_media"):
        if not config.get("compress_media"):
            conf["compress_media"] = False
    else:
        conf["include_media"] = False

    if config.get("upload_to_cloud"):
        if not config.get("remote"):
            raise ConfigError("You must provide the remote's name")
    else:
        conf["upload_to_cloud"] = False

    return conf


class ConfigError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(message)
