# rb-ldap

[![Build and Test](https://github.com/butlerx/rb-ldap-python/workflows/Build%20and%20Test/badge.svg)](https://github.com/butlerx/rb-ldap-python/actions)

Script to interact with Redbrick LDAP.

## Features

- Search for users in ldap
- Create a new Redbrick user
- Renew a user account
- Convert a users between usertype
- Edit user info
- Reset a user's password and shell
- Disable and re-enable a user account
- Remove and lock unpaid accounts
- Alert all unpaid users there accounts have been disabled and they need to
  renew
- Delete all user who have not paid for 2 years
- Disable all unpaid user accounts and notify the user the account is disabled
- Preform yearly update
  - Set newbie to false
  - Decrement years paid by one
  - Disable all accounts with years paid at 0.
  - Delete all accounts with years paid of -1

## Run

```bash
rb-ldap [global options] command [command options] [arguments...]
```

Run `rb-ldap -h` to get a list of flags and commands.

```bash
$ rb-ldap --help
Usage: rb-ldap [global options] command [command options] [arguments...]

Command line interface for Redbrick LDAP

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         Show the version
  --user value          ldap user, used for authentication (default: "cn=root,ou=ldap,o=redbrick")
  --dcu-user value      Active Directory user for DCU, used for authentication (default: "CN=rblookup,OU=Service Accounts,DC=ad,DC=dcu,DC=ie")
  --host value          ldap host to query (default: "ldap.internal")
  --dcu-host value      DCU Active Directory host to query (default: "ad.dcu.ie")
  --port value          Port for ldap host (default: 389)
  --dcu-port value      Port for DCU Active Directory host (default: 389)
  --password value      path to file containing the password for the ldap server (default: "/etc/ldap.secret")
  --dcu-password value  path to file containing the password for the DCU AD server (default: "/etc/dcu_ldap.secret")
  --smtp value          smtp server to send email with (default: "smtp.redbrick.dcu.ie")
  --dry-run             output to console rather then file

command:
    generate-docs       generate documentation for command line application
    add                 Add user to ldap
    search              Search ldap for user
    renew               Renew a LDAP user
    free                check if a username is free
    enable              Renable a Users LDAP Account
    disable             Disable a Users LDAP Account
    reset-password      Reset a users password
    reset-shell         Reset a user's login shell
    update              Update a user in ldap
    generate            Generate nix config for user vhosts based off ldap
    alert-unpaid        Send email to all users with unpaid account altmails telling them their account is unpaid
    delete-unpaid       Delete all unpaid users accounts that are outside their grace period (years paid = -1)
    disable-unpaid      Diable all unpaid users accounts (years paid = 0)
    new-year            To Be run at the beginning of each year prior to C&S

Version 1.0.0.dev0
Built by Redbrick <admins@redbrick.dcu.ie>, Cian Butler <butlerx@redbrick.dcu.ie>, Lucas Savva <m1cr0man@redbrick.dcu.ie>
```

## Development

Requirements:

- pipenv

Install dependencies:

```bash
pipenv install
```

Run Test:

```bash
pipenv run pytest
```

Build Wheel:

```bash
$ pipenv run flit build
Found 71 files tracked in git                                                             I-flit.sdist
Writing generated setup.py                                                                I-flit.sdist
Built sdist: dist/rbldap-1.0.0.dev0.tar.gz                                           I-flit_core.sdist
Copying package file(s) from /tmp/tmprb5ifr6l/rbldap-1.0.0.dev0/rbldap               I-flit_core.wheel
Writing metadata files                                                               I-flit_core.wheel
Writing the record of files                                                          I-flit_core.wheel
Built wheel: dist/rbldap-1.0.0.dev0-py3-none-any.whl                                 I-flit_core.wheel
```

Run `rb-ldap` locally
```bash
pipenv run python -m rbldap --help
```
