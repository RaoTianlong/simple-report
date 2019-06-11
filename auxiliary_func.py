# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:00:17 2019

@author: r00386
"""
#%% 函数
from bs4 import BeautifulSoup as bs
import bs4
def tobs(contents):
    a = [i for i in bs('<div>'+contents+'</div>').div.contents if isinstance(i,bs4.element.Tag)]
    return a[0]


#%% 模板
default_template = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>报表模板</title>
<link href="https://ums.smyoa.com/js/smy.ums.report.css" rel="stylesheet" type="text/css"/>
<script src="https://ums.smyoa.com/js/jquery-1.2.3.min.js"></script>
<script src="https://ums.smyoa.com/js/smy.ums.report.js"></script>
</head>
<body>
</body>
</html>
"""

