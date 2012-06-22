import datetime


def datatimenow(returnobject = False):
    if returnobject:
        return datetime.datetime.now()
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def dataexpire(obj):
    old_obj = deepcopy(obj)
    old_obj.id = None
    old_obj.now()
    old_obj.save()
    obj.time_exp = datatimenow()
    obj.save()
    return old_obj

def checkexpired(obj, timecheck = None):
    result = False
    if obj.time_exp:
        if timecheck:
            if obj.time_exp < timecheck:
                result =  True
        else:
            if obj.time_exp < datatimenow(returnobject = True):
                result = True
    return result