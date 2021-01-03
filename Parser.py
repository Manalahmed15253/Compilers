import sys
import uuid
import pydot
from subprocess import check_call
import random
import os
#Token Types
IF_token = "IF"
Then_token = "THEN"
Else_token ="ELSE"
End_token = "END"
Repeat_token = "REPEAT"
Until_token = "UNTIL"
Read_token = "READ"
Write_token = "WRITE"

Plus_token = "PLUS"
Minus_token = "MINUS"
Multiply_token = "MULT"
Division_token = "DIV"
Equal_token = "EQUAL"
Assign_token = "ASSIGN"
Compare_token = "LESSTHAN"
LeftPar_token = "LEFTBRACKET"
RightPar_token = "RIGHTBRACKET"
Semicolon_token = "SEMICOLON"
ID_token = "IDENTIFIER"
Num_token = "NUMBER"
Stmt_Start = [Read_token,IF_token,Repeat_token,Assign_token,Write_token]
#function to invert the List
def invertList(input_list):
    input_list.reverse()
    return input_list

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
def match(expectedTokenType):
    global token
    global error
    if token.type == expectedTokenType :
        #token = scanner.getNextToken()
        global Index
        Index = Index +1
        if Index+1 > len(L):
            return
        token = L[Index]
    else:
        print(expectedTokenType)
        print("There is an Error From match")
        syntax_tree.write_png("parser_syntax_tree.png")
        error = 1
        #sys.exit()

class parser :
    def __init__(self,fileName):
        self.fileName = fileName

    def intitalValues(self):
        f = open(self.fileName,"r")
        global L
        L = []
        global Index
        Index = 0
        for i in f:
            line = i.strip()
            tok =Token(line.split(',')[1] ,line.split(',')[0])
            L.append(tok)
        global token
        token = L[Index]
        global syntax_tree
        syntax_tree = pydot.Dot(graph_type='graph',rankdir="TB",strict=True)
        global error
        error = 0


    #addop → + | -
    def parse_addop(self):
        global token
        global syntax_tree
        global error
        if token.type == Plus_token :
            match(Plus_token)
            # creating addop node
            node_id = str(uuid.uuid4())
            addop_node = pydot.Node(node_id,label="op (+)")

        elif token.type == Minus_token :
            match(Minus_token)
            # creating addop node
            node_id = str(uuid.uuid4())
            addop_node = pydot.Node(node_id,label="op (-)")
            # syntax_tree.add_node(addop_node)
            # syntax_tree.write_png("parser_syntax_tree.png")
        else:
            print("There is an Error From Parse_addop")
            syntax_tree.write_png("parser_syntax_tree.png")
            error = 1
            #sys.exit()
        print("parse_addop Done!")
        return addop_node #op(-)

    #mulop → * | /
    def parse_mulop(self):
        global token
        global syntax_tree
        global error
        global L
        global Index

        if token.type == Multiply_token :
            # if ((Index+2)<(len(L)-1)):
            #     if(L[Index+2].type == Minus_token or L[Index+2].type == Plus_token or L[Index+2].type == Multiply_token or L[Index+2].type == Division_token ):
            #         error = 1
            match(Multiply_token)
            # creating mulop node
            node_id = str(uuid.uuid4())
            mulop_node = pydot.Node(node_id,label="op (*)")

        elif token.type == Division_token :
            # if ((Index+2)<(len(L)-1)):
            #     if(L[Index+2].type == Minus_token or L[Index+2].type == Plus_token or L[Index+2].type == Multiply_token or L[Index+2].type == Division_token ):
            #         error = 1
            match(Division_token)
            # creating mulop node
            node_id = str(uuid.uuid4())
            mulop_node = pydot.Node(node_id,label="op (/)")
        else:
            print("There is an Error From Parse_mulop")
            syntax_tree.write_png("parser_syntax_tree.png")
            error = 1
            #sys.exit()
        print("parse_mulop Done!")
        return mulop_node


    #comparison-op → < | =
    def parse_comparison_op(self):
        global token
        global syntax_tree
        global error

        if token.type == Compare_token :
            match(Compare_token)
            # creating comparison_op node
            node_id = str(uuid.uuid4())
            comparison_op_node = pydot.Node(node_id,label="op (<)")
        elif token.type == Equal_token :
            match(Equal_token)
            # creating comparison_op node
            node_id = str(uuid.uuid4())
            comparison_op_node = pydot.Node(node_id,label="op (=)")
        else:
            print("There is an Error From Parse_comparison_op")
            syntax_tree.write_png("parser_syntax_tree.png")
            error = 1
            #sys.exit()

        print("parse_comparison_op Done!")
        return comparison_op_node

    #term → factor {mulop factor}
    def parse_term(self):
        global token
        global syntax_tree
        node_id = str(uuid.uuid4())
        return_node = pydot.Node(node_id,label="error")
        flag=0
        factor_left_node=self.parse_factor() #const(1) 
        return_node =factor_left_node #const(1)
        syntax_tree.add_node(factor_left_node) #const(1) 
        while token.type == Multiply_token or token.type == Division_token and error == 0:
            flag+=1
            op_node=self.parse_mulop()
            if error == 1 :
                break
            syntax_tree.add_node(op_node)
            if flag > 1 : 
                syntax_tree.add_edge(pydot.Edge(op_node,first_op_node))  
            factor_right_node=self.parse_factor()
            if error == 1 :
                break
            syntax_tree.add_node(factor_right_node)
            syntax_tree.add_edge(pydot.Edge(op_node,factor_right_node))
            return_node =op_node
            if flag >= 1 :
                first_op_node=op_node 
            if flag ==1 :
                our_bottom_node=op_node
        if flag:
            syntax_tree.add_edge(pydot.Edge(our_bottom_node,factor_left_node))

        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_term Done!")
        return return_node #const(1)


    #simple-exp → term {addop term}
    def parse_simple_exp(self):
        global token
        global L
        global Index
        global error
        node_id = str(uuid.uuid4())
        return_node = pydot.Node(node_id,label="error")
        flag=0
        term_left_node=self.parse_term() #const(1)
        return_node=term_left_node #conts(1)
        syntax_tree.add_node(term_left_node)
        while token.type == Minus_token or token.type == Plus_token and error == 0:
            # if ((Index+2)<(len(L)-1)):
            #     if(L[Index+2].type == Minus_token or L[Index+2].type == Plus_token or L[Index+2].type == Multiply_token or L[Index+2].type == Division_token ):
            #         error = 1
            flag+=1            
            op_node=self.parse_addop() #op(-) #five
            if error == 1 :
                break
            syntax_tree.add_node(op_node)
            if flag > 1 : #comment
                syntax_tree.add_edge(pydot.Edge(op_node,first_op_node))  
            term_right_node=self.parse_term() #const(2)
            if error == 1 :
                break
            syntax_tree.add_node(term_right_node)
            syntax_tree.add_edge(pydot.Edge(op_node,term_right_node)) #1st egde
            return_node =op_node #op(-)
            if flag >= 1 :
                first_op_node=op_node 
            if flag ==1 :
                our_bottom_node=op_node
        if flag and error == 0:
            syntax_tree.add_edge(pydot.Edge(our_bottom_node,term_left_node))
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_simple_exp Done!")
        return return_node

    #exp → simple-exp  [ comparison-op simple-exp ]
    def parse_exp(self):
        global token
        global syntax_tree
        node_id = str(uuid.uuid4())
        return_node = pydot.Node(node_id,label="error")
        optional =0
        simple_exp_left_node=self.parse_simple_exp() #four
        return_node=simple_exp_left_node
        syntax_tree.add_node(simple_exp_left_node)
        if token.type == Compare_token or token.type == Equal_token :
            optional =1
            op_node=self.parse_comparison_op()
            syntax_tree.add_node(op_node)
            simple_exp_right_node=self.parse_simple_exp()
            syntax_tree.add_node(simple_exp_right_node)
            syntax_tree.add_edge(pydot.Edge(op_node,simple_exp_right_node))
            return_node=op_node
        if optional :
            syntax_tree.add_edge(pydot.Edge(op_node,simple_exp_left_node))

        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_exp Done!")
        return return_node

    #factor → (exp)  |  number |  identifier
    def parse_factor(self):
        global token
        global syntax_tree
        global error
        node_id = str(uuid.uuid4())
        return_node = pydot.Node(node_id,label="error")
        if token.type == Num_token:
            # creating number node
            node_id = str(uuid.uuid4())
            num_label="const ({num})".format(num=token.value)
            print(token.value)
            factor_node = pydot.Node(node_id,label=num_label)
            #syntax_tree.add_node(factor_node) 
            return_node=factor_node #const(1) --> const(2)
            match(Num_token)

        elif token.type == ID_token:
            # creating ID node
            node_id = str(uuid.uuid4())
            id_label="id ({id_name})".format(id_name=token.value)
            factor_node = pydot.Node(node_id,label=id_label)
            #syntax_tree.add_node(factor_node)
            return_node=factor_node
            match(ID_token)

        elif token.type == LeftPar_token:
            match(LeftPar_token)
            return_node=self.parse_exp()
            #syntax_tree.add_node(return_node)
            match(RightPar_token)
        else:
            print("There is an Error From Parse_factor")
            syntax_tree.write_png("parser_syntax_tree.png")
            error = 1
            #sys.exit()
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_factor Done!")
        return return_node #const(1) --> const(2)

      #if-stmt → if exp then stmt-sequence [else stmt-sequence] end
    def parse_if_stmt(self):
        global token
        global syntax_tree
        global error
        match(IF_token)
        # creating IF node
        node_id = str(uuid.uuid4())
        if_stmt_node = pydot.Node(node_id,label="IF",shape="rectangle")
        syntax_tree.add_node(if_stmt_node)
        exp_node=self.parse_exp()
        match(Then_token)
        then_parse_stmt_node=self.parse_stmt_sequence()
        if token.type == Else_token :
            match(Else_token)
            else_parse_stmt_sequence_node=self.parse_stmt_sequence()
            syntax_tree.add_node(else_parse_stmt_sequence_node)
            syntax_tree.add_edge(pydot.Edge(if_stmt_node,else_parse_stmt_sequence_node))
            match(End_token)
            print("parse_if_stmt Done!")
        elif token.type == End_token :
            match(End_token)
            print("parse_if_stmt Done!")
        else:
            print("There is an Error From parse_if_stmt")
            syntax_tree.write_png("parser_syntax_tree.png")
            error = 1
            #sys.exit()
        syntax_tree.add_node(then_parse_stmt_node)
        syntax_tree.add_edge(pydot.Edge(if_stmt_node,then_parse_stmt_node))

        syntax_tree.add_node(exp_node)
        syntax_tree.add_edge(pydot.Edge(if_stmt_node,exp_node))

        syntax_tree.write_png("parser_syntax_tree.png")
        return if_stmt_node

    #repeat-stmt → repeat stmt-sequence until exp
    def parse_repeat_stmt(self):
        global syntax_tree
        node_id = str(uuid.uuid4())
        repeat_node = pydot.Node(node_id,label="error")
        match(Repeat_token)
        # creating Repeat node
        node_id = str(uuid.uuid4())
        repeat_node = pydot.Node(node_id,label="Repeat",shape="rectangle")
        syntax_tree.add_node(repeat_node)
        stmt_sequence_node=self.parse_stmt_sequence()
        match(Until_token)
        exp_node=self.parse_exp()
        syntax_tree.add_node(exp_node)
        syntax_tree.add_edge(pydot.Edge(repeat_node,exp_node))
        syntax_tree.add_node(stmt_sequence_node)
        syntax_tree.add_edge(pydot.Edge(repeat_node,stmt_sequence_node))
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_repeat_stmt Done!")
        return repeat_node

    #assign-stmt → identifier := exp
    def parse_assign_stmt(self):
        global syntax_tree
        node_id = str(uuid.uuid4())
        assign_node = pydot.Node(node_id,label="error")
        identifier_val = token.value #x
        match(ID_token)
        match(Assign_token)
        # creating Assign node
        node_id = str(uuid.uuid4())
        Assign_label="Assign({id})".format(id=identifier_val)
        assign_node = pydot.Node(node_id,label=Assign_label,shape="rectangle")
        syntax_tree.add_node(assign_node)
        parse_exp_node=self.parse_exp()   #three
        syntax_tree.add_node(parse_exp_node)
        syntax_tree.add_edge(pydot.Edge(assign_node,parse_exp_node))
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_assign_stmt Done!")
        return assign_node

    #read-stmt → read identifier
    def parse_read_stmt(self):
        global syntax_tree
        node_id = str(uuid.uuid4())
        read_node = pydot.Node(node_id,label="error")
        match(Read_token)
        identifier_val = token.value
        match(ID_token)
        # creating Assign node
        node_id = str(uuid.uuid4())
        read_label="Read({id})".format(id=identifier_val)
        read_node = pydot.Node(node_id,label=read_label,shape="rectangle")
        syntax_tree.add_node(read_node)
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_read_stmt Done!")
        return read_node

    #write-stmt → write exp
    def parse_write_stmt(self):
        global syntax_tree
        node_id = str(uuid.uuid4())
        write_node = pydot.Node(node_id,label="error")
        match(Write_token)
        node_id = str(uuid.uuid4())
        write_node = pydot.Node(node_id,label="Write",shape="rectangle")
        syntax_tree.add_node(write_node)
        parse_exp_node=self.parse_exp()
        syntax_tree.add_node(parse_exp_node)
        syntax_tree.add_edge(pydot.Edge(write_node,parse_exp_node))
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_write_stmt Done!")
        return write_node

    #statement→ if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
    def parse_statement(self):
        global token
        global syntax_tree
        node_id = str(uuid.uuid4())
        statetment_node = pydot.Node(node_id,label="error")
        if token.type == IF_token :
            statetment_node = self.parse_if_stmt()
        elif token.type == Repeat_token :
            statetment_node = self.parse_repeat_stmt()
        elif token.type == Read_token :
            statetment_node = self.parse_read_stmt()
        elif token.type == Write_token :
            statetment_node = self.parse_write_stmt()
        else:
            statetment_node = self.parse_assign_stmt() #two
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_statement Done!")
        return statetment_node

    #stmt-sequence → statement{; statement} ##EBNF
    def parse_stmt_sequence(self):
        random_number = random.randint(0,16777215)
        hex_number = str(hex(random_number))
        hex_number ='#'+ hex_number[2:]
        global token
        global syntax_tree
        global error
        statement_list=[]
        horizontal_stmts_id_list=[]
        statement_node = self.parse_statement() ##1st #one
        statement_list.append(statement_node)
        return_node=statement_node ##1st
        if Index + 1 > len(L):
            print("here parse_stmt_sequence Done!")
            return
        else:
            while token.type == Semicolon_token and error ==0:
                match(Semicolon_token)
                if error == 1 :
                    break
                optional_statement_node =self.parse_statement() ##2nd
                if error == 1 :
                    break
                statement_list.append(optional_statement_node)
                statement_node = optional_statement_node
                print(token.type)
        for i in range(len(statement_list)-1) :
            syntax_tree.add_edge(pydot.Edge(statement_list[i],statement_list[i+1],constraint=False,color=hex_number))
        syntax_tree.write_png("parser_syntax_tree.png")
        print("parse_stmt_sequence Done!")
        return return_node
    def check_correctness(self):
        if token == L[len(L)-1] and error == 0:
            for i in Stmt_Start :
                print(i)
                if token.type == i :
                    print("wrong")
                    return 1
            print("Correct")
            return 0
        else :
            print("Wrong")
            return 1



# p=parser("Output.txt")
# p.intitalValues()
# p.parse_stmt_sequence()
# p.check_correctness()
