import os

import yaml


class DeployConfig:
    def __init__(self):

        conf_file = "./settings/config.yaml"

        if not os.path.exists(conf_file):
            raise Exception('Config file path [%s] invalid!' % conf_file)

        with open(conf_file) as fp:
            configs = yaml.load(fp, Loader=yaml.FullLoader)
            deploy_conf = configs["FACE"]
            # 正数为GPU的ID，负数为使用CPU
            self.gpu_id = deploy_conf["GPU_ID"]
            self.face_db = deploy_conf["FACE_DB"]
            self.threshold = deploy_conf["THRESHOLD"]
            self.nms = deploy_conf["NMS"]


TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '127.0.0.1',
                'port': '3306',
                'user': 'root',
                'password': 'root',
                'database': 'ease-eyesight',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                'echo': True
            }
        }
    },
    'apps': {
        'models': {
            'models': ['pojo.po_models', 'aerich.models'],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}
