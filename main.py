import re
import time
from copy import copy, deepcopy
from typing import List, Dict, Tuple, Text, Set

filename = "input.txt"


def f(_htable: Dict, _rules: List) -> Tuple[Dict, List]:
    _del_rules = set()
    for z in range(0, len(_rules)):
        left = _rules[z].split("->")[0].rstrip(" ").lstrip("")
        right = _rules[z].split("->")[1].lstrip(" ").rstrip(" ").split(" ")
        for x in right:
            if _htable[x] == "Y":
                _rules[z] = re.sub(f" {x}", "", _rules[z])
                if len(_rules[z].split("->")[1].lstrip(" ").rstrip(" ")) == 0:
                    _htable[left] = "Y"
                    _del_rules.add((_rules[z], left))
            elif _htable[x] == "N":
                _htable[left] = "N"
                _del_rules.add((_rules[z], left))
            elif _htable[x] == "U":
                pass
            else:
                pass

    for x in range(0, len(_rules)):
        left = _rules[x].split("->")[0].rstrip(" ").lstrip("")
        for _, z in _del_rules:
            if z == left:
                _rules[x] = "D"

    while True:
        if "D" in _rules:
            _rules.remove("D")
        else:
            break

    return _htable, _rules


def ll_verifier() -> Dict:
    loc_rule = []
    # N - non terminal, T - terminal
    N = set()
    T = set()
    H = dict()
    # deleted item
    D = set()
    D1 = set()
    with open(filename) as file:
        for i in file:
            if i == '\n':
                pass
            else:
                loc_rule.append(i.rstrip("\n"))

    for j in loc_rule:
        N.add(j.split("->")[0].rstrip(" ").lstrip(" "))
        H[j.split("->")[0].rstrip(" ").lstrip(" ")] = "U"

    for t in loc_rule:
        for k in t.split("->")[1].lstrip(" ").rstrip(" ").split(" "):
            if k not in N and k != "e":
                T.add(k)

    _rule = deepcopy(loc_rule)
    for i in _rule:
        _N = i.split("->")[0].rstrip(" ").lstrip("")
        for j in i.split("->")[1].lstrip(" ").rstrip(" ").split(" "):
            if j in T:
                if i in loc_rule:
                    loc_rule.remove(i)
                    D.add(_N)

    # page 100-102 stud book
    for j in D:
        trigger = 0
        for i in loc_rule:
            _N = i.split("->")[0].rstrip(" ").lstrip("")
            if j == _N:
                trigger = 1
        if trigger == 0:
            H[j] = "N"

    for i in loc_rule:
        _N = i.split("->")[0].rstrip(" ").lstrip("")
        for j in i.split("->")[1].lstrip(" ").rstrip(" ").split(" "):
            if j == "e":
                H[_N] = "Y"
                D1.add(i)

    for k in D1:
        if k in loc_rule:
            loc_rule.remove(k)

    while True:
        tmp, loc_rule = f(_htable=H, _rules=loc_rule)
        if tmp == H:
            H = tmp
            if len(loc_rule) == 0:
                break
        else:
            H = tmp
    return H


def ll_verifier2(_guides: Dict, _rules: Dict) -> Text:
    nonterminal_by_num = {}
    for _rule in _rules:
        for _item in _rules[_rule]:
            if _rules[_rule][_item][0] == "LEFT":
                if nonterminal_by_num.get(_rules[_rule][_item][1]) is None:
                    nonterminal_by_num[_rules[_rule][_item][1]] = {_item}
                else:
                    nonterminal_by_num[_rules[_rule][_item][1]].add(_item)
    for _letter in nonterminal_by_num:
        if len(nonterminal_by_num[_letter]) >= 2:
            for _guide in nonterminal_by_num[_letter]:
                for q in nonterminal_by_num[_letter]:
                    if _guide != q:
                        if _guides.get(q) and _guides.get(_guide):
                            for v in _guides[_guide]:
                                if v in _guides[q]:
                                    return "Грамматика не является LL(1), " \
                                           "так как направляющие множества " \
                                           f"для {_guide} пересекаются"
                                else:
                                    pass
        else:
            pass
    return "Ok"


def findfirst(nonterminal: Text, nextrule: List, lf=None, idx=None) -> Set:
    if lf is None:
        lf = set()
    local_nt = nonterminal
    for i in range(0, len(nextrule)):
        local_rule = nextrule[i].lstrip(" ").rstrip(" ").split("->")
        if len(local_rule) == 2:
            if local_rule[0].rstrip("usd ").rstrip(" ") == local_nt.rstrip(" "):
                if local_rule[1].lstrip(" ").rstrip(" ").split(" ")[0] \
                        not in NT:
                    for j in N.keys():
                        for m in N[j].keys():
                            if N[j][m][0] == "LEFT":
                                if N[j][m][1] == local_nt.rstrip(" "):
                                    for z in lf[m]:
                                        lf[idx].add(z)
                elif local_rule[1].lstrip(" ").rstrip(" ").split(" ")[0] in NT:
                    for j in N.keys():
                        for m in N[j].keys():
                            if j == i + 1:
                                if N[j][m][0] == "LEFT":
                                    if N[j][m][1] == local_rule[0].rstrip(
                                            "usd ").rstrip(" "):
                                        if len(lf[m]) == 0:
                                            return lf
                                        elif len(lf[m]) > 0:
                                            for z in lf[m]:
                                                lf[idx].add(z)
    return lf


def findfirst2(f: Dict) -> Dict:
    loc_first = f
    for i in range(0, len(P)):
        loc_rule = P[i].lstrip(" ").rstrip(" ").split("->")
        if len(loc_rule) == 2:
            symbol = loc_rule[1].lstrip(" ").rstrip(" ").split(" ")[0]
            if symbol in NT:
                if i + 1 < len(P):
                    for k in N[i + 1].keys():
                        if N[i + 1][k][0] == "LEFT":
                            if N[i + 1][k][1] == loc_rule[0].rstrip(
                                    "usd ").rstrip(" "):
                                loc_resp = findfirst(nonterminal=symbol,
                                                     nextrule=P,
                                                     lf=deepcopy(loc_first),
                                                     idx=k)
                                loc_first = loc_resp
            elif symbol not in NT:
                for j in N.keys():
                    for items in N[j]:
                        if j == i + 1:
                            if N[j][items][0] == "LEFT":
                                if N[j][items][1] == loc_rule[0].rstrip(
                                        "usd ").rstrip(" "):
                                    loc_first[items].add(symbol.rstrip(" "))
    return loc_first


def findfollow(follow: Dict) -> Dict:
    loc_follow = follow
    for j in range(0, len(P)):
        rule = P[j].lstrip(" ").rstrip(" ").split("->")
        if len(rule) == 2:
            _tmp = rule[1].lstrip(" ").rstrip(" ").split(" ")
            for i in range(0, len(_tmp)):
                if _tmp[i].rstrip(" ") in NT:
                    if i + 1 < len(_tmp):
                        alpha = "e"
                        A = _tmp[i].rstrip(" ")
                        beta = _tmp[i + 1].rstrip(" ")

                        if beta in NT:
                            Sb = copy(first_by_nonterminal[beta])
                            if "e" in Sb:
                                Sb.remove("e")

                            if beta == "e" or "e" in first_by_nonterminal[beta]:
                                Fb = loc_follow[rule[0].rstrip("usd ")]
                            elif beta != "e" and "e" \
                                    not in first_by_nonterminal[beta]:
                                Fb = []

                            pre_result = loc_follow[A].union(Sb).union(Fb)
                            loc_follow[A] = pre_result

                        elif beta not in NT:
                            if beta == "e":
                                Fb = loc_follow[rule[0].rstrip("usd ")]
                            elif beta != "e":
                                Fb = []

                            pre_result = loc_follow[A].union((beta,)).union(Fb)
                            loc_follow[A] = pre_result

                    elif i + 1 == len(_tmp):
                        alpha = _tmp[i - 1].rstrip(" ")
                        A = _tmp[i].rstrip(" ")
                        beta = "e"

                        if beta == "e":
                            Fb = loc_follow[rule[0].rstrip("usd ")]
                        elif beta != "e":
                            Fb = []

                        pre_result = loc_follow[A].union(Fb)
                        loc_follow[A] = pre_result
    return loc_follow


def llchain(table: Dict, stack: List, item: str, idx: int) -> Text or List:
    if item in table[idx]["terminals"]:
        if table[idx]["accept"] == "true":
            return "accept"
        elif table[idx]["stack"] == "true":
            stack.append(idx)
            return ["stack", stack]
        elif table[idx]["return"] == "true":
            return ["return", stack]
        elif int(table[idx]["jump"]) != 0:
            return ["jump", int(table[idx]["jump"])]
    elif table[idx]["error"] == "false":
        return ["error", idx]
    else:
        return item


# передать элемент целиком, не букву!
def llchain2(_table: Dict, _stack: List, _item: Text, _index_item: int = 0,
             _number_str_table: int = 1):
    _k = _index_item
    _i = _number_str_table
    _tmp = ""
    _accept_ = tuple()
    _stack_ = tuple()
    _return_ = tuple()
    _jump_ = tuple()
    _terminals_ = len(_table[_i]["terminals"])
    for _idx, _val in enumerate(_table[_i]["terminals"]):
        # _index_item - always 0
        if _item == _val:
            if _item[_index_item] == _val[_index_item]:
                if _table[_i]["accept"] == "true":
                    for x in range(0, len(_item)):
                        _tmp += _item[x]
                    if _tmp != _val and len(_table[_i]["terminals"]) == _idx:
                        return f"Элемент цепочки {_item} не совпадает с " \
                               f"ожидаемым элементом {_val}"
                    _accept_ = "accept", _stack, _tmp
                if _table[_i]["stack"] == "true":
                    _stack.append(_i)
                    _stack_ = "stack", _stack, _i
                if _table[_i]["return"] == "true":
                    _i = _stack.pop()
                    if _i != 0:
                        _i += 1
                        _return_ = "return", _stack, _i
                    else:
                        _return_ = "return", _stack, _i
                if _i != 0:
                    if _table[_i]["jump"] != 0:
                        _i = table[_i]["jump"]
                        _jump_ = "jump", _stack, _i
                return [_accept_, _stack_, _return_, _jump_]
            elif _table[_i]["error"] == "false":
                return ["error", _stack, _i + 1]
            else:
                if len(_stack) == 0 and _item == "HALT":
                    return "HALT"
        elif _idx + 1 == _terminals_:
            if _table[_i]["error"] == "false":
                return ["error", _stack, _i + 1]
    return f"Элемент цепочки {_item} не совпадает с ожидаемым(и) " \
           f"элементом/элементами"


# получает элемент, и номер строки в таблице разбора
# возврат из функции происходит только в случае, если в таблице разбора
# при проходе по цепочке обнаружен accept: true
def llchain3(x: Text, n: int, _table: Dict, _stack: List, _itern: int) -> List:
    _accept_ = False
    while True:
        _itern += 1
        print(f"Итерация {_itern}, Стек: {_stack}, Номер строки: {n}, "
              f"Элемент: {x}")
        time.sleep(0.4)
        r2 = llchain2(_table=_table, _stack=_stack, _item=x, _index_item=0,
                      _number_str_table=n)
        time.sleep(0.1)
        if "Элемент цепочки " in r2:
            raise ValueError(r2 + f" {_table[n]['terminals']}")
        if r2 != "HALT":
            if r2[0] != "error":
                if len(r2[0]) != 0:
                    if r2[0][0] == "accept":
                        _stack = r2[0][1]
                        _lexema_ = r2[0][2]
                        if _lexema_ == x:
                            _accept_ = True
                if len(r2[1]) != 0:
                    if r2[1][0] == "stack":
                        _stack = r2[1][1]
                        n = r2[1][2]
                if len(r2[3]) != 0:
                    if r2[3][0] == "jump":
                        _stack = r2[3][1]
                        n = r2[3][2]
                if len(r2[2]) != 0:
                    if r2[2][0] == "return":
                        _stack = r2[2][1]
                        n = r2[2][2]
                if _accept_:
                    return [n, _stack, _itern]
            else:
                _stack = r2[1]
                n = r2[2]
        else:
            print("HALT")
            break


if __name__ == '__main__':
    # Множества терминалов, не терминалов, правила
    T: Dict[Text, Text] = {}
    N: Dict[int, Dict[Text, List]] = {}
    NT: Set[Text] = set()
    P: List[Text] = []

    # Множества предшествующих, последующих и направляющих символов
    first: Dict[Text, Set[Text]] = {}
    first_by_nonterminal: Dict[Text, List[Text]] = {}
    follow: Dict[Text, Set[Text]] = {}
    guide: Dict[Text, Set[Text]] = {}

    # Вспомогательные множества
    Ml: Set[int] = set()
    Mr: Set[int] = set()

    resp = ll_verifier()
    stop = False
    for i in resp:
        if "U" == i:
            print("Грамматика не является LL(1)")
            stop = True
        else:
            pass
    if stop is False:
        with open(filename, "r", encoding="utf-8") as f:
            while True:
                chunk = f.readline()
                if chunk == "":
                    break
                elif chunk != "":
                    P.append(chunk.strip("\n"))

        for j in P:
            rule = j.lstrip(" ").rstrip(" ").split("->")
            if len(rule) == 2:
                NT.add(rule[0].rstrip(" "))

        number = 1
        for i in range(0, len(P)):
            rule = P[i].lstrip(" ").rstrip(" ").split("->")
            if len(rule) == 2:
                if "usd" not in rule[0].rstrip(" "):
                    N[i + 1] = {f"{number}": ["LEFT", rule[0].rstrip(" ")]}
                    number += 1

                for alt in range(i + 1, len(P)):
                    if rule[0] == P[alt].lstrip(" ").rstrip(" ").split("->")[0]:
                        # rewrite fix
                        if N.get(alt + 1) is None:
                            N[alt + 1] = {
                                f"{number}": ["LEFT", rule[0].rstrip(" ")]
                            }
                        P[alt] = rule[0].rstrip(" ") + "usd" + " -> " + str(
                            P[alt].lstrip(" ").rstrip(" ").split("->")[1])
                        number += 1

                for j in rule[1].lstrip(" ").rstrip(" ").split(" "):
                    if j not in NT:
                        T[str(number)] = j.rstrip(" ")
                        N[i + 1][f"{number}"] = ["RIGHT", j.rstrip(" ")]
                        number += 1
                    elif j in NT:
                        N[i + 1][f"{number}"] = ["RIGHT", j.rstrip(" ")]
                        number += 1

        for k in N.keys():
            for j in N[k].keys():
                if N[k][j][0] == "LEFT":
                    first[j] = set()

        while True:
            trigger = False
            before_first = deepcopy(first)
            first = findfirst2(first)
            for i in first.keys():
                if len(first[i]) != len(before_first[i]):
                    trigger += True
            if trigger is False:
                break

        for i in NT:
            for j in N.keys():
                for m in N[j].keys():
                    if N[j][m][0] == "LEFT":
                        if N[j][m][1] == i:
                            for k in first[m]:
                                if first_by_nonterminal.get(i) is None:
                                    first_by_nonterminal[i] = []
                                    first_by_nonterminal[i].append(k)
                                elif first_by_nonterminal.get(i) is not None:
                                    first_by_nonterminal[i].append(k)

        for k in N.keys():
            for j in N[k].keys():
                if N[k][j][0] == "LEFT":
                    if follow.get(str(N[k][j][1])) is None:
                        if k == 1:
                            follow[N[k][j][1]] = set()
                            follow[N[k][j][1]].add("HALT")
                        elif k != 1:
                            follow[N[k][j][1]] = set()

        while True:
            trigger = False
            before_follow = deepcopy(follow)
            follow = findfollow(follow)
            for i in follow.keys():
                if len(follow[i]) != len(before_follow[i]):
                    trigger += True

            if trigger is False:
                break

        for i in first:
            for j in N.keys():
                for k in N[j].keys():
                    if N[j][k][0] == "LEFT":
                        if k == i:
                            if "e" in first[i]:
                                Sa = copy(first[i])
                                Sa.remove("e")
                                guide[i] = follow[N[j][k][1]].union(Sa)
                            elif "e" not in first[i]:
                                Sa = copy(first[i])
                                guide[i] = Sa

        resp = ll_verifier2(guide, N)
        if resp != "Ok":
            print(resp)
        else:
            for i in first.keys():
                Ml.add(int(i))

            for i in N.keys():
                biggest: int = -1
                for j in N[i].keys():
                    if N[i][j][0] == "RIGHT":
                        if int(j) > int(biggest):
                            biggest = int(j)
                Mr.add(biggest)

            table: Dict[int, Dict[Text, Text or Set[str]]] = dict()
            for i in T:
                if table.get(int(i)) is None:
                    table[int(i)] = {"X": T[i], "terminals": None, "jump": None,
                                     "accept": None, "stack": None,
                                     "return": None, "error": None}
            for i in N:
                for j in N[i]:
                    if table.get(int(j)) is None:
                        table[int(j)] = {"X": N[i][j][1], "terminals": None,
                                         "jump": None, "accept": None,
                                         "stack": None, "return": None,
                                         "error": None}
            for i in guide:
                table[int(i)]["terminals"] = deepcopy(guide[i])

            # добавил в таблицу терминалы
            for i in N:
                for _idx_, j in enumerate(N[i]):
                    if int(j) not in Ml and j not in T:
                        if table[int(j)]["terminals"] is None:
                            _tmp = set()
                            _lst = []
                            _delta_l = []
                            _delta = {}
                            _A = N[i][j][1]
                            if _idx_ + 1 < len(N[i]):
                                for x in N[i]:
                                    if x >= j:
                                        if N[i][x][0] != "LEFT":
                                            _lst.append(x)
                                _n = len(_lst) - 1
                                for _x, _val in enumerate(_lst):
                                    if _val not in T:
                                        if "e" not in first_by_nonterminal[
                                                N[i][_val][1]]:
                                            _k = _x
                                            _delta_l.append(False)
                                            break
                                        else:
                                            _k = _n
                                            _delta_l.append(True)
                                    elif _val in T:
                                        if "e" not in T[_val]:
                                            _k = _x
                                            _delta_l.append(False)
                                            break
                                        else:
                                            _k = _n
                                            _delta_l.append(True)

                                _delta = {"e"}
                                for _x in _delta_l:
                                    if _x is False:
                                        _delta = {}

                                for _x, _val in enumerate(_lst):
                                    if _val in T:
                                        _tmp = _tmp.union({T[_val]}).union(
                                            first_by_nonterminal[_A])
                                    elif _val not in T:
                                        _tmp = _tmp.union(
                                            first_by_nonterminal[N[i][_val][1]]
                                        ).union(first_by_nonterminal[_A])
                                    if _x == _k:
                                        break
                            else:
                                _tmp = _tmp.union(first_by_nonterminal[_A])
                                if "e" in first_by_nonterminal[_A]:
                                    _delta = {"e"}

                            for z in N[i]:
                                if N[i][z][0] == "LEFT":
                                    _B = N[i][z][1]

                            if "e" in _tmp:
                                if "e" in _delta:
                                    _tmp = _tmp.union(follow[_B])
                                _tmp.remove("e")
                            if len(_tmp) != 0:
                                table[int(j)]["terminals"] = _tmp

            for i in T:
                if T[i] != "e":
                    if table[int(i)]["terminals"] is None:
                        table[int(i)]["terminals"] = {T[i]}
                elif T[i] == "e":
                    for j in N:
                        for k in N[j]:
                            if k == i:
                                for z in N[j]:
                                    if N[j][z][0] == "LEFT":
                                        if table[int(i)]["terminals"] is None:
                                            table[int(i)]["terminals"] = follow[
                                                N[j][z][1]]

            # добавил jump
            for i in Ml:
                for j in N:
                    for k in N[j]:
                        if N[j][k][0] == "LEFT":
                            if int(k) == i:
                                if table[int(i)]["jump"] is None:
                                    table[int(i)]["jump"] = \
                                        sorted([int(z)
                                                for z in N[j].keys()])[1]

            for i in N:
                for j in N[i]:
                    if N[i][j][0] == "RIGHT":
                        if j not in T:
                            for k in N:
                                for z in N[k]:
                                    if N[i][j][1] == N[k][z][1] and N[k][z][0] \
                                            == "LEFT":
                                        if table[int(j)]["jump"] is None:
                                            table[int(j)]["jump"] = int(z)

            for i in T:
                if int(i) not in Mr:
                    for k in N:
                        for j in N[k]:
                            if j == i:
                                idx = sorted(N[k].keys()).index(i)
                                # bugfix
                                # bugfix 2// 19.11.21
                                if idx < len(sorted(N[k].keys())) - 1:
                                    if table[int(i)]["jump"] is None:
                                        table[int(i)]["jump"] = int(
                                            sorted(N[k].keys())[idx + 1])

            for i in table.keys():
                if table[int(i)]["jump"] is None:
                    table[int(i)]["jump"] = 0

            # добавил accept
            for i in T:
                if T[i] != "e":
                    if table[int(i)]["accept"] is None:
                        table[int(i)]["accept"] = "true"

            for i in table.keys():
                if table[int(i)]["accept"] is None:
                    table[int(i)]["accept"] = "false"

            # добавил stack
            for i in N:
                for j in N[i]:
                    if N[i][j][0] == "RIGHT" and int(
                            j) not in Mr and j not in T:
                        if table[int(j)]["stack"] is None:
                            table[int(j)]["stack"] = "true"

            for i in table.keys():
                if table[int(i)]["stack"] is None:
                    table[int(i)]["stack"] = "false"

            # добавил return
            for i in T.keys():
                if T[i] == "e" and int(i) in Mr or T[i] != "e" and int(i) in Mr:
                    if table[int(i)]["return"] is None:
                        table[int(i)]["return"] = "true"

            for i in table.keys():
                if table[int(i)]["return"] is None:
                    table[int(i)]["return"] = "false"

            # добавил error
            for i, v in enumerate(Ml):
                if i + 1 <= len(Ml):
                    if int(v) + 1 in list(Ml):
                        if table[v]["error"] is None:
                            table[v]["error"] = "false"
                    else:
                        pass

            for i in table.keys():
                if table[int(i)]["error"] is None:
                    table[int(i)]["error"] = "true"
            print(f"Множество нетерминалов -> {NT}")
            print(f"Множество терминалов (с номерами элементов) -> {T}")
            print(f"Множество правил (без маркировки) -> {P}")
            print("=======")
            print("Грамматика: число на верхнем уровне, обозначет номер "
                  "правила, внутри маркировка правил и элементов грамматики, "
                  "согласно алгоритмам из учебного пособия")
            print(f"Грамматика (с маркировкой правил и элементов, json формат)"
                  f" -> {N}")
            print("=======")
            print(f"Вспомогательные множества Ml -> {Ml} и Mr -> {Mr} ")
            print("======= Таблица разбора, полученная из грамматики: =======")
            for i in sorted(table.keys()):
                print(i, table[i])
            print("======= Таблица разбора, полученная из грамматики: =======\n"
                  )

            # парсер структуры
            inChain = dict()
            types = ["int", "string", "float"]
            keywords = ["struct", "long", "short", "signed", "unsigned",
                        "double", "int", "typedef", "float"]
            reserved_ids = {"struct", "long", "short", "signed", "unsigned",
                            "double", "int", "typedef", "float", "[probel]",
                            "{", "}", ",", ";", "[", "]", " "}
            variables: Set[Text] = set()
            nested_lvl = 1
            nested_vars: Dict[Text, List[Tuple]] = {f"{nested_lvl}": []}
            stack = [0]
            itern = 0
            lexema = ""
            start_string = 1
            string_number = 1
            term = False
            with open("struct.txt") as f:
                inFile = f.read()
            strings = inFile.split("\n")
            print(first_by_nonterminal)
            for idxj, j in enumerate(inFile.rstrip(" ").rstrip("\n").rstrip("\r"
                                                                            )):
                current_terminals = table[start_string]['terminals']
                write = False
                nstdp_trig = False
                nstdm_trig = False
                if j == "\n" or j == "\r":
                    string_number += 1
                for i, v in enumerate(current_terminals):
                    if re.match(r"(\w|\d|_)", j):
                        write = True
                    elif re.match(r"(\s|\[|\]|;|,|\{|\})", j):
                        _reset = False
                        for _idx_, z in enumerate(current_terminals):
                            # keyword verifier
                            if lexema == z:
                                _resp_ = llchain3(str(lexema), start_string,
                                                  table, stack, itern)
                                stack = _resp_[1]
                                itern = _resp_[2]
                                start_string = _resp_[0]
                                _reset = True
                                variables.add(lexema)
                                break
                            elif ("[_a-zA-Z]" in current_terminals or
                                  "[0-9]" in current_terminals) and \
                                    _idx_ + 1 == len(current_terminals):
                                if len(lexema) > 0:
                                    if lexema in keywords:
                                        msg = "Ключевое слово не может " \
                                              "быть именем переменной, " \
                                              "позиция в файле - " \
                                              f"{inFile.find(lexema)}, " \
                                              f"строка {string_number}"
                                        raise ValueError(msg)
                                    for _idx, s in enumerate(lexema):
                                        if _idx == 0 and re.match(r"\d", s):
                                            msg = "Переменная должна начинат" \
                                                  "ься с буквы или нижнего " \
                                                  f"подчеркивания - " \
                                                  f"{lexema}, позиция " \
                                                  f"в файле - " \
                                                  f"{inFile.find(lexema)}," \
                                                  f" строка {string_number}"
                                            if "[" not in variables:
                                                raise ValueError(msg)
                                        # debug
                                        # print(s, "letter")
                                        if re.match(r"\d", s):
                                            s = "[0-9]"
                                        elif re.match(r"(\w|_)", s):
                                            s = "[_a-zA-Z]"
                                        _resp_ = llchain3(s, start_string,
                                                          table, stack, itern)
                                        stack = _resp_[1]
                                        itern = _resp_[2]
                                        start_string = _resp_[0]
                                        _reset = True
                                    variables.add(lexema)
                                    if nested_vars.get(str(nested_lvl)):
                                        if "struct" in variables:
                                            for x in nested_vars[
                                                    str(nested_lvl)]:
                                                if x[1] == "struct":
                                                    if x[0] == lexema:
                                                        _posinfile = inFile. \
                                                            find(lexema)
                                                        msg = f"Повторное " \
                                                              f"использование "\
                                                              f"имени - " \
                                                              f"{x[0]}, " \
                                                              f"позиция в " \
                                                              f"файле - " \
                                                              f"{_posinfile}," \
                                                              f" строка - " \
                                                              f"{string_number}"
                                                        # debug
                                                        raise NameError(msg, nested_vars)
                                            nested_vars[str(nested_lvl)].append(
                                                (lexema, "struct"))
                                        elif "struct" not in variables:
                                            for x in nested_vars[
                                                    str(nested_lvl)]:
                                                if x[1] == "var":
                                                    if x[0] == lexema:
                                                        _posinfile = inFile.\
                                                            find(lexema)
                                                        msg = f"Повторное " \
                                                              f"использование "\
                                                              f"имени - " \
                                                              f"{x[0]}, " \
                                                              f"позиция в " \
                                                              f"файле - " \
                                                              f"{_posinfile}," \
                                                              f" строка - " \
                                                              f"{string_number}"
                                                        #debug
                                                        raise NameError(msg, nested_vars)
                                            nested_vars[str(nested_lvl)].append(
                                                (lexema, "var"))
                                    else:
                                        if "struct" in variables:
                                            _diff = variables.difference(
                                                reserved_ids)
                                            if len(_diff) == 1:
                                                nested_vars[
                                                    str(nested_lvl)
                                                ] = [(next(iter(_diff)),
                                                       "struct")]
                                        else:
                                            _diff = variables.difference(
                                                reserved_ids)
                                            if len(_diff) == 1:
                                                nested_vars[
                                                    str(nested_lvl)
                                                ] = [(next(iter(_diff)), "var")]
                            else:
                                pass
                        if len(lexema) > 0 and _reset is False:
                            msg = f"Ошибка лексема {lexema} не допустима " \
                                  f"в текущей строке {current_terminals}, " \
                                  f"позиция в файле - {inFile.find(lexema)}, " \
                                  f"строка - {string_number}"
                            raise ValueError(msg)

                        if j == " " or j == "\n" or j == "\r":
                            j = "[probel]"

                        resp = llchain3(j, start_string, table,
                                        stack, itern)
                        stack = resp[1]
                        itern = resp[2]
                        start_string = resp[0]
                        variables.add(j)
                        lexema = ""
                        if j == "{":
                            _diff = variables.difference(reserved_ids)
                            if len(_diff) == 1:
                                nstdp_trig = True
                        if j == "}":
                            nstdm_trig = True
                        break
                    else:
                        print("Unexpected scenario")
                if ";" in variables and j == ";":
                    print(variables, nested_vars)
                    variables.clear()
                elif nstdp_trig:
                    nested_lvl += 1
                    variables.clear()
                elif nstdm_trig:
                    nested_lvl -= 1
                    variables.clear()
                if write:
                    lexema += j
                if len(stack) == 1 and stack[0] == 0 and idxj + 1 == len(
                        inFile):
                    print("STOP", stack)
                    break
