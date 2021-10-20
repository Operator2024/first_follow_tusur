import re
from typing import Text, Any, Set


def varDeclaration(a: Text) -> Any:
    if "=" in a:
        eqSign = re.findall("={1,}", a)
        if len(eqSign[0]) > 1:
            return 1, 1, eqSign[0], 1, 1
        else:
            _tmp = re.split("=", a.lstrip(" ").rstrip(" "))
            _name = _tmp[0].lstrip(" ").rstrip(" ").split(" ")[1]
            _type = _tmp[0].lstrip(" ").rstrip(" ").split(" ")[0]
            _expr = re.sub(";", "", _tmp[1].lstrip(" ").rstrip(" "))
            return _type, _name, eqSign[0], _expr, ";"
    elif ";" in a:
        _tmp = re.split(";", a.lstrip(" ").rstrip(" "))
        if _tmp[len(_tmp) - 1] == "":
            _type = _tmp[0].lstrip(" ").rstrip(" ").split(" ")[0]
            _name = _tmp[0].lstrip(" ").rstrip(" ").split(" ")[1]
        else:
            return 1, 1, 1, 1, 1
        return _type, _name, 1, 1, ";"
    else:
        return 1, 1, 1, 1, 1


def varConflict(var: Text, evars: Set) -> bool:
    if var in evars:
        return True
    else:
        return False
