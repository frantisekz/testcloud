# -*- coding: utf-8 -*-
# Copyright 2015, Red Hat, Inc.
# License: GPL-2.0+ <http://spdx.org/licenses/GPL-2.0+>
# See the LICENSE file for more details on Licensing

import os
import types

import testcloud


DEFAULT_CONF_DIR = os.path.abspath(os.path.dirname(testcloud.__file__)) + '/../conf'

CONF_DIRS = [DEFAULT_CONF_DIR,
             '{}/.config/testcloud'.format(os.environ['HOME']),
             '/etc/testcloud'
             ]

CONF_FILE = 'settings.py'

_config = None


def get_config():
    '''Retrieve a config instance. If a config instance has already been parsed,
    reuse that parsed instance.

    :return: :class:`.ConfigData` containing configuration values
    '''

    global _config
    if not _config:
        _config = _parse_config()
    return _config


def _parse_config():
    '''Parse config file in a supported location and merge with default values.

    :return: loaded config data merged with defaults from :class:`.ConfigData`
    '''

    config = ConfigData()
    config_filename = _find_config_file()

    if config_filename is not None:
        loaded_config = _load_config(config_filename)
        config.merge_object(loaded_config)

    return config


def _find_config_file():
    '''Look in supported config dirs for a configuration file.

    :return: filename of first discovered file, None if no files are found
    '''

    for conf_dir in CONF_DIRS:
        conf_file = '{}/{}'.format(conf_dir, CONF_FILE)
        if os.path.exists(conf_file):
            return conf_file
    return None


def _load_config(conf_filename):
    '''Load configuration data from a python file. Only loads attrs which are
    named using all caps.

    :param conf_filename: full path to config file to load
    :type conf_filename: str
    :return: object containing configuration values
    '''

    new_conf = types.ModuleType('config')
    new_conf.__file__ = conf_filename
    try:
        with open(conf_filename, 'r') as conf_file:
            exec(compile(conf_file.read(), conf_filename, 'exec'),
                 new_conf.__dict__)
    except IOError as e:
        e.strerror = 'Unable to load config file {}'.format(e.strerror)
        raise
    return new_conf


class ConfigData(object):
    '''Holds configuration data for TestCloud. Is initialized with default
    values which can be overridden.
    '''

    DOWNLOAD_PROGRESS = True
    LOG_FILE = None

    # Directories testcloud cares about

    DATA_DIR = "/var/lib/testcloud"
    STORE_DIR = "/var/lib/testcloud/backingstores"

    # libvirt domain XML Template
    # This lives either in the DEFAULT_CONF_DIR or DATA_DIR
    XML_TEMPLATE = "domain-template.jinja"
    XML_TEMPLATE_COREOS = "domain-coreos-template.jinja"

    # Data for cloud-init

    PASSWORD = 'passw0rd'
    HOSTNAME = 'testcloud'

    META_DATA = """instance-id: iid-123456
local-hostname: %s
    """
    USER_DATA = """#cloud-config
password: %s
chpasswd: { expire: False }
ssh_pwauth: True
    """
    ATOMIC_USER_DATA = """#cloud-config
password: %s
chpasswd: { expire: False }
ssh_pwauth: True
runcmd:
  - [ sh, -c, 'echo -e "ROOT_SIZE=4G\nDATA_SIZE=10G" > /etc/sysconfig/docker-storage-setup']
    """
    COREOS_DATA = """variant: fcos
version: 1.3.0
passwd:
  users:
    - name: coreos
      ssh_authorized_keys:
        - %s
    """

    # Extra cmdline args for the qemu invocation.
    # Customize as needed :)
    CMD_LINE_ARGS = []
    CMD_LINE_ENVS = {}

    # Extra coreos cmdline args for the qemu invocation.
    # Customize as needed :)
    CMD_LINE_ARGS_COREOS = ['-fw_cfg' ,]
    CMD_LINE_ENVS_COREOS = {}
    # timeout, in seconds for instance boot process
    BOOT_TIMEOUT = 45

    # Maximum space (in GiB) that unused images can occupy in /var/lib/testcloud/backingstores directory
    # Once the limit is reached, testcloud will attempt to remove oldest files
    # before creating a new instance
    # 0 = unlimited
    BACKINGSTORE_SIZE = 0

    # ram size, in MiB
    RAM = 768
    RAM_COREOS = 2048

    # Desired size, in GiB of instance disks. 0 leaves disk capacity
    # identical to source image
    DISK_SIZE = 0
    DISK_SIZE_COREOS = 10

    # Number of retries when stopping of instance fails (host is busy)
    STOP_RETRIES = 3

    # Waiting time between stop retries, in seconds
    STOP_RETRY_WAIT = 1

    # Desired VM type: False = BIOS, True = UEFI
    UEFI = False

    #stream of Coreos repo
    STREAM = 'testing'

    #stream list of Coreos repo
    STREAM_LIST = ['testing', 'stable', 'next']

    #version of fedora repo
    VERSION = 'latest'

    #number of vcpu
    VCPUS = 2
    # Port base for userspace sessions for SSH forward
    SSH_USER_PORT_BASE = 10022

    def merge_object(self, obj):
        '''Overwrites default values with values from a python object which have
        names containing all upper case letters.

        :param obj: python object containing configuration values
        :type obj: python object
        '''

        for key in dir(obj):
            if key.isupper():
                setattr(self, key, getattr(obj, key))
