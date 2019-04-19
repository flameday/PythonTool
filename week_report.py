#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import subprocess
import time
import datetime
from datetime import datetime,date

def show_report():
    applescript = """
    display dialog "该写周报了..." ¬
    with title "This is a pop-up window" ¬
    with icon caution ¬
    buttons {"OK"}
    """
    subprocess.call("osascript -e '{}'".format(applescript), shell=True)

### 采用 nohup 启动，每周五都会自动提醒2次发周报
for i in range(100000):
    ### 判断今天是否星期五
    dayOfWeek = datetime.now().weekday() + 1
    if dayOfWeek == 5:
        for i in range(2):
            show_report()
    time.sleep(3600*3)
