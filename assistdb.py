#coding=utf-8
'''
    :author mrli
    :date  
    :funcname 数据库操作辅助工具
'''
import time

from django.conf import settings
from login import func
def loaddb_cdm(condition='one_to_many'):
    ''' 查找此table被引用了的表-以及在被引用的表中的字段名'''
    result = dict()
    time.sleep(2)

    for appname in settings.MY_INSTALLED_APPS:
        for tablename in func.loadtables(appname):
            for field in func.loadclass(appname=appname, tablename=tablename)._meta.get_fields():

                if field.is_relation and getattr(field,condition) == True:
                    tablename_full = '.'.join([appname,tablename])
                    related_table = None
                    related_attrname = None

                    if hasattr(field,'related_model'):
                        related_table = getattr(field,'related_model')._meta.label
                    if hasattr(field, 'remote_field') and hasattr(getattr(field,'remote_field'),'column'):
                        related_attrname = getattr(getattr(field,'remote_field'),'column')
                    elif hasattr(field,'attname'):
                        related_attrname = getattr(field, 'attname')

                    if tablename_full != None and related_table != None and related_attrname != None:
                        if tablename_full not in result.keys():
                            result[tablename_full] = dict()
                        if related_table not in result.get(tablename_full).keys():
                            result[tablename_full][related_table] = related_attrname

    return result


if __name__ == '__main__':
    pass