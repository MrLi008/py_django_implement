from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from login import func
import packing


# Create your views here.
def index(request):
    pass

def logout(request):
    pass

def impl(request):

    ''' GET请求-帮助提示
        POST请求-数据处理
    '''
    return JsonResponse(packing.JsonResponsePack(data={
        '函数列表及功能':'impl/loadall,impl/loadone,' 
                  'impl/loadfilter,impl/saveobj,impl/loadaattrs',
        '使用提示':'GET请求获取POST请求需要的参数'
    }).val())
def impl_loadaattrs(request):
    ''' 查询指定表包含的字段

    '''
    keys = ['appname','']
def impl_loadall(request):
    ''' 查询指定modelname,tablename 的所有数据并返回json'''
    # 应当包含的参数
    keys = ['appname','modelname','tablename']
    res = None

    if request.method == 'POST':
        kwargs = request.POST
        if func.checkparams(kwargs,keys):
            if 'with_verbose_name' not in kwargs.keys():
                kwargs['with_verbose_name'] = True
            res = func.loadtable_attributes(**kwargs)

    else:
        res = {'support keys':','.join(keys)}
    return JsonResponse(packing.JsonResponsePack(data=res).val())





def impl_loadone(request):
    ''' 查询指定modelname,tablename,id的数据并返回json'''
    # 应当包含的参数
    keys = ['appname', 'modelname', 'tablename','itemid:number']
    res = None
    if request.method == 'POST':
        kwargs = request.POST
        if func.checkparams(kwargs, keys):
            res = func.loadtable_one(**kwargs)
    else:
        res = {'support keys': ','.join(keys)}
    return JsonResponse(packing.JsonResponsePack(data=res).val())


def impl_loadfilter(request):
    ''' 查询指定的modelname,tablename,condition的数据并返回json
        eg. condition: {'key1':'value1','key2':'value2'} --> json格式
    '''
    # 应当包含的参数
    keys = ['appname', 'modelname', 'tablename','condition:json or dict']
    res = None
    if request.method == 'POST':
        kwargs = request.POST
        if func.checkparams(kwargs, keys):
            res = func.loadtable_filter(**kwargs)
    else:
        res = {'support keys': ','.join(keys)}
    return JsonResponse(packing.JsonResponsePack(data=res).val())


def impl_saveobj(request):
    ''' 保存指定的modelname,tablename,obj的数据,并返回保存成功与否
        eg. obj {'id':1,'name':'name1'} --> json格式
    '''
    # 应当包含的参数
    keys = ['appname', 'modelname', 'tablename','obj:json or dict']
    res = None
    if request.method == 'POST':
        kwargs = request.POST
        if func.checkparams(kwargs,keys):
            res = func.savetable_obj(**kwargs)
    else:
        res = {'support keys': ','.join(keys)}
    return JsonResponse(packing.JsonResponsePack(data=res).val())
