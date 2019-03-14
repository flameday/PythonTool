#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import os
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # pie(x, explode=None, labels=None,
    #     colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'),
    #     autopct=None, pctdistance=0.6, shadow=False,
    #     labeldistance=1.1, startangle=None, radius=None)
    #t=[0, 0, 0, 19, 58, 226, 330, 360, 615, 2227, 4250, 4447, 16044, 83990]
    t=[0, 0, 0, 19, 58, 226, 330, 360, 615, 2227, 4250, 4447]#, 16044]#, 83990]
    plt.pie(t)
    plt.show()
