'''
@Author: WangGuanran
@Email: wangguanran@vanzotec.com
@Date: 2020-02-15 13:33:21
@LastEditTime: 2020-02-19 18:14:18
@LastEditors: WangGuanran
@Description: Operate database py file
@FilePath: \vprojects\vprjcore\operate_database.py
'''
from vprjcore.log import log


class OperateDatabase(object):
    '''
    数据库操作类
    '''
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        log.debug("Operate_Database Im In")


if __name__ == "__main__":
    pass