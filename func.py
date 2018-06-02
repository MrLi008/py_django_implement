#coding=utf-8
'''
    :author mrli
    :date  
    :funcname: 适用于django项目的数据库增改查的接口
'''
import traceback

def checkparams(kwargs,keys,isfullkeys=True):
    if not isinstance(kwargs, dict):
        raise   Exception('Please support dict for params ')
    if not isinstance(keys, list):
        raise   Exception('Please support list for keys')

    if isfullkeys:

        for key in keys:
            if key not in kwargs.keys():
                return False
        return True
    else:
        for key in keys:
             if key in kwargs.keys():
                 return True
        return False

def loadmodels(appname='',modelname='models'):
    ''' 根据app名称, 载入app.models实例'''
    try:
        return dir(getattr(__import__(appname),modelname))
    except Exception as e:
        traceback.print_exc()
    return []

def loadclass(appname='',modelname='models',tablename=''):
    ''' 根据app名称, 模块名称,表名获取表类'''
    try:
        return getattr(getattr(__import__(appname),modelname),tablename)
    except Exception as e:
        traceback.print_exc()
    return None

def loadtable_attributes(appname='',modelname='',tablename='',with_verbose_name=False):
    ''' 根据app名称, 模块名称,表名 获取表的字段列表'''
    if with_verbose_name:
        return loadtable_attributes_with_verbose_name(appname,modelname,tablename)
    else:
        return loadtable_attributes_without_verbose_name(appname,modelname,tablename)


def loadtable_attributes_with_verbose_name(appname='',modelname='models',tablename=''):
    ''' 包含中文名的属性列表'''
    try:
        return [(field.name,field.verbose_name)
                for field in loadclass(appname,modelname,tablename)()._meta.fields]
    except Exception as e:
        traceback.print_exc()
    return []

def loadtable_attributes_without_verbose_name(appname='',modelname='models',tablename=''):
    ''' 不包含中文名的属性列表'''
    try:
        return [key for key in loadclass(appname,modelname,tablename)().toDict().keys()]
    except Exception as e:
        traceback.print_exc()
    return []

def loadtable_all(appname='',modelname='models',tablename=''):
    ''' 返回表中的所有数据'''
    try:
        return [obj.toDict()
                for obj in loadclass(appname,modelname,tablename).objects.all()
                if obj is not None]
    except Exception as e:
        traceback.print_exc()
    return []


def loadtable_one(appname='',modelname='models',tablename='',itemid=''):
    ''' 根据给定的参数, 及itemid 获取指定数据,返回json'''
    try:
        return loadclass(appname,modelname,tablename).objects.get(id=itemid).toDict()
    except Exception as e:
        traceback.print_exc()
    return None

def loadtable_filter(appname='',modelname='models',tablename='',condition=None):
    ''' 根据给定条件获取表中的数据'''
    if not isinstance(condition, dict):
        raise Exception ('Please support type of condition as dict')

    try:
        return [obj.toDict()
                for obj in loadclass(appname,modelname,tablename).objects.filter(**condition )
                if obj is not None]
    except Exception as e:
        traceback.print_exc()
    return []

def savetable_obj(appname='',modelname='models',tablename='',obj=None):
    ''' 根据给定的obj 保存'''
    try:
        loadclass(appname,modelname,tablename)().toObj(data=obj).save()
        return True
    except Exception as e:
        traceback.print_exc()
    return False


def call(funcname,kwargs):
    return getattr(__file__,funcname)(**kwargs)

if __name__ == '__main__':
    pass