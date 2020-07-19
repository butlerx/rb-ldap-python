"""Version Info"""

TEAM_EMAIL = "admins@redbrick.dcu.ie"
PROJECT_HOME = "https://github.com/redbrick/rb-ldap-python"
PACKAGE_INFO = "Command line interface for Redbrick LDAP"
PACKAGE_LICENSE = "Apache 2"
OWNERS = [
    dict(name="Redbrick", email=TEAM_EMAIL),
    dict(name="Cian Butler", email="butlerx@redbrick.dcu.ie"),
    dict(name="Lucas Savva", email="m1cr0man@redbrick.dcu.ie"),
]

__version__ = "1.0.0-dev"
__author__ = ", ".join("{name} <{email}>".format(**info) for info in OWNERS)
