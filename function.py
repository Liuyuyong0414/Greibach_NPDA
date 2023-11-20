import copy
import json

# V,T,P,S

V = []
T = []
P = {}
S = 'S'
# 转移函数
move = {}


def transform(filename, V, T, P, S):
    with open(filename, "r") as f:
        data = f.read()
    try:
        for line in data.splitlines():
            # 删除多余的空格
            statement = line.replace(" ", "")
            statement = statement.replace("蔚", "ε")
            statement = statement.split("->")
            if statement[0] not in V:
                V.append(statement[0])
                P[statement[0]] = statement[1].replace(" ", "").split("|")
            else:
                # 合并相同左部的产生式
                for item in statement[1].replace(" ", "").split("|"):
                    P[statement[0]].append(item)
    except:
        print("语法存在错误！请修改后保存在input.txt文件中")
        return False
    for (i, j) in P.items():
        for t in j:
            # 利用非终结符分隔终结符
            for v in V:
                t = t.replace(v, " ")
            """
            保存终结符，注意第二个循环
            避免D->dD|dd最后dd未被分隔，导致保存为dd，而不是d
            """
            for ii in t.split(" "):
                for iii in list(ii):
                    if iii not in T:
                        T.append(iii)
    print("*******************")
    print("transformer!")
    print("V: ", V)
    print("T: ", T)
    print("P: ", P)
    print("S: ", S)
    print("*******************")


"""
1.消除ε规则
2.消除单一产生式
3.消除无用符号
4.消除左递归
"""
index = []
for i in range(26):
    index.append(chr(i + 65))


# print(index)


# 消除空产生式
def delete_epsilon():
    def search():
        V0 = []  # 可空符号集
        V1 = []  # 不可空符号集

        # 对于所有产生式A->ε，A是一个可致空符号
        for (p, right) in P.items():  # 对每个符号
            css_num = len(right)
            have_T = 0
            for item in right:  # 对每个符号的每个产生式
                if len(item) == 1 and 'ε' in item and p not in V0:
                    V0.append(p)
                    break
                else:
                    for char in item:
                        if char in T:
                            have_T += 1
                            break
            if have_T == css_num and p not in V0 and p not in V1:  # 判断所有的产生式都含有终结符
                V1.append(p)

        # 如果有产生式B->C1C2...Ck，其中每一个Ci∈V0是可致空符号，则B是一个可致空符号
        def can_be_epsilon(v):  # 判断一个非终结符是否能推出空
            flag1 = 0  # 当前符号是否可空，1为可空
            if v in V0:
                return True
            elif v in V1:
                return False
            else:
                for (p, right) in P.items():
                    if p == v:  # 找到符号对应的产生式
                        flag2 = 0
                        flag3 = 0
                        for item in right:  # 对每个产生式
                            for char in item:  # 对产生式右边的每个符号
                                if char in T or char in V1:  # 如果包含终结符或不可空的非终结符，处理下一个产生式
                                    flag2 = 1
                                    break
                            if flag2 == 1:
                                flag2 = 0
                                continue
                            for char in item:  # 产生式中全是非终结符，且有的能推出空，有的不知道是否能推出空
                                if not can_be_epsilon(char):
                                    flag3 = 1
                                    break
                            if flag3 == 0:
                                flag1 = 1
                                break
                            else:
                                flag3 = 0
                        if flag1 == 1 and p not in V0:
                            V0.append(p)
                            return True
                        elif flag1 == 0 and p not in V1:
                            V1.append(p)
                            return False

        # 先推出可空符号集
        for v in V:
            can_be_epsilon(v)

        print("****可致空集合V0和不可致空集合V1*****")
        print("V0: ", V0)
        print("V1: ", V1)
        if len(V0) == 0 or (len(V0) == 1 and "S" in V0):
            return V0, True

        # 替换可空符号
        copy_P = copy.deepcopy(P)
        for (p, right) in P.items():
            for item in right:
                ans = ""
                for char in item:
                    if char not in V0:
                        ans += char
                if ans != item:
                    if ans == "" and "ε" not in P[p]:
                        P[p].append("ε")
                    elif ans not in P[p]:
                        P[p].append(ans)

        # print("*****替换可空符号********")
        # print(P)
        # print("*************")
        # 删除ε产生式
        copy_P = copy.deepcopy(P)
        FLAG = 0
        for (p, right) in copy_P.items():
            for item in right:
                if len(item) == 0 or item == "ε":
                    if p == "S":
                        FLAG = 1
                        continue
                    P[p].remove(item)
        if not FLAG:
            if 'ε' in T:
                T.remove("ε")

        # print("*****删除ε产生式********")
        # print(P)
        # print("*************")

        # 删除只能推出空的非终结符
        useless_V = []
        copy_P = copy.deepcopy(copy_P)
        for (p, right) in copy_P.items():
            if len(right) == 0:
                useless_V.append(p)
                V.remove(p)
                del P[p]
        # print("*****删除只能推出空的非终结符********")
        # print(P)
        # print("*************")
        copy_P = copy.deepcopy(P)
        for (p, right) in copy_P.items():
            for item in right:
                may_replace_item = [i for i in item if i not in useless_V]
                if len(may_replace_item) != len(item):  # 有无用非终结符
                    if "".join(may_replace_item) not in right and len(may_replace_item) != 0:
                        P[p].append("".join(may_replace_item))
                        P[p].remove(item)
        return [], False

    while 1:
        V0, flag = search()
        if flag:
            break
    print(P)
    print("*******************")
    print("消除空产生式!")
    print("V: ", V)
    print("T: ", T)
    print("P: ", P)
    print("S: ", S)
    print("*******************")


# 消除单一产生式
def delete_single():
    def get_pair():
        pair = []
        for (p, right) in P.items():
            for item in right:
                if item in V:
                    pair.append((p, item))
        return pair

    while 1:
        pair = get_pair()
        if len(pair) == 0:
            break
        print("*******************")
        print("文法存在的单元偶对如下：")
        print(pair)
        print("*******************")
        for (A, B) in pair:
            copy_right = P[A]
            for item in P[B]:
                if item not in copy_right:
                    P[A].append(item)
            P[A].remove(B)
    print("*******************")
    print("消除单一产生式!")
    print("V: ", V)
    print("T: ", T)
    print("P: ", P)
    print("S: ", S)
    print("*******************")


# 消除无用符号
def delete_useless():
    reach = []

    def search(p):
        if p not in reach:
            reach.append(p)
        for item in P[p]:
            for char in item:
                if char in V and char not in reach:
                    search(char)
                elif char in T and char not in reach:
                    reach.append(char)

    search("S")
    print("可达字符集***********")
    print(reach)
    print("不可达*******")
    non_reach = [item for item in (V + T) if item not in reach]
    print(non_reach)
    # copy_V = copy.deepcopy(V)
    # for v in copy_V:
    #     if v not in reach:
    #         V.remove(v)
    #         del P[v]
    for nr in non_reach:
        if nr in V:
            V.remove(nr)
            del P[nr]
        if nr in T:
            T.remove(nr)

    print("*******************")
    print("消除无用符号！")
    print("V: ", V)
    print("T: ", T)
    print("P: ", P)
    print("S: ", S)
    print("*******************")


# 消除直接左递归
def delete_direct_left_recursive():
    new_P = copy.deepcopy(P)
    for (p, right) in new_P.items():
        alpha, beta = [], []
        for item in right:
            if p == item[0]:
                alpha.append(item[1:])
            else:
                beta.append(item)
        if alpha:
            for i in index:
                if i not in V:
                    print("针对符号" + p, "替换字母位： ", i)
                    new_V = i
                    V.append(new_V)
                    break
            P[p] = [b + new_V for b in beta]
            P[new_V] = [a + new_V for a in alpha]
            P[new_V].append("ε")


def delete_left_recursive():
    def search(v, reach):
        # print(v,reach)
        right = P[list(reach)[-1]]
        for item in right:
            if item[0] in V:
                if item[0] == v:
                    return reach, True
                elif item[0] not in reach:
                    str, flag = search(v, reach + item[0])
                    if flag:
                        return str, True
        return "", False

    while 1:
        delete_direct_left_recursive()
        flag = 0
        for v in P.keys():
            # print(v)
            reach = v
            reach, FLAG = search(v, reach)
            if FLAG:
                flag = 1
                break
        if flag == 0:
            break
        else:
            # print(reach)
            p = list(reach)[0]
            for i in list(reach)[1:]:
                alpha = []
                copy_right = P[p]
                for item in P[p]:
                    if item[0] == i:
                        alpha.append(item[1:])
                        copy_right.remove(item)
                for item in P[i]:
                    for alp in alpha:
                        if item + alp not in copy_right:
                            copy_right.append(item + alp)
            P[p] = copy_right
            print("*******************")
            print("间接左递归转换为直接左递归！")
            print("reach: ", reach)
            print("V: ", V)
            print("T: ", T)
            print("P: ", P)
            print("S: ", S)
            print("*******************")
    print("*******************")
    print("最终消除左递归后的产生式!")
    print("V: ", V)
    print("T: ", T)
    print("P: ", P)
    print("S: ", S)
    print("*******************")


def change_to_greibach():
    # 处理以非终结符开头的产生式
    while 1:
        flag = 0
        for (p, right) in P.items():
            copy_right = right.copy()
            for item in right:
                if item[0] in V:
                    copy_right.remove(item)
                    flag = 1
                    for C_item in P[item[0]]:
                        if C_item + item[1:] not in copy_right:
                            copy_right.append(C_item + item[1:])
                    break
            if flag == 1:
                P[p] = copy_right
                break
        if flag == 0:
            break
    print("*******************")
    print("消除首字符为非终结符!")
    print("V: ", V)
    print("T: ", T)
    print("P: ", P)
    print("S: ", S)
    print("*******************")
    # 处理不处于后继的终结符
    new = {}
    copy_P = copy.deepcopy(P)
    for (p, right) in copy_P.items():
        for item in right:
            copy_item = list(item)
            for iii, char in enumerate(item[1:]):
                if char in T and char in new.keys():
                    copy_item[iii + 1] = new[char]
                elif char in T and char not in new.keys():
                    FLAG = 0
                    for (pp, pp_right) in copy_P.items():
                        if len(pp_right) == 1 and char == pp_right[0]:
                            new[char] = pp
                            FLAG = 1
                            break
                    if FLAG == 0:
                        for i in index:
                            if i not in V:
                                print("引入新变量：", i)
                                new[char] = i
                                V.append(i)
                                break
                    copy_item[iii + 1] = new[char]
                    P[new[char]] = [char]
            print(item, copy_item)
            if not copy_item == item:
                P[p].remove(item)
                P[p].append("".join(copy_item))

    print("*******************")
    print("消除非首字符为终结符!")
    print("V: ", V)
    print("T: ", T)
    print("P: ", P)
    print("S: ", S)
    print("*******************")


# 转化为Greibach范式
def toGNF():
    delete_epsilon()
    delete_single()
    delete_useless()
    delete_left_recursive()
    # print(P)
    delete_epsilon()
    delete_single()
    delete_useless()
    change_to_greibach()


def to_npda():
    # 起始状态q0，中间状态q1，结束状态qf
    Q = ["q0", "q1", "qf"]
    # 开始转移函数
    # 结束转移函数
    move[("q0", "", "z")] = [("q1", "Sz")]
    move[("q1", "", "z")] = [("qf", "z")]
    # 如果ε存在于终结符，则必为S->ε
    if "ε" in T:
        move[("q1", "", "S")] = [("qf", "z")]

    for (p, right) in P.items():
        for item in right:
            key = ("q1", item[0], p)
            if key in move.keys():
                move[key].append(("q1", item[1:]))
            else:
                move[key] = [("q1", item[1:])]
    print(move)


def judge():
    def dfs(String, Point, State):
        if Point == -1:
            Str = stack.pop()
            Left = (State, "", Str)
            if Left in move.keys():
                print("*********************")
                print("当前位置： ", point)
                new_state, new_str = move[Left][0]
                for i in reversed(list(new_str)):
                    stack.append(i)
                print("执行转移：", Left, "->", move[Left][0])
                return dfs(String, Point + 1, new_state)
            else:
                print("请添加开始转移函数！")
                return False
        else:
            print("*********************")
            print("当前位置： ", Point)
            print("当前栈为： ", stack)
            Str = stack.pop()
            print("弹出：", Str)
            print("当前栈为：", stack)
            # if point>=len(String)时，当前符号应该为“”
            if Point >= len(String):
                Left = (State, "", Str)
            else:
                Left = (State, String[Point], Str)
            print(Left)
            if Left not in move.keys():
                print("无法找到 ", Left, " 对应的转移函数！")
                stack.append(Str)
                return False
            else:
                for number, item in enumerate(move[Left]):
                    new_state, new_str = item
                    if new_state == "qf":
                        return True
                    # 为空就不需要加入栈中
                    if new_str != "":
                        for i in reversed(list(new_str)):
                            stack.append(i)
                    print("执行转移：", Left, "->", item)

                    print("弹入：", new_str)
                    print("当前栈为：", stack)
                    if dfs(String, Point + 1, new_state):
                        return True
                    else:
                        # 如果当前路径不符合，就回溯，进行退栈
                        print("    ______________")
                        print("    回溯")
                        print("    回溯前，栈为：", stack)
                        if new_str != "":
                            for i in reversed(list(new_str)):
                                stack.pop()
                        if number == len(move[Left]) - 1:
                            stack.append(Str)
                        print("    回溯后，栈为：", stack)
                        print("    ______________")
                        continue
                # stack.append(Str)
                return False

    with open("./判断字符.txt", "r") as f:
        data = f.read().splitlines()
    answer = []
    for string in data:
        print("当前判断字符为：", string)
        state = "q0"
        stack = ["z"]
        # 控制器point
        point = -1
        # print(dfs(list(string), point, state))
        if dfs(list(string), point, state):
            answer.append((string, " 属于"))
            # print("当前语言属于该文法！")
        else:
            answer.append((string, " 不属于"))
            # print("当前语言不属于该文法！")
    for (ii, jj) in answer:
        print(ii, jj)


if __name__ == "__main__":
    transform("test2.txt", V, T, P, S)
    toGNF()
    print("*******************")
    print("V: ", V)
    print("T: ", T)
    for (p, right) in P.items():
        print(p, end="->")
        print("|".join(right))
    # print("S: ", S)
    print("*******************")

    to_npda()
    print("******************")
    print("该GNF对应的状态转移函数如下：")
    for (left, right) in move.items():
        print(left, "->", right)
    print("******************")

    judge()
