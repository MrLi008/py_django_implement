#coding=utf-8
'''
    :author mrli
    :date  
    :funcname: 适用于django项目的数据库增改查的接口
'''
import traceback
import packing
import assistdb

def checkparams(kwargs,keys,isfullkeys=True):
    '''
    :param kwargs: 提交的参数
    :param keys:  指定的key
    :param isfullkeys: 是否满key
        True For keys中的值kwargs中必须存在
        False For kwargs中的key 必须存在于keys中
    :return: 检验结果
    '''
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
        for key in kwargs.keys():
             if key not in keys:
                 return False
        return True

def loadtables(appname='',modelname='models'):
    ''' 根据app名称, 载入app.models下所有表实例'''
    result = list()
    try:
        modelobj = getattr(__import__(appname),modelname)
        # print (modelobj)

        for classname in dir(modelobj):
            # print (classname)
            classobj = getattr(modelobj,classname)
            if hasattr(classobj,'__call__') and isinstance(classobj(),packing.ToDictObject):
                result.append(classname)

    except Exception as e:
        traceback.print_exc()
    return result


def loadclass(appname='',modelname='models',tablename=''):
    ''' 根据app名称, 模块名称,表名获取表类'''
    try:
        return getattr(getattr(__import__(appname),modelname),tablename)
    except Exception as e:
        traceback.print_exc()
    return None

def loadtable_attributes(appname='',modelname='models',tablename='',with_verbose_name=False):
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

def loadtable_filter_cmpl(tablelist=None,condition=None):
    '''

    :param kwargs: {'condition': {......},'tablelist':[...]}
    :return: list [dict..]
    '''
    res = None
    cdm_one2many = assistdb.loaddb_cdm(condition='one_to_many')
    # condition = kwargs.get('condition') # eg. {'id':2}
    # tablelist = kwargs.get('tablelist') # eg. ['conf.ConfExaminationItem', 'conf.ConfExaminationPlot']
    if not isinstance(tablelist, list) or not isinstance(condition, dict):
        raise Exception ('Please support tablelist typeof list and condition typeof dict')
    for i in range(len(tablelist)):
        tablename_full = tablelist[i]
        appname = tablename_full.split('.')[0]
        tablename = tablename_full.split('.')[-1]
        # print (condition)
        res = loadclass(appname=appname, tablename=tablename).objects.filter(**condition)
        # print (res)
        if i + 1 < len(tablelist):
            condition = {''.join([cdm_one2many[tablelist[i]][tablelist[i + 1]],'__in']): [r.toDict().get('id') for r in res]}
    return [r.toDict() for r in res if r is not None]

def call(funcname,kwargs):
    return getattr(__file__,funcname)(**kwargs)

if __name__ == '__main__':
    pass