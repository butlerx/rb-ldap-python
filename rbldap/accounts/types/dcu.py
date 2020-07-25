"""dcu ad user"""

import datetime
import re
from dataclasses import dataclass

DCU_ATTR = [
    "employeeNumber",
    "displayName",
    "mail",
    "physicalDeliveryOfficeName",
    "birthday",  # TODO: double check if correct key
]


@dataclass
class DCUUser:
    """DCU AD user info"""

    role: str
    display_name: str  # Full name
    mail: str  # DCU email
    id: int  # DCU ID number
    course: str  # DCU course code
    year: int  # DCU course year number/code
    birthday: datetime

    def __str__(self) -> str:
        return f"""User Information
================
role: {self.role}
displayName: {self.display_name}
mail: {self.mail}
id: {self.id}
course: {self.course}
year: {self.year}"""

    @classmethod
    def from_ldap(cls, user: dict) -> "DCUUser":
        """convert ldap response in to an DCUUser"""
        match = re.search(
            "(?P<course>[A-Z]+)(?P<year>[0-9]+)",
            user["attributes"]["physicalDeliveryOfficeName"][0],
        )
        return cls(
            role=user["dn"].rdns[1][1],
            display_name=user["attributes"]["displayName"][0],
            mail=user["attributes"]["mail"][0],
            id=user["attributes"]["employeeNumber"][0],
            course=match.groupdict("course"),
            year=match.groupdict("year"),
            birthday=user["attributes"]["birthday"][0],
        )

    @property
    def usertype(self) -> str:
        """
        convert dcu role to rb usertype

        Return:
            the matching usertype of self.role as string
        """
        if self.role == "Student":
            return "member"
        if self.role == "Staff":
            return "staff"
        if self.role == "Alumni":
            return "associat"
        return "member"
