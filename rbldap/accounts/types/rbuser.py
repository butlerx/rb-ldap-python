"""ldap user"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

from bonsai import LDAPEntry

from ..gid import usertype_to_gid
from ..passwd import generate_passwd
from .dcu import DCUUser

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

    @property
    def dn(self) -> str:
        """
        get users dn

        Returns:
            formatted string of user dn in ldap
        """
        return f"uid={self.uid},ou=accounts,o=redbrick"

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
        """
        convert ldap response in to an RBUser

        Args:
            user: dictionary returned from bonsai with user info

        Return:
            User with details from ldap dict
        """
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        return cls(
            uid=user["attributes"]["uid"][0],
            usertype=user["attributes"]["usertype"][0],
            object_class=user["attributes"]["objectClass"],
            newbie=user["attributes"]["newbie"][0],
            cn=user["attributes"]["cn"][0],
            altmail=user["attributes"]["altmail"][0],
            id=user["attributes"]["id"][0],
            course=user["attributes"]["course"][0],
            year=user["attributes"]["year"][0],
            years_paid=user["attributes"]["yearsPaid"][0],
            updated_by=user["attributes"]["updatedBy"][0],
            updated=datetime.strptime(user["attributes"]["updated"][0], date_format),
            created_by=user["attributes"]["createdBy"][0],
            created=datetime.strptime(user["attributes"]["created"][0], date_format),
            birthday=datetime.strptime(user["attributes"]["birthday"][0], date_format),
            uid_number=user["attributes"]["uidNumber"][0],
            gid_number=user["attributes"]["gidNumber"][0],
            gecos=user["attributes"]["gecos"],
            login_shell=user["attributes"]["loginShell"][0],
            home_directory=user["attributes"]["homeDirectory"][0],
            user_password=user["attributes"]["userPassword"][0],
            host=user["attributes"]["host"],
            shadow_last_change=user["attributes"]["shadowLastChange"][0],
        )

    @classmethod
    def from_dcu(
        cls,
        student: DCUUser,
        username: str,
        uid: int,
        created_by: str,
        hosts: List[str],
    ) -> "RBUser":
        """
        Convert dcu account to rb
        This is used for creating new rb accounts

        Args:
            student: dcu account to be used for creating rb account
            username: username to check
            uid: user id for new user
            created_by: person creating the account
            hosts: list of hosts user can access

        Return:
            User with details from dcu account
        """

        return cls(
            uid=username,
            usertype=student.usertype,
            object_class=[student.usertype, "posixAccount", "top", "shadowAccount"],
            newbie=True,
            cn=student.display_name,
            altmail=student.mail,
            id=student.id,
            course=student.course,
            year=student.year,
            years_paid=1,
            updated_by=created_by,
            updated=datetime.now(),
            created_by=created_by,
            created=datetime.now(),
            birthday=student.birthday,
            uid_number=uid,
            gid_number=usertype_to_gid(student.usertype),
            gecos=[student.display_name],
            login_shell="/usr/local/shells/shell",
            home_directory=f"/home/{student.usertype}/{username[:1]}/{username}",
            user_password=generate_passwd(12),
            host=hosts,
            shadow_last_change=0,
        )

    def to_ldap(self) -> LDAPEntry:
        """
        format class for writing to ldap

        Return:
            LDAPEntry for writing to ldap
        """
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        user = LDAPEntry(f"uid={self.uid},ou=accounts,o=redbrick")
        user["uid"] = self.uid
        user["usertype"] = self.usertype
        user["objectClass"] = self.object_class
        user["newbie"] = self.newbie
        user["cn"] = self.cn
        user["altmail"] = self.altmail
        user["id"] = self.id
        user["course"] = self.course
        user["year"] = self.year
        user["yearsPaid"] = self.years_paid
        user["updatedBy"] = self.updated_by
        user["updated"] = self.updated.strftime(date_format)
        user["createdBy"] = self.created_by
        user["created"] = self.created.strftime(date_format)
        user["birthday"] = self.birthday.strftime(date_format)
        user["uidNumber"] = self.uid_number
        user["gidNumber"] = self.gid_number
        user["gecos"] = self.gecos
        user["loginShell"] = self.login_shell
        user["homeDirectory"] = self.home_directory
        user["userPassword"] = self.user_password
        user["host"] = self.host
        user["shadowLastChange"] = (
            [self.shadow_last_change] if self.shadow_last_change != 0 else []
        )
        return user
