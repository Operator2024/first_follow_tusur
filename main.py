import re
import time
from copy import copy, deepcopy
from typing import Text, List, Dict, Set, Tuple

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


def ll_verifier() -> Set:
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


def ll_verifier2(_guides: Dict, _rules: List) -> Text:
    nonterminal_by_num = {}
    for _rule in _rules:
        for _item in _rules[_rule]:
            if _rules[_rule][_item][0] == "LEFT":
                if nonterminal_by_num.get(_rules[_rule][_item][1]) is None:
                    nonterminal_by_num[_rules[_rule][_item][1]] = set(_item)
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
                                    print(v, _guides, q)
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
                                                     idx=k
                                                     )
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

                            pre_result = loc_follow[A].union(beta).union(Fb)
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
    for _idx, _val in enumerate(_table[_i]["terminals"]):
        # _index_item - always 0
        if _item == _val or _val == "HALT":
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
        else:
            if _table[_i]["error"] == "false":
                return ["error", _stack, _i + 1]
    return f"Элемент цепочки {_item} не совпадает с ожидаемым элементом"


# получает элемент, и номер строки в таблице разбора
# возврат из функции происходит только в случае, если в таблице разбора
# при проходе по цепочке обнаружен accept: true
def llchain3(x: Text, n: int, _table: Dict, _stack: List, _itern: int) -> List:
    _accept_ = False
    while True:
        _itern += 1
        print(f"Итерация {_itern}, Стек: {_stack}, Номер строки: {n}, "
              f"Элемент: {x}")
        time.sleep(0.5)
        r2 = llchain2(_table=_table, _stack=_stack, _item=x, _index_item=0,
                      _number_str_table=n)
        if "Элемент цепочки " in r2: raise ValueError(r2)
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
    T = {}
    N = {}
    NT = set()
    P = list()

    # Множества предшествующих, последующих и направляющих символов
    first = {}
    first_by_nonterminal = {}
    follow = {}
    guide = {}

    # Вспомогательные множества
    Ml = set()
    Mr = set()

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

                    # {"1":{"1": ["LEFT", "E"], "2": []}}
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

        # bug ll_verifier2
        resp = ll_verifier2(guide, N)
        # resp = "Ok"
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

            table = dict()
            for i in T:
                if table.get(int(i)) is None:
                    table[int(i)] = {"X": T[i], "terminals": None, "jump": None,
                                     "accept": None, "stack": None,
                                     "return": None, "error": None
                                     }

            for i in N:
                for j in N[i]:
                    if table.get(int(j)) is None:
                        table[int(j)] = {"X": N[i][j][1], "terminals": None,
                                         "jump": None, "accept": None,
                                         "stack": None, "return": None,
                                         "error": None
                                         }

            for i in guide:
                table[int(i)]["terminals"] = deepcopy(guide[i])

            # добавил в таблицу терминалы
            for i in N:
                for j in N[i]:
                    if int(j) not in Ml and j not in T:
                        # print(N[i][j][1], f" - Number - {j}")

                        if table[int(j)]["terminals"] is None:
                            _tmp = set()
                            _A = N[i][j][1]
                            _tmp = _tmp.union(first_by_nonterminal[_A])
                            for z in N[i]:
                                if N[i][z][0] == "LEFT":
                                    _B = N[i][z][1]
                            if "e" in _tmp:
                                _tmp = _tmp.union(follow[_B])
                                _tmp.remove("e")
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
                                    # table[int(i)]["jump"] = int(sorted(N[j].keys())[1])
                                    table[int(i)]["jump"] = \
                                        sorted([int(z) for z in N[j].keys()])[1]

            for i in N:
                for j in N[i]:
                    if N[i][j][0] == "RIGHT":
                        if j not in T:
                            for k in N:
                                for z in N[k]:
                                    if N[i][j][1] == N[k][z][1] and N[k][z][
                                        0] == \
                                            "LEFT":
                                        if table[int(j)]["jump"] is None:
                                            table[int(j)]["jump"] = int(z)

            for i in T:
                if int(i) not in Mr:
                    for k in N:
                        for j in N[k]:
                            if j == i:
                                idx = sorted(N[k].keys()).index(i)
                                # bugfix
                                # if len(sorted(N[k].keys())) - 1 < idx:
                                if idx < len(sorted(N[k].keys())):
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
            # for i in range(1, len(N)):
            #     if i + 1 <= len(N):
            #         minimal_curr = min(N[i].keys())
            #         minimal_next = min(N[i + 1].keys())
            #         if N[i][minimal_curr][0] == "LEFT" and \
            #                 N[i + 1][minimal_next][
            #                     0] == "LEFT":
            #             if N[i][minimal_curr][1] == N[i + 1][minimal_next][1]:
            #                 if table[int(minimal_curr)]["error"] is None:
            #                     table[int(minimal_curr)]["error"] = "false"
            for i, v in enumerate(Ml):
                if i + 1 < len(Ml):
                    if list(Ml)[i + 1] - list(Ml)[i] == 1:
                        if table[v]["error"] is None:
                            table[v]["error"] = "false"
                    else:
                        pass

            for i in table.keys():
                if table[int(i)]["error"] is None:
                    table[int(i)]["error"] = "true"

            for i in sorted(table.keys()):
                print(i, table[i])

            test_struct = ["struct", "яяя", ";", "HALT"]
            test_struct = ["struct", "person", "{", "}", ";", "HALT"]
            test_struct = ["struct", "person", ";", "HALT"]
            stack = [0]
            stroka = 1
            itern = 1

            for i, v in enumerate(test_struct):
                if i == 0:
                    r = llchain3(x=v, n=1, _table=table, _stack=stack,
                                 _itern=itern)
                    stack = r[1]
                    itern = r[2]
                else:
                    if r[0] == 0 and v != "HALT":
                        print("Обнаружен переход в нулевую строку")
                    if r[0] == 0 and v == "HALT":
                        print(f"Разбор окончен, стек: {stack}")
                    else:
                        r = llchain3(x=v, n=r[0], _table=table, _stack=stack,
                                     _itern=itern)
                        stack = r[1]
                        itern = r[2]
                # time.sleep(10)
