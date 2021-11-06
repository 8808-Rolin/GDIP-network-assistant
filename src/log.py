'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-11-06 17:21:46
LastEditors: Rolin
Code-Function-What do you want to do: logging 工具类
'''
import logging
import os
import random
import time
import tkinter as tk

class log:
    # 日志名称生成
    _time_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


    if not os.path.exists("config"):
        os.mkdir("config")
        if not os.path.exists("config\\log"):
            os.mkdir("config\\log")
    # 生成日志
    _logger = logging.getLogger()
    _logger.setLevel(logging.NOTSET)
    _fileHandeler = logging.FileHandler(
        'config\\log\\Log-{}.log'.format(_time_name), mode='w', encoding='UTF-8')
    _fileHandeler.setLevel(logging.NOTSET)
    _formatter = logging.Formatter(
        '[%(asctime)s]:[%(levelname)s]:[%(message)s]')
    _fileHandeler.setFormatter(_formatter)
    _logger.addHandler(_fileHandeler)

    text = None

    def __init__(self,text):
        self.text = text
    
    def addText(self, message):
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        message = localtime+"->"+message + "\n"
        self.text.configure(state='normal')
        self.text.insert(tk.END, message)
        self.text.configure(state='disabled')

    # debug信息 输出日志
    def debug(self, message):
        self._logger.debug(message)

    # info信息，输出日志与屏幕
    def info(self, message):
        self._logger.info(message)
        self.addText(message)

    # warn 信息，输出日志与屏幕
    def war(self, message):
        self._logger.warn(message)
        self.addText(message)
    
    #error 信息，输出日志
    def error(self, message):
        self._logger.error(message)

    # cri信息 输出日志
    def cri(self, message):
        self._logger.critical(message)
    
    #show 信息，仅展示到屏幕
    def show(self,message):
        self.addText(message)

    

