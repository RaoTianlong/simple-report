# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:46:50 2019

@author: r00386
"""
from .auxiliary_func import bs, tobs, bs4

class Table():
    def __init__(self,tid, df, rindex=None, cindex=None, row_format=None): #之后升级多层表头和df多层索引的情况
        self.tb = bs(df.to_html()).table
        del self.tb['border'];del self.tb['class'];del self.tb.tr['style'];
        self.shape = [df.shape[0]+1,df.shape[1]+1]
        self.styles = ''
        self.rindex = rindex
        self.cindex = cindex
        self.row_format = row_format
        self.tid = tid
        self.set_id()
        self.set_index()
        self.set_format()
    
    def set_id(self):
        # 添加id，class
        r = 0 
        for i in self.tb.find_all('tr'):
            c = 0
            i['class'] = self.tid+'_r'+str(r)
            for j in i.contents:
                if isinstance(j,bs4.element.Tag):
                    j['id'] = self.tid+'_r'+str(r)+'_c'+str(c)
                    j['class'] = self.tid+'_c'+str(c)
                    c += 1
            r += 1
            
    def set_index(self):
        # 修改index
        if self.rindex :
            for i in range(len(self.rindex)):
                self.replace_string(self.tid+'_r'+str(i)+'_c0',self.rindex[i])
        if self.cindex :
            for i in range(len(self.cindex)):
                self.replace_string(self.tid+'_r0'+'_c'+str(i),self.cindex[i])
    
    def set_format(self):
        rs = self.tb.find_all('tr')
        for i in range(len(self.row_format)):
            a = self.row_format[i].split('||')
            try:
                if a[0]:self.add_style(a[0],i)
            except Exception as e :print(e)
            try:
                if a[1]:self.add_style(a[1],i,0)
            except:pass
            try:
                if a[2]:
                    for j in rs[i].find_all('td'):
                        try: j.string = a[2].format(float(j.string))
                        except:pass
            except:pass
            
    def _set_format(self,row,col,func):
        a = self.tb.find(id=self.tid+'_r'+str(row)+'_c'+str(col))
        try:a.string = func(float(a.string))
        except:pass
    
    def replace_string(self,tagid,new_string):
        self.tb.find(id=tagid).string = str(new_string)
    
    def add_style(self,style,row='',col=''):
        row = str(row)
        col = str(col)
        if row and col:
            self.tb.find(id=self.tid+'_r'+row+'_c'+col)['style'] = style
        elif row:
            self.styles += '\n  .'+self.tid+'_r'+row+' {'+style+'}'
        elif col:
            self.styles += '\n  .'+self.tid+'_c'+col+' {'+style+'}'
        else: raise ValueError('请确定位置!')
    
    def add_property(self,ppt,value,row,col):
        self.tb.find(id=self.tid+'_r'+str(row)+'_c'+str(col))[ppt] = value
    
    def change_value(self,value,row,col):
        self.tb.find(id=self.tid+'_r'+str(row)+'_c'+str(col)).string = value
    
    def add_rows(self,rows,location,how='append',insert=0):
        for row in rows:
            tg = tobs('<tr><th></th>'+'<td></td>'*(len(row)-1)+'</tr>')
            for i in range(len(tg.contents)):
                tg.contents[i].string = row[i]
            if how!='insert':
                location.append(tg)
            else:
                location.insert(insert,tg)
                insert += 1
        self.set_id()

    def del_cell(self,row,col):
        return self.tb.find(id=self.tid+'_r'+str(row)+'_c'+str(col)).extract()