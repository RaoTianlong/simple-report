# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 10:14:32 2019

@author: r00386
"""
#%% 引入
from .auxiliary_func import bs, tobs, default_template
from .table import Table


#%% 类


class Report():
    def __init__(self,title,template='default'):
        self.tables = {}
        self.style = ''
        if template == 'default':
            self._sp = bs(default_template)
        elif template[-5:]=='.html':
            self._sp = bs(open(template))
        else:
            try:self._sp = bs(template)
            except: raise ValueError('模板必须是HTML内容或HTML文件路径！')
        
        if not self._sp.head: self._sp.html.insert(0,tobs('<head></head>'))
        if not self._sp.body: self._sp.html.insert(1,tobs('<body></body>'))
        if not self._sp.title: self._sp.head.append(tobs('<title></title>'))
        self._sp.title.string = title
        
    
    def add_table(self,name,df, rindex=None, cindex=None, row_format=None):
        tid = 't'+str(len([x for x in self.tables.values() if isinstance(x,Table)]))
        tb = Table(tid,df,rindex,cindex,row_format)
        self.tables[name] = tb
    
    def add_contents(self,contents,types='p'):
        self.tables[types+str(len(self.tables))] = tobs('<'+types+'>'+contents+'</'+types+'>')
    
    def add_css(self,css):
        if css:
            if css[-4:]=='.css':
                self._sp.head.append(tobs('<link rel="stylesheet" type="text/css" media="screen" href="'+css+'" />'))
            else:
                self.style += css
                #self._sp.head.append(tobs('<style>'+css+'</style>'))
        else:
            pass #self._sp.head.append(tobs('<style></style>'))
    
    def add_js(self,js): #body的js之后再来完善
        if js:
            if js[-3:]=='.js':
                self._sp.head.append(tobs('<script type="text/javascript" src="'+js+'"></script>'))
            else:
                self._sp.head.append(tobs('<script type="text/javascript">'+js+'</script>'))
    
    def add_style(self,style,table_name=None,row='',col=''):
        if not table_name:
            if '{' in style: self.style += style
            else: raise ValueError('不指定表，请输入完整css')
        else:
            self.tables[table_name].add_style(style,row,col)
    
    def add_property(self,table_name,ppt,value,row,col):
        self.tables[table_name].add_property(ppt,value,row,col)
    
    def change_value(self,table_name,value,row,col):
        self.tables[table_name].change_value(value,row,col)
        
    def del_cell(self,table_name,row,col):
        return self.tables[table_name].del_cell(row,col)
    
    def save(self,path='tbs.html'):
        for i in self.tables.values(): 
            if isinstance(i,Table):
                self._sp.body.append(i.tb)
                self.style += i.styles
            else:
                self._sp.body.append(i)
        self._sp.head.append(tobs('<style>'+self.style+'</style>'))
        with open(path,'w',encoding='utf8') as f: #如果不加encoding会有格式问题
            f.write(self._sp.encode(formatter=None).decode())
    
