import nodes
type_map={'WHOLE':int,'DECIMAL':float,'WORD':str,'FLAG':bool}
reverse_type_map={int:'WHOLE',float:'DECIMAL',str:'WORD',bool:'FLAG'}
class Interpret:
    def __init__(self,code):
        self.code=code
        self.symbols={}
        self.stack=[]

    def id_exist(self,id,decl_state=False):
        if decl_state:
            if id in self.stack[-1].locals:
                return self.stack[-1].locals[id]
            else: return False
        else:
            if self.stack[-1].arguments is not None and id in self.stack[-1].arguments:
                return self.stack[-1].arguments[id]
            else:
                for i in self.stack[::-1]:
                    if id in i.locals:
                        return i.locals[id]
                    else: continue
                return False
        
    
    def parameter_check(self,stmt):
        t={}
        if id_exist:=self.id_exist(stmt.id):
           if stmt.params is None and id_exist.params is None:
               return t,id_exist.value
           elif len(stmt.params)!=len(id_exist.params):
               raise Exception('argument length error')
           else:
            for i,j in zip(stmt.params,id_exist.params):
                expr_value=self.normalize_expression(i)
                if expr_value[0] is not type_map[j.type]: raise Exception('argument type error')
                else: t[j.id]=expr_value
            return t,id_exist.value
        else: return False
        
    
    def format_number(self,value):
        if isinstance(value, float) and value.is_integer(): return int(value)
        else: return value

    def normalize_expression(self,exp):  
        flag={'WHOLE':False,'DECIMAL':False,'WORD':False,'FLAG':False,'COMP_OP':False}
        string=''
        for i in exp:
            if i.type=='ID':
                if id_exist:=self.id_exist(i.value):
                    if id_exist.data_type=='WORD': string+=f'\"{id_exist.value}\"'
                    else: string+=id_exist.value
                else: raise Exception(f'[{i.value}] not found')
            elif i.type=='WORD': string+=f'\"{i.value}\"'
            else: string+=i.value

        try:
            x=eval(string)
            if type(x) is float: x=self.format_number(x)
            return (type(x),str(x))
        except: raise Exception('Evaluation error')
        

    def declaration(self,stmt):
        # print(stmt)
        if self.id_exist(stmt.id,True):
            raise Exception(f'[{stmt.id}] is already declared')
        else:
            if stmt.decl_type=='variable':
                if stmt.value is None: self.stack[-1].locals[stmt.id]=Symbol(stmt.decl_type,stmt.data_type)
                else:
                    expr_value=self.normalize_expression(stmt.value)
                    # print(expr_value)
                    if expr_value[0] is type_map[stmt.data_type]:
                        self.stack[-1].locals[stmt.id]=Symbol(stmt.decl_type,stmt.data_type,expr_value[1])
                    else: raise Exception('Type Error')
            elif stmt.decl_type=='function':
                self.stack[-1].locals[stmt.id]=Symbol(stmt.decl_type,stmt.data_type,stmt.value,stmt.params)
            
            # print(self.stack,self.stack[-1].locals)

    def assignment(self,stmt):
        # print(stmt)
        if id_exist:=self.id_exist(stmt.id):
            expr_value=self.normalize_expression(stmt.value)
            if expr_value[0] is type_map[id_exist.data_type]:
                id_exist.changeValue(str(expr_value[1]))
            else:
                raise Exception('Type mismatch')
        else:
            raise Exception(f'[{stmt.id}] is not found')
        # print(id_exist)

    def printing(self,exp):
        expr_value=self.normalize_expression(exp.value)
        print(expr_value[1])

    def reading(self,exp):
        input_data=input()
        wrap_data=[nodes.Data('WORD',input_data)]
        self.declaration(nodes.Declaration('variable','WORD',exp.id,wrap_data))

    def loop(self,stmt):
        # print(stmt)
        for i in range(stmt.FROM,stmt.TO,stmt.BY):
            self.lp_index=i
            self.run('loop',stmt.body)

    def conditional(self,stmt):
        # print(stmt)
        if eval(self.normalize_expression(stmt.exp)[1]):
            self.run('if',stmt.body)
        elif type(stmt.next)==nodes.Conditional:
            self.conditional(stmt.next)
        elif type(stmt.next)==list:
            self.run('else',stmt.next)

    def call_action(self,stmt):
        # print(stmt)
        arg_body=self.parameter_check(stmt)
        if arg_body:
            self.run('action',arg_body[1],arg_body[0])
        else: raise Exception(f'[{stmt.id}] not found')

    def run(self,scope=None,code=None, arg=None):
        try:
            if code is None: self.stack.append(activation_record('main'))
            elif arg is None: self.stack.append(activation_record(scope))
            else: self.stack.append(activation_record(scope,arg))
    
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
            
            # print(self.stack[-1])
            self.stack.pop()
      
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
    

class activation_record:
    def __init__(self,scope,arguments=None):
        self.scope=scope
        self.locals={}
        self.arguments={}
        if arguments is not None:
            for i in arguments:
                self.arguments[i]=Symbol('argument',reverse_type_map[arguments[i][0]],arguments[i][1])
        else: self.arguments=arguments

    
    def __repr__(self):
        return f'{self.scope}  {self.locals} {self.arguments}'