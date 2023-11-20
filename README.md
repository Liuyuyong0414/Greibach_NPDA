# Greibach_NPDA
	Transform
将输入文法转换为G=(V,T,P,S)形式，其中V是非终结符集合，T是终结符集合，P是产生式集合，S是起始符，下图为转化前和转化后的文法。
            
图2 输入文法                图3   转化为V，T，P，S
	消除无用符号
伪代码：
FUNCTION delete_useless():
    INITIALIZE reach=[ ]
    FUNCTION search(v):
        IF v not in reach:
            ADD v to reach
        FOR 非终结符v的每一个产生式:
            FOR 字符 in 产生式:
                IF 字符为非终结符且不在reach中:
                    search(character)
                ELSE IF 字符为终结符且不在reach中:
                    ADD character to reach
    search(起始符”S“)
    UPDATE V，T，P
    PRINT results
END FUNCTION

使用DFS从起始点S开始对文法进行深度优先搜索，对可达到的终结符和非终结符进行记录，保存为reach数组和non_reach数组，然后根据搜索结果遍历语法产生式表。对从起始点S无法到达的非终结符和终结符，删除其相关产生式，并将无用符号从V和T中删除。下图为删除无用符号Q和R。
 
图4 消除之前的文法

 
图5 生成可达和不可达符号集，进行产生式删除

	消除单一产生式

伪代码：
FUNCTION delete_single():
    FUNCTION get_pair():
        收集所有的单元偶对如（A，B）；
    DO：
        INITIALIZE 使用get_pair()更新单元偶对组；
        IF 没有单元偶对，结束循环；
        FOR each (A, B) in pair:
            使用B所有的产生式右部替换B，移除A->B
    PRINT updated grammar components
END FUNCTION

遍历产生式列表，寻找所有的单元偶对（A，B）,A、B均为非终结符，然后将由B推导的产生式全部加入A中，并将B从A的产生式列表删除，不断循环这个过程，直至没有单元偶对被发现。
 
图6 将A->B进行消除

	消除ε产生式

伪代码：
FUNCTION delete_epsilon():
    FUNCTION can_be_epsilon(v):
        RETURN 根据V0和V1判断v是否能推出ε
    DO:
        //根据产生式直接更新V0和V1
        V0 = 可空符号集
        V1 = 不可空符号集
        UPDATE V0 and V1 using can_be_epsilon()
        UPDATE P（包括替换可空符号和删除除S->ε外的ε推导）
        REMOVE useless symbols from grammar
    WHILE V0为空或者V0只有起始符”S“
    PRINT updated grammar
END FUNCTION

定义循环，循环结束条件为语法系统中无ε产生式，除S->ε外。循环内部，定义可致空符号集V0和不可致空符号集V1，先粗略遍历产生式列表，将直接产生空的非终结符加入符号集V0，将所有产生式都能产生非空符号的非终结符加入符号集V1。利用当前生成的符号集，对剩余的非终结符产生式进行替换判断，直到所有的非终结符都加入对应的集合。如果可致空符号集为空或者只有起始符S，则结束循环，否则就将产生式中可空的推导删除。如果存在只能推出空的非终结符，则将其产生式P和V中对应的元素进行删除。如下图所示，为一例删除空产生式示例。
 
图7 循环删除可空表达式

	消除左递归（间接和直接）

直接左递归伪代码
FUNCTION delete_direct_left_recursive():
    FOR each production (p, right) in P:
        alpha=[ ]，beta=[ ]//alpha记录以p开头的剩余部分，beta记录其他所有
        IF alpha不为空，即存在直接左递归
            按照公式替换
END FUNCTION

间接左递归代码
FUNCTION delete_left_recursive():
    FUNCTION search()
        DFS寻找某个非终结符推导其本身开头字符串的路径
    DO:
        delete_direct_left_recursive()  # 先处理一次直接左递归
        FOR 每一个非终结符 in P:
            search（）//搜索路径
        IF 某个非终结符存在此路径：
            按照路径进行产生式替换
        WHILE 所有的非终结符均不存在此路径：
END FUNCTION

删除直接左递归：定义函数，判断产生式右部第一符号是否为产生式左部非终结符，若判断为真，则存在直接左循环，则引入符号对产生式进行替换，替换如书上公式。
删除间接左递归：开始循环，首先调用删除直接左递归函数对语法进行初步处理，然后使用DFS对产生式进行搜索，判断是存在一条路径使得当前非终结符能经过一系列推导到达当前非终结符，若存在，则按照路径进行产生式替换，将其转变为直接左递归，然后进行循环，若不存在，则退出循环。下图为一例消除左递归实例。
 
图8 消除左递归文法

	产生式右部终结符打头和非首元素为非终结符
处理以非终结符开头的产生式：进入循环，遍历产生式，若存在产生式右部首位为非终结符，则使用该非终结符能推导产生式进行替换，若遍历整个产生式列表P均不存在，则退出循环。
处理不处于后继的终结符：定义字典保存新引入的非终结符和对应非终结符的映射关系，遍历产生式列表，若存在产生式右部非首位为终结符的情况，则利用已生成的映射关系或者寻找新的映射关系对其进行替换。如图所示，为一例转化情况。
 
图9 转化为Greibach范式

	转化为Greibach测试结果
	测试1
     
图10 测试样例                   图11 Greibach文法生成

	测试2
 
图12 测试文法
 
图13 Greibach文法
	测试3
 
图14 测试文法
 
图15 Greibach文法
	GNF转化为NPDA
（1）构造转移函数
共三种状态，起始状态q0,中间状态q1，终止状态qf，将起始转移函数move[("q0", "", "z")] = [("q1", "Sz")]和终止转移函数move[("q1", "", "z")] = [("qf", "z")]加入转移序列，特判S->ε,将move[("q1", "", "S")] = [("qf", "z")]加入转移序列，其余按照产生式进行逐个添加，示例如下：
（2）判断给定语言是否属于当前文法
伪代码：
FUNCTION judge():
    FUNCTION dfs(String, Point, State):
        IF Point==-1://设置初始指针位置为-1，字符为空，执行起始转移函数
              // 下推栈出栈，构造转移左部Left
              // 根据转移函数，将字符串倒推入栈
        ELSE:
                // 下推栈出栈
               IF 指针移至字符最后
                     // 使用空字符串构造转移左部Left
               ELSE：
                     // 使用当前位置字符构造Left
                For 每一个Left的move函数：
                      IF 下一个状态为qf：
                          RETURN 该语言符合文法
                      ELSE:
                              IF 当前搜索路径可以到达qf：返回TRUE
                              ELSE：
                                   回溯，先将右部元素出栈，再将左部元素入栈
                  RETURN False //如果所有move都不能到达，则不符合
    FOR 每一个需要判断的语句
          INITIALIZE 初始状态q0，下推栈z，指针p=-1
          DO dfs( )
END FUNCTION
