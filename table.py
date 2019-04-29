# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:46:50 2019

@author: r00386
"""
from .auxiliary_func import bs, tobs, bs4

class Table():
    def __init__(self,tid, df, rindex=None, cindex=None): #之后升级多层表头和df多层索引的情况
        self.tb = bs(df.to_html()).table
        self.shape = [df.shape[0]+1,df.shape[1]+1]
        self.rindex = rindex
        self.cindex = cindex
        self.tid = tid
        self.set_id()
        self.set_index()
    
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
        
    def replace_string(self,tagid,new_string):
        self.tb.find(id=tagid).string = new_string
    
    def add_style(self,style,row=None,col=None):
        row = str(row)
        col = str(col)
        if row and col:
            self.tb.find(id=self.tid+'_r'+row+'_c'+col)['style'] = style
            return '\n'
        elif row:
            return '\n  .'+self.tid+'_r'+row+' {'+style+'}'
        elif col:
            return '\n  .'+self.tid+'_c'+col+' {'+style+'}'
        else: raise ValueError('请确定位置!')
    
    def add_property(self,ppt,value,row,col):
        self.tb.find(id=self.tid+'_r'+str(row)+'_c'+str(col))[ppt] = value
    
    def add_row(self,rows,location,how='append',insert=0):
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