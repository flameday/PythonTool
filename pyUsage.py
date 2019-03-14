#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import os,sys,signal,platform,subprocess,re
import pyLog
import pyUsage

def usage(strText, argc = 1):
    def showUsage(s):
        text = '\n==================================================\n'
        text += s
        text += '\n==================================================\n'
        pyLog.logging.info(text)
        
    if len(sys.argv) < argc:
        #print(strText)
        showUsage(strText)
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        showUsage(strText)
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == '-help':
        showUsage(strText)
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1][:2] == '--':
        showUsage(strText)
        sys.exit(0)


def handler(signum, frame):
    system_type = platform.platform()
    
    ###针对Windows系统，需要特殊处理下，因为ps -ef 没法执行
    if system_type.find('Windows') != -1:
        sys.exit(0)
        
    ###current_file = os.path.realpath(__file__)
    ####注意:__file__结果是本文件common_function,而不是调用着的文件
    current_file = os.path.realpath(sys.argv[0])
    pos = current_file.rfind(os.sep)
    current_file = current_file[pos + 1:]

    p1 = subprocess.Popen(['ps', '-ef'],stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', current_file],stdin=p1.stdout,stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['awk', '{print $2}'],stdin=p2.stdout,stdout=subprocess.PIPE)
    t = p3.stdout.readlines()
    if len(t) > 0:
        p4 = subprocess.Popen(['kill', '-9', t[0].strip()])

###这个函数用来操作Ctrl+C的命令
def setHandler():
    signal.signal(signal.SIGINT,handler)
    signal.signal(signal.SIGTERM,handler)
    signal.signal(signal.SIGABRT,handler)

def PrintObjectInfo(object, spacing=10, collapse=1):   
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    text = "\n".join(["      %s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])
    pyLog.logging.info(text)

def isPlatform3():
    ver = platform.python_version()
    if re.match('2.7', ver):
        return False
    return True

def get_cur_info(isShowFile = False):
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back

    file = ''
    if isShowFile:
        file = os.path.split(f.f_code.co_filename)[-1]
    return (file, f.f_code.co_name, f.f_lineno)    
