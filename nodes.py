class Declaration:
    def __init__(self,decl_type,data_type,id,value=None,params=None):
        self.decl_type=decl_type
        self.data_type=data_type
        self.id=id
        self.value=value
        self.params=params

    def __repr__(self):
        if self.decl_type=='function':
            return f'{self.decl_type} :: {self.data_type} {self.id} {self.params} = {self.value}'
        else: return f'{self.decl_type} :: {self.data_type} {self.id} = {self.value}'


class Assignment:
    def __init__(self,id,value):
        self.id=id
        self.value=value

    def __repr__(self):
        return f'{self.id} = {self.value}'

class Data:
    def __init__(self,type,value):
        self.type=type
        self.value=value

    def __repr__(self):
        return f'{self.type}:{self.value}'
    
class Parameter:
    def __init__(self,type,id):
        self.type=type
        self.id=id

    def __repr__(self):
        return f'{self.type}:{self.id}'
    
class Print:
    def __init__(self,value):
        self.value=value

    def __repr__(self):
        return f'{self.value}'

class Read:
    def __init__(self,id):
        self.id=id

class Loop:
    def __init__(self,FROM,TO,BY,body):
        self.FROM=FROM
        self.TO=TO
        self.BY=BY
        self.body=body

    def __repr__(self):
        return f'LOOP :: ({self.FROM}->{self.TO}->{self.BY}) = {self.body}'

class Conditional:
    def __init__(self,exp,body,next):
        self.exp=exp
        self.body=body
        self.next=next

    def __repr__(self):
        return f'CONDITIONAL :: {self.exp} = {self.body} -> {self.next}'
    
class Call_Action:
    def __init__(self,id,params):
        self.id=id
        self.params=params

    def __repr__(self):
        return f'Call :: {self.id} {self.params}'