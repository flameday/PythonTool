#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import os

# if not isPlatform3():
#     ###需要安装windows下的pdfminer库，mac下没有
#     from pdfminer.pdfparser import PDFParser, PDFDocument  
#     from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  
#     from pdfminer.pdfdevice import PDFDevice  
#     from pdfminer.converter import PDFPageAggregator  
#     from pdfminer.layout import *

def getPdfPages(pdf_name):
    fp = open(pdf_name, 'rb')
    #用文件对象来创建一个pdf文档分析器  
    parser = PDFParser(fp)  
    # 创建一个  PDF 文档   
    doc = PDFDocument()  
    # 连接分析器 与文档对象  
    parser.set_document(doc)  
    doc.set_parser(parser)  
    
    # 提供初始化密码  
    # 如果没有密码 就创建一个空的字符串  
    doc.initialize()  
    # 检测文档是否提供txt转换，不提供就忽略  
    if not doc.is_extractable:  
        #raise PDFTextExtractionNotAllowed  
        logging.info('=========not txt change %s'%pdf_name)
        return False

    logging.info('-----processing: %s'%pdf_name)
    # 创建PDf 资源管理器 来管理共享资源  
    rsrcmgr = PDFResourceManager()  
    # 创建一个PDF设备对象  
    laparams = LAParams()  
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)  
    interpreter = PDFPageInterpreter(rsrcmgr, device)  
    # 处理文档对象中每一页的内容  
    # doc.get_pages() 获取page列表  
    # 循环遍历列表，每次处理一个page的内容  
    # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括
    ###LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
    pages = doc.get_pages()  
    return pages
        
def isPdfValid(pdf_name):
    if pdf_name[-4:].lower() != '.pdf':
        logging.info('-------------------not pdf file: %s'%pdf_name)
        return False
        
    try:
        getPdfPages(pdf_name)
    except:
        return False
        pass###错误后继续
    return True

###注意:这里是多进程在跑,即使挂掉了也没有关系     
def parsePdfFile(pdf_name):
    all_text = ''
    if pdf_name[-4:].lower() != '.pdf':
        logging.info('-------------------not pdf file:%s'%pdf_name)
        return all_text

    #try:
    if True:
        pdf_pages = getPdfPages(pdf_name)
        for i, page in enumerate(pdf_pages):  
            interpreter.process_page(page)  
            layout = device.get_result()  
            for x in layout:  
                if isinstance(x, LTTextBox) or isinstance(x, LTTextLine):
                    all_text += x.get_text()
                    all_text += ' '
        fp.close()
        device.close()
#     except:
#         print 'error happens somewhere!'
#         pass###错误后继续
#     print 'all_text len= ',len(all_text)

    return all_text

