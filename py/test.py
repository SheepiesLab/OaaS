import importlib
import inspect
import json

def parse_param(paramname, fullargspec, default, selftype='any'):
    paramdesc = {}
    if paramname in fullargspec.annotations:
        typename = None
        if fullargspec.annotations[paramname] is not None:
            typename = fullargspec.annotations[paramname].__name__
        paramdesc['type'] = typename
    elif paramname == 'self':
        paramdesc['type'] = selftype
    else:
        paramdesc['type'] = 'any'
    if default is not None:
        paramdesc['default'] = default
    return paramdesc

def parse_function(membername, memberdef, selftype='any'):
    funcdesc = {"name": membername, "type": "function", "parameters": {}}
    fullargspec = inspect.getfullargspec(memberdef)
    defaults = [None] * len(fullargspec.args)
    if fullargspec.defaults is not None:
        defaults = [None] * (len(fullargspec.args) - len(fullargspec.defaults)) +list(fullargspec.defaults)
    for i, pname in enumerate(fullargspec.args):
        default = defaults[i]
        funcdesc["parameters"][pname] = parse_param(pname, fullargspec, default, selftype)
    funcdesc["parameters"]['return'] = parse_param('return', fullargspec, None, selftype)
    return funcdesc

def parse_class(classname, classdef):
    classdesc = {"name": classname, "type": "class", "methods": {}}
    for membername, memberdef in classdef.__dict__.items():
        if not callable(memberdef):
            continue
        if isinstance(memberdef, type):
            classdesc['classes'][membername] = parse_class(membername, memberdef)
        if membername == '__init__':
            membername = classname
        classdesc["methods"][membername] = parse_function(membername, memberdef, classname)
        
    return classdesc

def parse_module(modulename: str):

    account = importlib.import_module("account")
    classes = dict([(name, cls)
                    for name, cls in account.__dict__.items()
                    if isinstance(cls, type)])
    functions = dict([(name, func)
                    for name, func in account.__dict__.items()
                    if callable(func) and name not in classes])



    moduledesc = {}
    objects_by_class = {}
    for classname, classdef in classes.items():
        moduledesc[classname] = parse_class(classname, classdef)
        objects_by_class[classname] = {}

    for funcname, funcdef in functions.items():
        moduledesc[funcname] = parse_function(funcname, funcdef)

    return account, classes, functions, moduledesc, objects_by_class

account, classes, functions, moduledesc, objects_by_class = parse_module("account")
print(json.dumps(moduledesc, indent=2))


    


'''
OaaS Common Class Specification

interface:     name
               method list

class:         name
               method list

method:        name
               parameter list

parameter:     name
               type
               default value

type:          int / float / bool / string / null / interface / class
'''
