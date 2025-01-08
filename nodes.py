class Declaration:
    def __init__(self,decl_type,data_type,id,value=None):
        self.decl_type=decl_type
        self.data_type=data_type
        self.id=id
        self.value=value

    def __repr__(self):
        return f'{self.decl_type} {self.data_type} {self.id}={self.value}'


class Assignment:
    def __init__(self,id,value):
        self.id=id
        self.value=value

    def __repr__(self):
        return f'{self.id}={self.value}'


class Data:
    def __init__(self,type,value):
        self.type=type
        self.value=value

    def __repr__(self):
        return f'{self.type}:{self.value}'
    
class Print:
    def __init__(self,value):
        self.value=value

    def __repr__(self):
        return self.value

class Read:
    def __init__(self,id):
        self.id=id

class Loop:
    def __init__(self,FROM,TO,BY,body):
        self.FROM=FROM
        self.TO=TO
        self.BY=BY
        self.body=body

class Conditional:
    def __init__(self,exp,body,next):
        self.exp=exp
        self.body=body
        self.next=next