usage: rb-ldap [-h] [--version] [--user USER] [--dcu-user DCU_USER] [--host HOST] [--dcu-host DCU_HOST] [--port PORT] [--dcu-port DCU_PORT] [--password PASSWORD]
               [--dcu-password DCU_PASSWORD] [--smtp SMTP] [--dry-run]
               COMMAND ...

Command line interface for Redbrick LDAP

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         Show the version
  --user USER           ldap user, used for authentication
  --dcu-user DCU_USER   Active Directory user for DCU, used for authentication
  --host HOST           ldap host to query
  --dcu-host DCU_HOST   DCU Active Directory host to query
  --port PORT           Port for ldap host
  --dcu-port DCU_PORT   Port for DCU Active Directory host
  --password PASSWORD   path to file containing the password for the ldap server
  --dcu-password DCU_PASSWORD
                        path to file containing the password for the DCU AD server"
  --smtp SMTP           smtp server to send email with
  --dry-run             output to console rather then file

command:
  COMMAND               Command to run
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
