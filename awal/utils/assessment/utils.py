# Utils
# Auteur: Cédric Fayet

import json
import jsonschema
import time
import os
import shutil
import threading
from threading import Timer
import yaml
import csv
import random
import string
import roots
import csv
import math

# import src.SysFile as sfile

# # GLOBAL VARIABLES
# CONFIG = None
# OPENAPI_doc_origin = "./specification/REST.yaml"
# CONFIG_specification = "./specification/config.schema.json"

# # Chargement du fichier de config json
# def load_config(config_file):
#     global CONFIG

#     with open(CONFIG_specification) as json_specification:
#         json_specification = json.load(json_specification)

#     with open(config_file,"rt", encoding='utf8') as json_config:
#         json_config = json.load(json_config)

#     jsonschema.validate(instance=json_config,schema=json_specification)

#     # CONFIG
#     CONFIG = json_config
#     CONFIG["adhoc"]={}

#     # Init
#     tmp_dir = sfile.Directory("tmp",CONFIG["settings"]["tempory_files"]["directory"])
#     tmp_dir.create("config.adhoc")

# def load_openapi():

#     with open(OPENAPI_doc_origin,"rt", encoding='utf8') as yaml_data:
#         OPENAPI_spec = yaml.full_load(yaml_data)

#     # INFOS
#     if not("servers" in OPENAPI_spec):
#         OPENAPI_spec["servers"] = []

#     tmp = {}
#     tmp["url"] = CONFIG["settings"]["server"]["url"]
#     tmp["description"] = "R.E.S.T Server"

#     OPENAPI_spec["servers"].append(tmp)

#     # SAVE
#     with open(sfile.File.path("tmp","config.adhoc","openapi.yaml"),'w') as yaml_file:
#         yaml.dump(OPENAPI_spec, yaml_file)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def arr_cleaning(z):
    _Z = []
    for sz in z:
        if sz ==  "":
            pass
        else:
            _Z.append(sz)

    return _Z
