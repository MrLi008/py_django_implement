from django.test import TestCase,Client
import packing
import json
# from login import func

# Create your tests here.
class func_testcase(TestCase):
    def setUp(self):
        packing.loaddata()
        self.appname = 'conf'
        self.tablename = 'ConfExaminationItem'
        self.c = Client()

    def test_func_impl_loadattrs(self):
        # packing.loaddata()

        c = self.c
        # appname = 'conf'
        # tablename = 'ConfExaminationItem'

        data = {'appname':self.appname,
                'tablename':self.tablename}
        response = c.post('/impl/loadattrs',data=data)

        self.assertEqual(response.status_code,200)
        # print ('test_func_impl_loadattrs',str(response.content,encoding='utf-8'))

    def test_func_impl_loadall(self):
        # packing.loaddata()
        c = self.c
        data = {'appname':self.appname,
                'tablename':self.tablename}
        response = c.post('/impl/loadall',data=data)
        self.assertEqual(response.status_code,200)
        # print ('test_func_impl_loadall',str(response.content,encoding='utf-8'))

    def test_func_impl_loadfilter(self):
        # packing.loaddata()
        c = self.c

        data = {'appname':self.appname,
                'tablename':self.tablename,
                'condition':json.dumps({
                    'id':1
                    }),
                }
        response = c.post('/impl/loadfilter',data=data)
        self.assertEqual(response.status_code,200)
        # print ('test_func_impl_loadfilter',str(response.content,encoding='utf-8'))

    def test_func_cmpl_loadfilter(self):
        # packing.loaddata()
        c = self.c
        data = {
            'tablelist':json.dumps(['conf.ConfExaminationItem', 'conf.ConfExaminationPlot']),
            'condition':json.dumps({'id':2})
        }
        response = c.post('/cmpl/loadfilter',data=data)
        self.assertEqual(response.status_code, 200)
        # print ('test func cmpl loadfilter: ', str(response.content, encoding='utf-8'))

    def test_func_impl_loadone(self):
        # packing.loaddata()
        c = self.c
        data = {'appname':self.appname,
                'tablename':self.tablename,
                'itemid':1}
        response = c.post('/impl/loadone',data=data)
        self.assertEqual(response.status_code,200)
        # print ('test_func_impl_loadone',str(response.content,encoding='utf-8'))

    def test_func_impl_saveobj(self):
        # packing.loaddata()
        c = self.c
        data = {
            'appname':self.appname,
            'tablename':self.tablename,
            'obj':json.dumps({
                'item_name':'test_item_name',
                'item_type':'工作考核',
                'score_total':10000.0,
                'score_default':0,
                'score_top_limit':10000.0,
                'score_bottom_limit':0,
                'item_count_limit':0,
            }),
        }
        response = c.post('/impl/saveobj',data=data)
        self.assertEqual(response.status_code,200)
        # print ('test_func_impl_saveobj',str(response.content,encoding='utf-8'))




from login import func
class func_load_test(TestCase):
    def setUp(self):
        pass
    def test_func_impl_loadmodels(self):
        data = {
            'appname':'conf',
        }

        res = func.loadtables(**data)
        self.assertListEqual(res, ['ConfExaminationItem', 'ConfExaminationPlot'])


