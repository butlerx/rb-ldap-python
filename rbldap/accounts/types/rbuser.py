"""ldap user"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

RB_ATTR = [
    "uid",
    "usertype",
    "objectClass",
    "newbie",
    "cn",
    "altmail",
    "id",
    "course",
    "year",
    "yearsPaid",
    "updatedBy",
    "updated",
    "createdBy",
    "created",
    "birthday",
    "uidNumber",
    "gidNumber",
    "gecos",
    "loginShell",
    "homeDirectory",
    "userPassword",
    "host",
    "shadowLastChange",
]


@dataclass
class RBUser:
    """Redbrick LDAP user info"""

    uid: str
    usertype: str
    object_class: List[str]
    newbie: bool  # New this year
    cn: str  # Full name
    altmail: str  # Alternate email
    id: int  # DCU ID number
    course: str  # DCU course code
    year: int  # DCU course year number/code
    years_paid: int  # Number of years paid (integer)
    updated_by: str  # Username of user last to update
    updated: datetime
    created_by: str  # Username of user that created them
    created: datetime
    birthday: datetime
    uid_number: int
    gid_number: int
    gecos: List[str]
    login_shell: str
    home_directory: str
    user_password: str  # Crypted password.
    host: List[str]  # List of hosts.
    shadow_last_change: int

    def __str__(self) -> str:
        date_format = "%Y-%m-%d %H:%M:%S"
        return f"""User Information
================
uid: {self.uid}
usertype: {self.usertype}
objectClass: {", ".join(self.object_class)}
newbie: {self.newbie}
cn: {self.cn}
altmail: {self.altmail}
id: {self.id}
course: {self.course}
year: {self.year}
yearsPaid: {self.years_paid}
updatedBy: {self.updated_by}
updated: {self.updated.strftime(date_format)}
createdBy: {self.created_by}
created: {self.created.strftime(date_format)}
birthday: {self.birthday.strftime(date_format)}
uidNumber: {self.uid_number}
gidNumber: {self.gid_number}
gecos: {", ".join(self.gecos)}
loginShell: {self.login_shell}
homeDirectory: {self.home_directory}
userPassword: {self.user_password}
host: {", ".join(self.host)}
shadowLastChange: {self.shadow_last_change}"""

    @classmethod
    def from_ldap(cls, user: dict) -> "RBUser":
        """convert ldap response in to an RBUser"""
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        return cls(
            uid=user["uid"][0],
            usertype=user["usertype"][0],
            object_class=user["objectClass"],
            newbie=user["newbie"][0],
            cn=user["cn"][0],
            altmail=user["altmail"][0],
            id=user["id"][0],
            course=user["course"][0],
            year=user["year"][0],
            years_paid=user["yearsPaid"][0],
            updated_by=user["updatedBy"][0],
            updated=datetime.strptime(user["updated"][0], date_format),
            created_by=user["createdBy"][0],
            created=datetime.strptime(user["created"][0], date_format),
            birthday=datetime.strptime(user["birthday"][0], date_format),
            uid_number=user["uidNumber"][0],
            gid_number=user["gidNumber"][0],
            gecos=user["gecos"],
            login_shell=user["loginShell"][0],
            home_directory=user["homeDirectory"][0],
            user_password=user["userPassword"][0],
            host=user["host"],
            shadow_last_change=user["shadowLastChange"][0],
        )
