'''
@Author: WangGuanran
@Email: wangguanran@vanzotec.com
@Date: 2020-02-16 00:35:02
@LastEditTime: 2020-02-16 00:35:03
@LastEditors: WangGuanran
@Description: common py file
@FilePath: \vprojects\scripts\common.py
'''
import os
import time

def _get_filename(preffix, suffix, path):
    '''
    根据时间获取动态文件名
    '''
    if(not os.path.exists(path)):
        os.makedirs(path)
    date_str = time.strftime('%Y%m%d_%H%M%S')
    return os.path.join(path, ''.join((preffix, date_str, suffix)))