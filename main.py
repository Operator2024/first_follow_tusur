from copy import copy, deepcopy
from typing import Text, List, Dict, Set


def findfirst(nonterminal: Text, nextrule: List, lf=None, idx=None):
    if lf is None:
        lf = set()
    local_nt = nonterminal

    for i in range(0, len(nextrule)):
        local_rule = nextrule[i].lstrip(" ").rstrip(" ").split("->")
        if len(local_rule) == 2:
            if local_rule[0].rstrip("usd ").rstrip(" ") == local_nt.rstrip(" "):
                if local_rule[1].lstrip(" ").rstrip(" ").split(" ")[0] not in NT:
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
                                    if N[j][m][1] == local_rule[0].rstrip("usd ").rstrip(" "):
                                        if len(lf[m]) == 0:
                                            return lf
                                        elif len(lf[m]) > 0:
                                            for z in lf[m]:
                                                lf[idx].add(z)
    return lf


def findfirst2(f):
    first = f
    for i in range(0, len(P)):
        rule = P[i].lstrip(" ").rstrip(" ").split("->")
        if len(rule) == 2:
            symbol = rule[1].lstrip(" ").rstrip(" ").split(" ")[0]
            if symbol in NT:
                if i + 1 < len(P):
                    for k in N[i + 1].keys():
                        if N[i + 1][k][0] == "LEFT":
                            if N[i + 1][k][1] == rule[0].rstrip("usd ").rstrip(" "):
                                resp = findfirst(nonterminal=symbol, nextrule=P, lf=deepcopy(first),
                                                 idx=k)
                                first = resp
            elif symbol not in NT:
                for j in N.keys():
                    for items in N[j]:
                        if j == i + 1:
                            if N[j][items][0] == "LEFT":
                                if N[j][items][1] == rule[0].rstrip("usd ").rstrip(" "):
                                    first[items].add(symbol.rstrip(" "))
    return first


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
                            elif beta != "e" and "e" not in first_by_nonterminal[beta]:
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


if __name__ == '__main__':
    T = {}
    N = {}
    NT = set()
    P = list()

    with open("input.txt", "r", encoding="utf-8") as f:
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
                    N[alt + 1] = {f"{number}": ["LEFT", rule[0].rstrip(" ")]}
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

    first = {}
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

    first_by_nonterminal = {}
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

    follow = {}
    for k in N.keys():
        for j in N[k].keys():
            if N[k][j][0] == "LEFT":
                if follow.get(str(N[k][j][1])) is None:
                    if k == 1:
                        follow[N[k][j][1]] = set()
                        follow[N[k][j][1]].add("halt")
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

    guide = {}
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

    Ml = set()
    Mr = set()

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
            table[int(i)] = {"X": T[i], "terminals": None, "jump": None, "accept": None, "stack":
                None,
                             "return": None, "error": None}

    for i in N:
        for j in N[i]:
            if table.get(int(j)) is None:
                table[int(j)] = {"X": N[i][j][1], "terminals": None, "jump": None, "accept": None,
                                 "stack": None, "return": None, "error": None}

    for i in guide:
        table[int(i)]["terminals"] = deepcopy(guide[i])

    # добавил в таблицу терминалы
    for i in N:
        for j in N[i]:
            if int(j) not in Ml and j not in T:
                # print(N[i][j][1], f" - Number - {j}")

                if table[int(j)]["terminals"] is None:
                    _tmp = set()
                    if "e" in first_by_nonterminal[N[i][j][1]]:
                        for z in first_by_nonterminal[N[i][j][1]]:
                            if z != "e":
                                _tmp.add(z)
                            for x in N[i]:
                                if N[i][x][0] == "LEFT":
                                    table[int(j)]["terminals"]: Set = _tmp.union(follow[N[i][x][1]])
                    elif "e" not in first_by_nonterminal[N[i][j][1]]:
                        for z in first_by_nonterminal[N[i][j][1]]:
                            _tmp.add(z)
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
                                    table[int(i)]["terminals"] = follow[N[j][z][1]]

    # добавил jump
    for i in Ml:
        for j in N:
            for k in N[j]:
                if N[j][k][0] == "LEFT":
                    if int(k) == i:
                        if table[int(i)]["jump"] is None:
                            table[int(i)]["jump"] = int(sorted(N[j].keys())[1])

    for i in N:
        for j in N[i]:
            if N[i][j][0] == "RIGHT":
                if j not in T:
                    for k in N:
                        for z in N[k]:
                            if N[i][j][1] == N[k][z][1] and N[k][z][0] == "LEFT":
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
                                table[int(i)]["jump"] = int(sorted(N[k].keys())[idx + 1])

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
            if N[i][j][0] == "RIGHT" and int(j) not in Mr and j not in T:
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
    for i in range(1, len(N)):
        if i + 1 <= len(N):
            minimal_curr = min(N[i].keys())
            minimal_next = min(N[i + 1].keys())
            if N[i][minimal_curr][0] == "LEFT" and N[i + 1][minimal_next][0] == "LEFT":
                if N[i][minimal_curr][1] == N[i + 1][minimal_next][1]:
                    if table[int(minimal_curr)]["error"] is None:
                        table[int(minimal_curr)]["error"] = "false"

    for i in table.keys():
        if table[int(i)]["error"] is None:
            table[int(i)]["error"] = "true"
