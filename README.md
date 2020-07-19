# rbldap

Script to interact with Redbrick LDAP.

## Features

- Search for users in ldap
- Create a new Redbrick user
- Renew a user
- convert a users usertype
- edit user info
- reset a user's password and shell
- disable and renable a user account
- remove and lock unpaid accounts
- Alert all unpaid users there accounts have been disabled and they need to
  renew
- Delete all user who have not paid for 2 years
- Disable all unpaid user accounts and notify the user the account is disabled
- Preform yearly update
  - set newbie to false
  - decrement years paid by one
  - disable all accounts with years paid at 0.
  - delete all accounts with years paid of -1

## Run

```bash
rbldap [global options] command [command options] [arguments...]
```

Run `rbldap -h` to get a list of flags and commands.

```bash
$ rbldap --help
NAME:
   rbldap - Command line interface for Redbrick LDAP

USAGE:
   rbldap [global options] command [command options] [arguments...]


COMMANDS:
     add               Add user to ldap
     disable           Disable a Users ldap account
     renable           Renable a Users ldap account
     renew             renew a LDAP user
     reset             reset a users password
     reset-shell       reset a users shell
     search            Search ldap for user
     update            Update a user in ldap
     help, h           Shows a list of commands or help for one command

   Batch Commands:
     alert-unpaid    Alert all unpaid users that their accounts will be disabled
     delete-unpaid   Delete all unpaid users accounts that are outside their grace period
     disable-unpaid  Diable all unpaid users accounts
     new-year        Decriment Years Paid of all users to 1

GLOBAL OPTIONS:
   --user value, -u value  ldap user, used for authentication (default: "cn=root,ou=ldap,o=redbrick")
   --dcu-user value        Active Directory user for DCU, used for authentication (default: "CN=rblookup,OU=Service Accounts,DC=ad,DC=dcu,DC=ie")
   --host value            ldap host to query (default: "ldap.internal")
   --dcu-host value        DCU Active Directory host to query (default: "ad.dcu.ie")
   --port value, -p value  Port for ldap host (default: 389)
   --dcu-port value        Port for DCU Active Directory host (default: 389)
   --password value        password for the ldap server [/etc/ldap.secret]
   --dcu-password value    password for the DCU ldap server [/etc/dcu_ldap.secret]
   --smtp value            smtp server to send email with [smtp.redbrick.dcu.ie]
   --dry-run               output to console rather then file
   --help, -h              show help
   --version, -v           print the version
```
