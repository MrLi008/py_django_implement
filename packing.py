#coding=utf8
'''JsonResponse Pack
'''
import datetime
from django.conf    import settings
import pickle,traceback
class JsonResponsePack(object):
    def __init__(self,msg='',success=True,data=None,status=200):
        self.res = dict()
        self.res['msg'] = msg
        self.res['success'] = success
        self.res['data'] = data
        self.res['status'] = status
    def val(self):
        return self.res
    def __str__(self):
        return str(self.res)


class ToDictObject(object):
    def toDict(self,depth=0):
        result = dict()
        if depth > 10:
            return result
        for field in self._meta.fields:
            if isinstance(getattr(self,field.name) , ToDictObject):
                result[field.name] = getattr(self,field.name).toDict(depth+1)
            elif isinstance(field, (datetime.datetime,datetime.date)):
                result[field.name] = self.__dict__[field.name].strftime('%Y-%m-%d')
            else:
                result[field.name] = getattr(self,field.name)

    def toObj(self,data):
        if data == None:
            return None
        for key,val in data.items():
            if hasattr(self,key):
                setattr(self,key,val)
        return self

def dumpdata(full=True):
    apps = ['conf','info','login','record']
    result = dict()
    for app in apps:
        models = getattr(__import__(app),'models')
        print (models)
        if app not in result.keys():
            result[app] = dict()
        for classname in dir(models):
            classobj = getattr(models,classname)
            # print (classobj)
            if isinstance(classobj,object.__class__):
                # print (classobj)
                if isinstance(classobj(), ToDictObject):
                    if classname not in result[app].keys():
                        result[app][classname] =  classobj.objects.all() # [obj.toDict() for obj in classobj.objects.all()]
                    # print (classobj)
                    # all_data = classobj.objects.all()
                    # print (all_data)
    print (result)
    with open(''.join([settings.BASE_DIR,'/','db.sqlite3.bak']),'wb') as outstream:
        pickle.dump(result,outstream)

def loaddata(full=True):
    with open(''.join([settings.BASE_DIR,'/','db.sqlite3.bak']), 'rb') as instream:
        result = pickle.load(instream)
    errdata = list()
    for modelname, modeldata in result.items():
        for classname, value in modeldata.items():
            for val in value:
                classobj = getattr(getattr(__import__(modelname),'models'),classname)
                if isinstance(classobj(),ToDictObject):
                    # c = classobj().toObj(val)
                    c = val

                    errdata.append(c)
    count = 0
    flag = True
    while flag:
        for d in errdata:
            try:
                d.save()
                count += 1
            except Exception as e:

                traceback.print_exc()
        if count >= len(errdata):
            flag = False
    print ('save success.', str(count))