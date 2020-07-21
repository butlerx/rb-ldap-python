"""redbrick GID"""
GROUPS = [
    ("associat", 107),
    ("club", 102),
    ("committe", 100),
    ("dcu", 31382),
    ("founder", 105),
    ("intersoc", 1016),
    ("member", 103),
    ("projects", 1014),
    ("redbrick", 1017),
    ("society", 101),
    ("staff", 109),
]


def gid_to_usertype(gid: int) -> str:
    """
    convert gid to usertype

    Args:
        gid: the redbrick group id to look up

    Returns:
        The name of the group or an empty string if none found
    """
    for group in GROUPS:
        if group[1] == gid:
            return group[0]
    return ""


def usertype_to_gid(group_name: str) -> int:
    """
    convert user type to gid

    Args:
        group_name: the redbrick group name to look up

    Returns:
        The gid of the given group or 0 if none match
    """
    for group in GROUPS:
        if group[0] == group_name:
            return group[1]
    return 0
