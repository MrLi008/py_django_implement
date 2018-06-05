from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from login import func
import packing
import traceback
import json


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
    keys = ['appname','tablename']
    res = {'support keys:':','.join(keys)}
    if request.method == 'POST':
        kwargs = dict()
        for key,val in request.POST.items():
            try:
                val = json.loads(val)
            except Exception as e:
                pass
                # traceback.print_exc()
            kwargs [key] = val
        # {key: val for key, val in request.POST.items()}
        if func.checkparams(kwargs,keys):

            if 'with_verbose_name' not in kwargs.keys():
                kwargs['with_verbose_name'] = True
            res = func.loadtable_attributes(**kwargs)
            # print ('res: ', res)
        else:
            res['your keys'] = kwargs

    return JsonResponse(packing.JsonResponsePack(data=res).val())



def impl_loadall(request):
    ''' 查询指定modelname,tablename 的所有数据并返回json'''
    # 应当包含的参数
    keys = ['appname','tablename']
    res = {'support keys:':','.join(keys)}

    if request.method == 'POST':
        kwargs = dict()
        for key,val in request.POST.items():
            try:
                val = json.loads(val)
            except Exception as e:
                pass
                # traceback.print_exc()
            kwargs [key] = val
        # {key: val for key, val in request.POST.items()}
        if func.checkparams(kwargs,keys):

            res = func.loadtable_all(**kwargs)
            # print ('res: ', res)
        else:
            res['your keys'] = kwargs


    return JsonResponse(packing.JsonResponsePack(data=res).val())

def impl_loadone(request):
    ''' 查询指定modelname,tablename,id的数据并返回json'''
    # 应当包含的参数
    keys = ['appname', 'tablename','itemid']
    res = {'support keys:':','.join(keys),'tips': 'itemid typeof number'}
    if request.method == 'POST':
        kwargs = dict()
        for key,val in request.POST.items():
            try:
                val = json.loads(val)
            except Exception as e:
                pass
                # traceback.print_exc()
            kwargs [key] = val
        # {key: val for key, val in request.POST.items()}
        if func.checkparams(kwargs, keys):
            res = func.loadtable_one(**kwargs)
            # print ('res: ', res)
        else:
            res['your keys'] = kwargs

    return JsonResponse(packing.JsonResponsePack(data=res).val())


def impl_loadfilter(request):
    ''' 查询指定的modelname,tablename,condition的数据并返回json
        eg. condition: {'key1':'value1','key2':'value2'} --> json格式
    '''
    # 应当包含的参数
    keys = ['appname', 'tablename','condition']
    res = {'support keys:':','.join(keys), 'tips':'condition typeof dict or json'}
    if request.method == 'POST':
        kwargs = dict()
        for key,val in request.POST.items():
            try:
                val = json.loads(val)
            except Exception as e:
                pass
                # traceback.print_exc()
            kwargs [key] = val
        # {key: val for key, val in request.POST.items()}
        if func.checkparams(kwargs, keys):
            res = func.loadtable_filter(**kwargs)
            # print ('res: ', res)
        else:
            res['your keys'] = kwargs
    return JsonResponse(packing.JsonResponsePack(data=res).val())


def impl_saveobj(request):
    ''' 保存指定的modelname,tablename,obj的数据,并返回保存成功与否
        eg. obj {'id':1,'name':'name1'} --> json格式
    '''
    # 应当包含的参数
    keys = ['appname', 'tablename','obj']
    res = {'support keys:':','.join(keys),'tips':'obj typeof dict or json'}
    if request.method == 'POST':
        kwargs = dict()
        for key,val in request.POST.items():
            try:
                val = json.loads(val)
            except Exception as e:
                pass
                # traceback.print_exc()
            kwargs [key] = val
        # {key: val for key, val in request.POST.items()}
        if func.checkparams(kwargs,keys):
            res = func.savetable_obj(**kwargs)
            # print ('res: ', res)
        else:
            res['your keys'] = kwargs

    return JsonResponse(packing.JsonResponsePack(data=res).val())

def cmpl_loadfilter(request):
    ''' 根据给定的多表查询的条件 获取指定的字段'''
    # keys = settings.MY_INSTALLED_APPS# app name list
    keys = ['condition', 'tablelist']
    res = {
        'support keys':','.join(keys),
        'tips':'''condition typeof dict or json, and tablelist typeof list.
            eg. {'condition':{'id':2},'tablelist':['conf.ConfExaminationItem','conf.ConfExaminationPlot']}
        '''
    }
    if request.method == 'POST':
        kwargs = dict()
        for key, val in request.POST.items():
            try:
                val = json.loads(val)
            except Exception as e:
                traceback.print_exc()
            kwargs[key] = val

        if func.checkparams(kwargs,keys):
            ''' 只要kwargs的key, 都存在于keys下即可'''
            res = func.loadtable_filter_cmpl(**kwargs)
        else:
            res ['your keys'] = kwargs


    return JsonResponse(packing.JsonResponsePack(data=res).val())
