# coding=utf-8


'''
trietree包含通配符的实现版.
'''

class SimulateTrieTree(object):
    '''
    Trie Tree
    '''
    def __init__(self, root='', name='trietree'):
        # root节点
        self.root = root
        self.name = name
        # 树结构索引
        self.trietree = dict()
        # 深度限制
        self.max_depth = 0
        # 节点个数限制
        self.node_count = 0

    def index(self, contentlist):
        # 生成索引树
        for content in contentlist:
            tempres = self.trietree
            # for c in content.split(','):
            for c in content:
                if c not in tempres.keys():
                    tempres[c] = dict()
                tempres = tempres[c]
        # print(self.trietree)

    def _format_path(self, *filename):
        # 格式化保存
        return ctl_utils.tag.join([self.root, 'result', self.name] + [f for f in filename])

    def save(self):
        ctl_utils.saveobj_auto(self.trietree, self._format_path('trietree.txt'))
        ctl_utils.saveobj_auto(self.max_depth, self._format_path('max_depth.txt'))
        ctl_utils.saveobj_auto(self.node_count, self._format_path('node_count.txt'))

    def load(self):
        try:
            trietree = ctl_utils.loadobj_auto(self._format_path('trietree.txt'))
            max_depth = ctl_utils.loadobj_auto(self._format_path('max_depth.txt'))
            node_count = ctl_utils.loadobj_auto(self._format_path('node_count.txt'))
            self.trietree = trietree
            self.max_depth = max_depth
            self.node_count = node_count
        except Exception as e:
            traceback.print_exc()

    def select(self, content, tempdict=None, r='', res=set()):
        '''
        # 递归查找
        :param content: 要遍历的文本
        :param tempdict: 字节点树
        :param r: 匹配的文本
        :param res: 匹配好的集合
        :return: 返回查找到的模板结构
        '''
        if tempdict in (None, ):
            tempdict = self.trietree
        # content = str(content)
        # 如果content为单字, 且 ctl_utils.def_tag(通配符) 或 content 在tempdict(余下的节点树)中
        if len(content) == 1 and (content[-1] in tempdict.keys()
                                  or ctl_utils.def_tag in tempdict.keys()):
            if content[-1] in tempdict.keys():
                r = ''.join([r, content[-1]])
                res.add(r)
            elif r == '':
                r = ctl_utils.def_tag
                res.add(r)
            elif ctl_utils.def_tag in tempdict.keys() and r[-1] != ctl_utils.def_tag:
                r = ''.join([r, ctl_utils.def_tag])
                res.add(r)
            return
        # 取首字开始遍历.
        c = content[0]
        #
        if c in tempdict.keys():
            if r in ('', ):
                r_ = c
            else:
                r_ = ''.join([r, c])
            # 查找余下字符串
            self.select(content[1:],  tempdict[c], r_, res=res)
        # 或者 通配符在该层树节点中, 也可将结果添加.
        if ctl_utils.def_tag in tempdict.keys():

            if len(content) > 1:
                for j in range(len(content[1:])):
                    if r in ('', ):
                        r_ = ctl_utils.def_tag
                    elif r[-1] != ctl_utils.def_tag:
                        # 如果r追加的最后一个字符不是通配符
                        r_ = ''.join([r, ctl_utils.def_tag])
                    else:
                        r_ = r
                    # 如果存在通配符, 余下所有字符都可能匹配
                    self.select(content[1+j:], tempdict[ctl_utils.def_tag], r=r_, res=res)
            else:
                if r in ('', ):
                    r_ = ctl_utils.def_tag
                elif r[-1] != ctl_utils.def_tag:
                    r_ = ''.join([r, ctl_utils.def_tag])
                else:
                    r_ = r
                # 如果存在通配符, 则余下所有字符都可能匹配
                self.select(content[-1], tempdict[ctl_utils.def_tag], r=r_, res=res)

    def check(self, content, length):
        '''
        检查content 是否在trietree 中匹配了length个模板
        用于单元测试
        :param content: 文本
        :param length: 匹配模板的个数
        :return:
        '''
        res = set()
        self.select(content, res=res)
        print(content, res)
        if len(res) == length:
            return True
        return False

    def show(self, data=None):
        '''
        辅助查看模板
        :param data:
        :return:
        '''
        if isinstance(data, dict):
            for key, val in data.items():
                self.show(key)
                self.show(val)
        else:
            print(data)
