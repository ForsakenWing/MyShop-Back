#!/usr/bin/python
import os
from configparser import ConfigParser


def cfgparser(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(os.path.join(os.path.dirname(__file__) + '/configs', filename))

    # get section, default to postgresql
    cfg = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            cfg[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return cfg
