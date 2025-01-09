import nodes

class Interpret:
    def __init__(self,code):
        self.code=code
        self.symbols={}
        self.stack=[]
        self.loop_info={'FROM':None,'TO':None,'BY':None}

    def id_exist(self,id):
        return id in self.symbols
    
    def parameter_check(self):
        current_record=self.stack[-1]
        if len(self.symbols[current_record.function_name].params) != len(current_record.arguments):
            raise Exception('Number of arguments error')
        else:
            evaluated_call_time_arg=[self.normalize_expression(i) for i in current_record.arguments]
            t={}
            for i,j in zip(self.symbols[current_record.function_name].params, evaluated_call_time_arg):
                if i.type==j[0]: t[i.id]=j[1]
                else : raise Exception('Argument Type Mismatch')
            current_record.param_arg_map=t
        return True
    
    def format_number(self,value):
        if isinstance(value, int):
            return ('WHOLE',value)
        elif isinstance(value, float) and value.is_integer():
            return ('WHOLE',int(value) )
        else: return ('DECIMAL',value)

    def normalize_expression(self,exp):
        flag={'WHOLE':False,'DECIMAL':False,'WORD':False,'FLAG':False,'COMP_OP':False}
        string=''
        
        for i in exp:
            if type(i) is str:
                if i in ['<','>','=']:
                    if flag['WORD'] or flag['FLAG']:
                        raise Exception("string/bool can't be compared")
                    else:
                        flag['COMP_OP']=True
                        string+=i
                elif flag['WHOLE'] or flag['DECIMAL']:
                    string+=i
                elif flag['WORD'] and i=='+':
                    continue
                else: raise Exception('Type Evaluation Mismatch')
            else:
                if (i.type=='WHOLE' or i.type=='DECIMAL') and not flag['WORD'] and not flag['FLAG']:
                    flag['WHOLE']=True
                    string+=i.value
                elif i.type=='WORD' and not flag['WHOLE'] and not flag['DECIMAL'] and not flag['FLAG']:
                    flag['WORD']=True
                    string+=i.value
                elif i.type=='FLAG' and len(exp)==1:
                    flag['FLAG']=True
                    string+=i.value
                elif i.type=='ID':
                    if i.value in self.symbols:
                        id_type=self.symbols[i.value].data_type
                        id_value=str(self.symbols[i.value].value)
                        if exp[0].type=='ID':
                            string+=id_value
                            flag[id_type]=True
                        elif (flag['WHOLE'] or flag['DECIMAL']) and id_type in ['WHOLE', 'DECIMAL']:
                            string+=id_value
                        elif flag['WORD'] and id_type=='WORD':
                            string+=id_value
                        else: raise Exception('Type Evaluation Mismatch')
                    else: raise Exception(f'{i.value} is not found')

                else: raise Exception('Type Evaluation Mismatch')
            
        if flag['COMP_OP']:
            return('FLAG',eval(string))
        elif flag['WORD']:
            return ('WORD',string)
        elif flag['WHOLE'] or flag['DECIMAL']:
            return self.format_number(eval(string))
        elif flag['FLAG']: return ('FLAG',string)

    def declaration(self,stmt):
        print(stmt)
        if stmt.id in self.symbols:
            raise Exception(f'{stmt.id} is already declared')
        else:
            if stmt.decl_type=='data':
                if stmt.value is None: self.symbols[stmt.id]=Symbol(stmt.decl_type,stmt.data_type,'None')
                else:
                    expr_value=self.normalize_expression(stmt.value)
                    if stmt.data_type==expr_value[0]:
                        self.symbols[stmt.id]=Symbol(stmt.decl_type,stmt.data_type,expr_value[1])
                    else:
                        raise Exception('Type Declaration Mismatch')
            elif stmt.decl_type=='function':
                self.symbols[stmt.id]=Symbol(stmt.decl_type,stmt.data_type,stmt.value,stmt.params)

        # print(self.symbols)

    def assignment(self,stmt):
        if stmt.id in self.symbols:
            expr_value=self.normalize_expression(stmt.value)
            if self.symbols[stmt.id].data_type==expr_value[0]:
                self.symbols[stmt.id].changeValue(expr_value)
            else:
                raise Exception('Type mismatch')
        else:
            raise Exception(f'{stmt.id} is not found')
        # print(self.symbols)

    def printing(self,exp):
        expr_value=self.normalize_expression(exp.value)
        print(expr_value[1])

    def reading(self,exp):
        input_data=input()
        wrap_data=[nodes.Data('STRING',input_data)]
        self.declaration(nodes.Declaration('data','WORD',exp.id,wrap_data))

    def loop(self,stmt):
        print(stmt)
        for i in range(stmt.FROM,stmt.TO,stmt.BY):
            self.run(stmt.body)

    def conditional(self,stmt):
        if self.normalize_expression(stmt.exp)[1]:
            self.run(stmt.body)
        elif type(stmt.next)==nodes.Conditional:
            self.conditional(stmt.next)
        elif type(stmt.next)==list:
            self.run(stmt.next)

    def call_action(self,stmt):
        print(stmt)
        if stmt.id in self.symbols:
            # self.stack.append(nodes.activation_record(stmt.id,stmt.params))
            # print(self.parameter_check())
            self.run(self.symbols[stmt.id].value)
        else: raise Exception('id not found')

    def run(self,code=None):
        try:
            for i in self.code if code is None else code:
                if i.__class__.__name__=='Declaration':
                    self.declaration(i)
                elif i.__class__.__name__=='Assignment':
                    self.assignment(i)
                elif i.__class__.__name__=='Print':
                    self.printing(i)
                elif i.__class__.__name__=='Read':
                    self.reading(i)
                elif i.__class__.__name__=='Loop':
                    self.loop(i)
                elif i.__class__.__name__=='Conditional':
                    self.conditional(i)
                elif i.__class__.__name__=='Call_Action':
                    self.call_action(i)
      
        except Exception as e:
            print("Error: ", e)


class Symbol:
    def __init__(self,symbol_type,data_type,value,params=None):
        self.symbol_type=symbol_type
        self.data_type=data_type
        self.value=value
        self.params=params

    def changeValue(self,value):
        self.value=value

    def __repr__(self):
        return f'Symbol -> {self.symbol_type} {self.data_type} {self.params} = {self.value}'
