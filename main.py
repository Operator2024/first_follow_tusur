from copy import copy, deepcopy
from typing import Text, List, Dict


def findfirst(nonterminal: Text, nextrule: List, lf=None):
    if lf is None:
        lf = set()
    local_nt = nonterminal

    for i in range(0, len(nextrule)):
        local_rule = nextrule[i].lstrip(" ").rstrip(" ").split("->")
        if len(local_rule) == 2:
            if local_rule[0].rstrip("usd ").rstrip(" ") == local_nt.rstrip(" "):
                if local_rule[1].lstrip(" ").rstrip(" ").split(" ")[0] not in NT:
                    for k in N.keys():
                        if N[k][0] == "LEFT":
                            if N[k][1] == local_rule[0].rstrip("usd ").rstrip(" "):
                                if len(lf[k]) == 0:
                                    lf[k].add(local_rule[1].lstrip(" ").rstrip(" ").split(" ")[0].rstrip(" "))
                                    return lf, k
                                elif len(lf[k]) != 0:
                                    return lf, k
                elif local_rule[1].lstrip(" ").rstrip(" ").split(" ")[0] in NT:
                    if i + 1 <= len(nextrule):
                        resp, id = findfirst(nonterminal=local_rule[1].lstrip(" ").rstrip(" ").split(" ")[0],
                                         nextrule=nextrule[i + 1::], lf=lf)
                        return resp, id



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
                            Sb = copy(first[beta])
                            if "e" in Sb:
                                Sb.remove("e")

                            if beta == "e" or "e" in first[beta]:
                                Fb = loc_follow[rule[0].rstrip("usd ")]
                            elif beta != "e" and "e" not in first[beta]:
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
                N[i+1] = {f"{number}":  ["LEFT", rule[0].rstrip(" ")]}
                number += 1

                #{"1":{"1": ["LEFT", "E"], "2": []}}

            for alt in range(i + 1, len(P)):
                if rule[0] == P[alt].lstrip(" ").rstrip(" ").split("->")[0]:
                    N[alt + 1] = {f"{number}":  ["LEFT", rule[0].rstrip(" ")]}
                    P[alt] = rule[0].rstrip(" ") + "usd" + " -> " + str(P[alt].lstrip(" ").rstrip(" ").split("->")[1])
                    number += 1

            for j in rule[1].lstrip(" ").rstrip(" ").split(" "):
                if j not in NT:
                    T[str(number)] = j.rstrip(" ")
                    N[i+1][f"{number}"] = ["RIGHT", j.rstrip(" ")]
                    number += 1
                elif j in NT:
                    N[i+1][f"{number}"] = ["RIGHT", j.rstrip(" ")]
                    number += 1

    first = {}
    # for k in N.keys():
    #     if N[k][0] == "LEFT":
    #         first[k] = set()

    # for i in range(0, len(P)):
    #     rule = P[i].lstrip(" ").rstrip(" ").split("->")
    #     if len(rule) == 2:
    #         symbol = rule[1].lstrip(" ").rstrip(" ").split(" ")[0]
    #         if symbol in NT:
    #             if i + 1 < len(P):
    #                 resp, fid = findfirst(nonterminal=symbol, nextrule=P[i + 1::], lf=deepcopy(first))
    #                 for k in N.keys():
    #                     if N[k][0] == "LEFT":
    #                         if N[k][1] == rule[0].rstrip("usd ").rstrip(" "):
    #                             if len(resp[k]) == 0:
    #                                 for e in resp[fid]:
    #                                     print(resp, "test")
    #                                     resp[k].add(e)
    #                                 first = resp
    #                 print(resp, "test2")
    #         elif symbol not in NT:
    #
    #             for k in N.keys():
    #                 if N[k][0] == "LEFT":
    #                     if N[k][1] == rule[0].rstrip("usd ").rstrip(" "):
    #                         if len(first[k]) == 0:
    #                             print(symbol, rule, k, first)
    #                             first[k].add(symbol.rstrip(" "))
    #                             break


    # for i in range(0, len(P)):
    #     rule = P[i].lstrip(" ").rstrip(" ").split("->")
    #     if len(rule) == 2:
    #         symbol = rule[1].lstrip(" ").rstrip(" ").split(" ")[0]
    #         if symbol in NT:
    #             if i + 1 < len(P):
    #                 resp = findfirst(nonterminal=symbol, nextrule=P[i + 1::])
    #                 first[rule[0].rstrip("usd ")] = [x for x in resp]
    #         elif symbol not in NT:
    #             if first.get(rule[0].rstrip("usd ")) is None:
    #                 first[rule[0].rstrip("usd ")] = [symbol.lstrip(" ").rstrip(" ")]
    #             elif first.get(rule[0].rstrip("usd ")):
    #                 first[rule[0].rstrip("usd ")].append(symbol.lstrip(" ").rstrip(" "))


    # follow = {}
    # for k in first.keys():
    #     if N[str(1)] == k:
    #         follow[k] = set()
    #         follow[k].add("halt")
    #     else:
    #         follow[k] = set()
    #
    # while True:
    #     trigger = False
    #     before_follow = deepcopy(follow)
    #     follow = findfollow(follow)
    #     for i in follow.keys():
    #         if len(follow[i]) != len(before_follow[i]):
    #             trigger += True
    #
    #     if trigger is False:
    #         break
    #
    # guide = {}
    # for i in NT:
    #     if "e" in first[i]:
    #         Sa = copy(first[i])
    #         Sa.remove("e")
    #         guide[i] = follow[i].union(Sa)
    #     elif "e" not in first[i]:
    #         Sa = copy(first[i])
    #         guide[i] = Sa


    print(T, " - Terminals")
    print(NT, " - Non terminals 1")
    print(N, " - Non terminals")
    print(P)
    # print(first)
    # print(follow)
    # print(guide, "guide")
