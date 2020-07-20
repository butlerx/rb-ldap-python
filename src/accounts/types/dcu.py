"""dcu ad user"""

import re

import attr

DCU_ATTR = [
    "employeeNumber",
    "displayName",
    "mail",
    "physicalDeliveryOfficeName",
]


@attr.s(auto_attribs=True)
class DCUUser:
    """DCU AD user info"""

    role: str
    displayName: str  # Full name
    mail: str  # DCU email
    id: int  # DCU ID number
    course: str  # DCU course code
    year: int  # DCU course year number/code

    def __str__(self) -> str:
        return f"""User Information
================
role: {self.role}
displayName: {self.displayName}
mail: {self.mail}
id: {self.id}
course: {self.course}
year: {self.year}"""

    @classmethod
    def from_ldap(cls, user: dict) -> "DCUUser":
        """convert ldap response in to an DCUUser"""
        match = re.search(
            "(?P<course>[A-Z]+)(?P<year>[0-9]+)", user["physicalDeliveryOfficeName"][0]
        )
        course_year = match.groupdict() or {"course": "Not found", "year": "Not found"}
        return cls(
            role=user["dn"].rdns[1][1],
            displayName=user["displayName"][0],
            mail=user["mail"][0],
            id=user["employeeNumber"][0],
            **course_year,
        )
