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


if __name__ == '__main__':
    inChain = dict()
    types = ["int", "string"]
    keywords = ["struct"]
    variables = set()
    leftBracket = False
    rightBracket = False

    with open("input.txt") as f:
        inFile = f.read()

    print(inFile.split("\n"))
    strings = inFile.split("\n")
    strings.remove('')

    for i, v in enumerate(strings):
        line = 1 + i
        column = 0
        b_index = 0
        e_index = 0

        if leftBracket is False and rightBracket is False:
            if line == 1:
                if "{" in v and "}" in v:
                    if ";" in v:
                        if len(v.split(" ")) == 3:
                            if "{};" in v.split(" ")[2]:
                                # 1
                                print(v.split(" "), "1")
                        else:
                            if keywords[0] in v.split(" ")[0]:
                                if "{" in v.split(" ")[1]:
                                    print(f"Ожидался один пробел в "
                                          f"позиции "
                                          f"{re.search('{', v).span()[0] + 1},"
                                          f" строка {line}"
                                          " перед '{' ")
                    else:
                        print(v.split(" "), "err")
                        if len(v.split(" ")) == 3:
                            if "{}" in v.split(" ")[2]:
                                print(f"Ожидался знак ';' в позиции "
                                      f"{re.search('}', v).span()[1] + 1} "
                                      f"строка {line}")
                        elif len(v.split(" ")) == 2:
                            if "{}" in v.split(" ")[1]:
                                print(f"Ожидался пробел "
                                      f"в позиции "
                                      f"{re.search('{', v).span()[0] + 1} "
                                      f"строка {line}")
                elif "{" in v:
                    if len(v.split(" ")) == 3:
                        print(v.split(" "), "3")
                        leftBracket = True
                    else:
                        print(f"Ожидался пробел в позиции "
                              f"{re.search('{', v).span()[0]} строка {line}")
                elif ";" in v:
                    print(v, "2")
                else:
                    print("Ожидался знак '{' "
                          f"либо ';' в позиции {len(v.rstrip(' '))+1}")

        elif leftBracket is True and rightBracket is False:
            if "}" not in v:
                resp = varDeclaration(v)
                if ";" == v[len(v) - 1]:
                    if resp[0] in types and resp[1] != 1 and resp[2] == 1 and \
                            resp[3] == 1:
                        print(v, f"Строка {line}", "4")
                    elif resp[0] in types and resp[1] != 1 and resp [2] == "=" \
                            and resp[3] != 1:
                        print(v, f"Строка {line}", "5")
                else:
                    print(f"Ожидался знак ';' либо '=' "
                          f"в позиции {len(v) + 1} строка {line}")
                    break
            else:
                rightBracket = True
                print(v, "6")
        elif leftBracket is True and rightBracket is True:
            print("THE END")
        else:
            print(f"Неожиданный сценарий - {i},{v}")
