# Commented out default values with details are displayed below. If you want
# to change the values, make sure this file is available in one of the three
# supported config locations:
# - conf/settings.py in the git checkout
# - ~/.config/testcloud/settings.py
# - /etc/testcloud/settings.py


#DOWNLOAD_PROGRESS = True
#LOG_FILE = None


## Directories for data and cached downloaded images ##

#DATA_DIR = "/var/lib/testcloud/"
#STORE_DIR = "/var/lib/testcloud/backingstores"


## Data for cloud-init ##

#PASSWORD = 'passw0rd'
#HOSTNAME = 'testcloud'

#META_DATA = """instance-id: iid-123456
#local-hostname: %s
#"""
## Read http://cloudinit.readthedocs.io/en/latest/topics/examples.html to see
## what options you can use here.
#USER_DATA = """#cloud-config
#password: %s
#chpasswd: { expire: False }
#ssh_pwauth: True
#"""
#ATOMIC_USER_DATA = """#cloud-config
#password: %s
#chpasswd: { expire: False }
#ssh_pwauth: True
#runcmd:
#  - [ sh, -c, 'echo -e "ROOT_SIZE=4G\nDATA_SIZE=10G" > /etc/sysconfig/docker-storage-setup']
#"""


## Extra cmdline args for the qemu invocation ##
## Customize as needed :)

#CMD_LINE_ARGS = []
#CMD_LINE_ENVS = {}

# The timeout, in seconds, to wait for an instance to boot before
# failing the boot process. Setting this to 0 disables waiting and
# returns immediately after starting the boot process.
#BOOT_TIMEOUT = 30

# Maximum space (in GiB) that unused images can occupy in /var/lib/testcloud/backingstores directory
# Once the limit is reached, testcloud will attempt to remove oldest files
# before creating a new instance
# 0 = unlimited
BACKINGSTORE_SIZE = 2

# ram size, in MiB
#RAM = 768

# Desired size, in GiB of instance disks. 0 leaves disk capacity
# identical to source image
#DISK_SIZE = 0

# Number of retries when stopping of instance fails (host is busy)
#STOP_RETRIES = 3

# Waiting time between stop retries, in seconds
#STOP_RETRY_WAIT = 1

# Desired VM type: False = BIOS, True = UEFI
#UEFI = False
