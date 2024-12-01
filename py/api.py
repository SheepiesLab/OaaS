from fastapi import FastAPI, Body
import uuid
from test import parse_module

account, classes, functions, moduledesc, objects_by_class = parse_module("account")

app = FastAPI()

@app.get("/")
def GetModuleDesc():
    return moduledesc

@app.get("/{classname}")
def GetClassDesc(classname: str):
    if classname in moduledesc:
        return {"desc": moduledesc[classname], "objects": list(objects_by_class[classname].keys())}
    return {"error": "classname not in module"}

@app.post("/{classname}")
def ConstructClassObj(classname: str):
    if classname not in moduledesc:
        return {"error": "classname not in module"}
    obj_id = uuid.uuid4().hex
    objects_by_class[classname][obj_id] = classes[classname]()
    return {"return":obj_id}

@app.get("/{classname}/{obj_id}")
def GetObj(classname: str, obj_id: str):
    if classname not in moduledesc:
        return {"error": "classname not in module"}
    if obj_id not in objects_by_class[classname]:
        return {"error": "object not exist"}
    return {"return":obj_id}

@app.get("/{classname}/{obj_id}/{methodname}")
def GetObj(classname: str, obj_id: str, methodname: str):
    if classname not in moduledesc:
        return {"error": "classname not in module"}
    if methodname not in moduledesc[classname]["methods"]:
        return {"error": "method not in class"}
    if obj_id not in objects_by_class[classname]:
        return {"error": "object not exist"}
    return {"return":moduledesc[classname]["methods"][methodname]}

@app.post("/{classname}/{obj_id}/{methodname}")
def GetObj(classname: str, obj_id: str, methodname: str, body=Body(None)):
    if classname not in moduledesc:
        return {"error": "classname not in module"}
    if methodname not in moduledesc[classname]["methods"]:
        return {"error": "method not in class"}
    if obj_id not in objects_by_class[classname]:
        return {"error": "object not exist"}
    
    parameters = []
    paramdescs = moduledesc[classname]["methods"][methodname]["parameters"]
    for paramname, paramdesc in paramdescs.items():
        if paramname == 'self':
            continue
        if paramname == 'return':
            continue
        if paramname not in body:
            return {"error": f"required parameter not present: {paramname}"}
        parameters.append(body[paramname])

    ret = classes[classname].__dict__[methodname](objects_by_class[classname][obj_id], *parameters)

    return {"parameters": body, "return": ret}