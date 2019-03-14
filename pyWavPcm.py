#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import numpy
import pyLog

def caculateSize(buffer):
    if len(buffer) > 4:
        pyLog.logging.error('warnning: size buffer is not 4')
        sys.exit(0)
        
    total_size = 0
    for i in range(len(buffer)):
        hex = buffer[i]
        #pyLog.logging.info('hex= %d'%hex)
        #print ('hex= ', hex, 'i= ', i)
        val = hex * (256**i)
        #print ('===val=%d * %d = %d'%(val, 256**i, val))
        total_size += val
        #print ('val= %d,total size= %d, hex= %d\n'%(val, total_size, hex))
    return total_size

def wav2Pcm(wav_file):
    wav_file_size = os.path.getsize(wav_file)

    fr = open(wav_file, 'rb')
    wav_header_length = 0

    #########################RIFF WAV Chunk
    chunk = fr.read(12)
    ###RIFF
    pyLog.logging.info('riff_header: %s'%chunk[0:4])

    ###Size总大小
    total_size = caculateSize(chunk[4:8])
    pyLog.logging.info('riff_header, total_size= %d, wav_file_size= %d'%(total_size, wav_file_size))
    
    if total_size + 8 != wav_file_size:
        pyLog.logging.error('error: read bad content! (total_size + 8 != wav_file_size); diff = %d'%(wav_file_size - total_size))
        #sys.exit(0)
    ###WAVE
    pyLog.logging.info('riff_header: %s'%chunk[8:12])

    wav_header_length += 12
    pyLog.logging.info("wav_header_length= %d"%(wav_header_length))
    #########################Format Chunk
    chunk = fr.read(24)
    append_format = ''
    ###fmt' '
    pyLog.logging.info('format_chunk:%s'%chunk[0:4])
    
    ###size
    format_chunk_size = caculateSize(chunk[4:8])
    pyLog.logging.info('format_chunk, format_chunk_size=%d'%format_chunk_size)
    
    pyLog.logging.info('FormatTag= %d'%caculateSize(chunk[8:10])) 
    pyLog.logging.info('Channels= %d'%caculateSize(chunk[10:12])) 
    pyLog.logging.info('SamplesPerSec= %d'%caculateSize(chunk[12:16])) 
    pyLog.logging.info('AvgBytesPerSec= %d'%caculateSize(chunk[16:20])) 
    avgBytesPerSec = caculateSize(chunk[16:20])

    pyLog.logging.info('BlockAlign= %d'%caculateSize(chunk[20:22])) 
    pyLog.logging.info('BitsPerSample= %d'%caculateSize(chunk[22:24])) 
    bitsPerSample = caculateSize(chunk[22:24])
    
    diff = format_chunk_size - 16
    if diff != 0:
        pyLog.logging.error('warnning append_format is not 0')
    append_format = fr.read(diff)

    wav_header_length += 8
    wav_header_length += 16
    wav_header_length += diff
    pyLog.logging.info("wav_header_length= %d"%(wav_header_length))
    #########################下面是否有FactChunk？这里需要判断下，以免出错
    chunk = fr.read(8)
    text = chunk[0:4].decode('ascii')
    if text != 'data':
        #########################Fact Chunk
        ###目前采用wav录音的iphone软件,这里字段是FLLR
        #chunk = fr.read(8)
        ###FLLR
        pyLog.logging.info('fact_chunk:%s'%chunk[0:4])
        fact_chunk_size = caculateSize(chunk[4:8])
        pyLog.logging.info('fact_chunk, size=%s'%fact_chunk_size)
        chunk = fr.read(fact_chunk_size)

        wav_header_length += 8
        wav_header_length += fact_chunk_size      
        pyLog.logging.info("wav_header_length= %d"%(wav_header_length))

        ###这里刷新数据，为data模块读入数据
        chunk = fr.read(8)

    #########################Data Chunk
    ###data
    #chunk = fr.read(8)
    pyLog.logging.info('data chunk, chunk=%s'%chunk[0:4])
    data_chunk_size = caculateSize(chunk[4:8])
    pyLog.logging.info('data chunk, data_chunk_size=%s'%data_chunk_size)
    ###接下来都是数据
    
    ###############
    wav_header_length += 8        
    pyLog.logging.info("wav_header_length= %d"%(wav_header_length))
    ###接下来把文件写为pcm格式
    pyLog.logging.info("wav_file_size= %d, wav_header_length= %d"%(wav_file_size, wav_header_length))
    pcm = fr.read(wav_file_size - wav_header_length)
    pyLog.logging.info('wav_header_length= %d*16 + %d'%(wav_header_length/16, wav_header_length%16))
    
    return pcm, wav_file_size, avgBytesPerSec, bitsPerSample#[:16*5]
 
def genWavHeader(pcm_size, bitrate = 16000, channels = 1, trunk = 2):
    pyLog.logging.info('')
    pyLog.logging.info('pcm_size= %d'%pcm_size)
    res = b''
    ###| ID    |  4 Bytes |   'RIFF'    |
    res += struct.pack('4s', b'RIFF')###不加4的话,就只会写入一个R,没有IFF
    pyLog.logging.info(res.decode('ascii'))
    ###| Size  |  4 Bytes |             |
    res += struct.pack('i', pcm_size + 44 - 8)
    pyLog.logging.info('pcm_size+44-8= %d'%(pcm_size+44-8))
    
    ###数据29dc 0600 意思是: 06 * 16^3 + dc *16 ^2 + 29
    #res += struct.pack('i', 16*16*16*16 *(1*16*16*16 + 2*16*16 + 3*16 + 4) + 5*16*16*16 + 6*16*16 + 7*16 + 8)
    ###| Type  |  4 Bytes |   'WAVE'    |
    res += struct.pack('4s', b'WAVE')###不加4的话,就只会写入一个R,没有IFF
    pyLog.logging.info('Type= %s'%(b'WAVE'.decode('ascii')))
    ###| ID            |  4 Bytes  |   'fmt ' 
    res += struct.pack('4s', b'fmt ')###不加4的话,就只会写入一个R,没有IFF
    pyLog.logging.info(b'fmt '.decode('ascii'))
    ###| Size          |  4 Bytes  | 数值为16或18，18则最后又附加信息
    res += struct.pack('i', 16)
    pyLog.logging.info('Size= 16')
    ###| FormatTag     |  2 Bytes  | 编码方式，一般为0x0001   
    res += struct.pack('h', 1)
    pyLog.logging.info('FormatTag= 1')
    ###|Channels      |  2 Bytes  | 声道数目，1--单声道；2--双声道 
    res += struct.pack('h', channels)
    pyLog.logging.info('Channels= %d'%channels)
    ###|SamplesPerSec |  4 Bytes  | 采样频率
    res += struct.pack('i', bitrate)
    pyLog.logging.info('SamplesPerSec= %d'%bitrate)
    ###|AvgBytesPerSec|  4 Bytes  | 每秒所需字节数                       |     |===> WAVE_FORMAT
    res += struct.pack('i', bitrate*trunk)
    pyLog.logging.info('AvgBytesPerSec= %d'%(bitrate*trunk))
    ###|BlockAlign    |  2 Bytes  | 数据块对齐单位(每个采样需要的字节数) |     |
    res += struct.pack('h', trunk)
    pyLog.logging.info('BlockAlign= %d'%(trunk))
    ###|BitsPerSample |  2 Bytes  | 每个采样需要的bit数                  |     |
    res += struct.pack('h', channels*trunk*8)
    pyLog.logging.info('BitsPerSample= %d'%(channels*trunk*8))
    ###|ID    |  4 Bytes |   'data'    |
    res += struct.pack('4s', b'data')
    pyLog.logging.info('ID= %s'%(b'data'.decode('ascii')))
    ###|Size  |  4 Bytes |             |
    res += struct.pack('i', pcm_size)
    pyLog.logging.info('Size= %d'%pcm_size)

    return res
    
def saveWavFile(pcm, file_name, bitrate = 16000, channels = 1, trunk = 2):
    header = genWavHeader(len(pcm), bitrate, channels, trunk)    
    file = open(file_name, 'wb')
    file.write(header)
    file.write(pcm)
    file.close()

###注意:buf是pcm的数据
###chunk_size是一个数据点的大小字节(一般为2)
###dst_size是多少个"点"
###height是振幅的缩放比例
def getPcmValueList(buf, chunk_size, dst_length, height = 1):
    val_list = []
    
    rate = dst_length/(len(buf) / chunk_size)
    
    for i in range(dst_length):
        orig_index = i / rate;

        pre_ind = int(orig_index)
        beg = chunk_size*pre_ind
        #pre_val = caculateSize(buf[beg:beg + 2])
        pre_val  = struct.unpack('h', buf[beg:beg + 2])[0]
#         print('pre_val= ', pre_val)
        
        post_ind = pre_ind + 1
        beg = chunk_size*post_ind
        #post_val = caculateSize(buf[beg:beg + 2])#
        if beg >= len(buf) -2:
            break
        post_val = struct.unpack('h', buf[beg:beg + 2])[0]

        pre_diff = orig_index - pre_ind
        post_diff = post_ind - orig_index
        #print('pre_diff= ', pre_diff, 'post_diff= ', post_diff)
        val = pre_val * post_diff + post_val * pre_diff;
        val *= height
        #print('val= ', val)        
        
        val = int(val)
        if val < -32768:
            print('val= ', val)
            val = -32768
        if val > 32767:
            print('val= ', val)
            val = 32767
#         pyLog.logging.info('rate= %f,i= %d, orig= %f, val=%d, pre_ind= %d, post_ind= %d)'%\
#                 (rate, i, orig_index, val, pre_ind, post_ind))
        val_list.append(val)
    #saveWavFile(buf, 'buf.wav')
    #saveWavFile(res_buf, 'buf_scaled2.wav')
    return val_list
    
def pcmValueList(buf, channels, chunk_size):
    res_list = []
    
    dict_unpack_ch = {2:'h', 
                      4:'i',}
                      
    format = dict_unpack_ch[chunk_size]
    big_sample = chunk_size * channels
    ind_list = range( len(buf)//big_sample )
    
    for i in ind_list:
        beg = big_sample * i 
        end = big_sample * (i + 1)
        if channels == 1:
            val  = struct.unpack(format, buf[beg:end])[0]
            res_list.append(val)
        if channels == 2:
            data_buf = buf[beg:end]
            ###第一块
            val    = struct.unpack(format, data_buf[:chunk_size])[0]
            ###第二块
            val02  = struct.unpack(format, data_buf[chunk_size:])[0]
            val = (val, val02)
            res_list.append(val)
    
    return res_list
        
def expandValueList(value_list, dst_length, height = 1):
    res_list = []
    rate = dst_length/len(value_list)
    
    for i in range(dst_length):
        orig_index = i / rate;
        pre_ind = int(orig_index)
        post_ind = pre_ind + 1
        #print(get_cur_info(), 'i= ', i, 'pre_ind= ', pre_ind, 'post_ind= ', post_ind)
        
        pre_val = 0
        post_val = 0
        if pre_ind < len(value_list) and post_ind < len(value_list):
            pre_val = value_list[pre_ind]
            post_val = value_list[post_ind]
        elif pre_ind < len(value_list) and post_ind >= len(value_list):
            ###根据前面2个点,线性估算下一个点的值()
            if len(value_list) < 2:
                pre_val = value_list[pre_ind]
                post_val = value_list[pre_ind]
            else:
                pre_val = value_list[pre_ind]
                post_val = 2 * value_list[pre_ind] - value_list[pre_ind - 1]
        else:
            print(get_cur_info(), 'error! bad index')
            sys.exit(0)
        
        pre_diff = orig_index - pre_ind
        post_diff = post_ind - orig_index
        
        val = 0
        val =  pre_val * post_diff
        val += post_val * pre_diff
            
        val *= height
        res_list.append(val)
    return res_list

def valueList2pcm(value_list, trunk_size = 2, channels = 1):
    res_buf = b''
    
    dict_unpack_ch = {2:'h', 
                      4:'i',}
    format = dict_unpack_ch[trunk_size]
                      
    if channels == 1:
        for val in value_list:
            val = int(val)
            if abs(val) >= 32767:
                print('val= ', val)
            res_buf += struct.pack(format,val)
    elif channels == 2:
#         ###对齐字节
#         align_size = trunk_size * channels * 8
#         dst_size = len(value_list)
#         dst_size = (dst_size + align_size - 1)
#         dst_size = dst_size//align_size
#         dst_size = dst_size * align_size 
#         for i in range(dst_size - len(value_list)):
#             value_list.append((0, 0))
        for left, right in value_list:
            left = int(left)
            right = int(right)
            res_buf += struct.pack(format,left)
            res_buf += struct.pack(format,right)
        
    return res_buf

def scaleValueBuff(buf, chunk_size, dst_size, height = 1):
    value_list = getPcmValueList(buf, chunk_size, dst_size, height)
    res_buf = valueList2pcm(value_list)
    return res_buf

def realImag2ComplexList(r_list, i_list):
    print(numpy.vectorize(complex)(5, 7))
    
    res_list = []
    for i,r in enumerate(r_list):
        t = (r, i_list[i])
        res_list.append(t)
    #print(res_list)
    
    t_list = []
    for i, e in enumerate(res_list):
        #print(e)
        t = (numpy.vectorize(complex)(e[0], e[1]))
        #print(t)
        t_list.append(t)
    
    #d = numpy.array(t_list, dtype=complex )
    return t_list
    
def alignPcmLength(pcm_list):
    double_v_list = []
    ###pcm转到频域处理
    for i,pcm in enumerate(pcm_list):
        val_list = pcmValueList(pcm, 2)
        fft_list = numpy.fft.rfft(val_list)/len(val_list)
        #print(get_cur_info(), 'len(fft_list)= ', len(fft_list))
        r_list = [numpy.real(e) for e in fft_list]
        i_list = [numpy.imag(e) for e in fft_list]
        double_v_list.append((r_list, i_list))

    ###设置缩放大小:按最大的进行align
    size_list = [len(e[0]) for e in double_v_list]
    min_len,_ = minMaxValue(size_list)
    #max_len = averageValue(size_list)
    min_len = int(min_len/2)
    #print(get_cur_info(), 'min_len= ', min_len, 'size_list= ', size_list)

    new_pcm_list = []
    ###缩放并生成wav
    for i, (r_list, i_list) in enumerate(double_v_list):
        file_name = 'fft_expanded.new_%d.wav'%i
        r2_list = expandValueList(r_list, min_len)
        i2_list = expandValueList(i_list, min_len)

        tmp_list = realImag2ComplexList(r2_list, i2_list)
        y01=numpy.fft.irfft(tmp_list)
        #print(get_cur_info(), 'len(y01)= ', len(y01))
        #print(get_cur_info(), 'tmp_list[:50]= ', tmp_list[:50])
        #print(get_cur_info(), 'y01[:50]= ', y01[:50])
        y01 = [min_len * e * 1.5 for e in y01]
        for i,e in enumerate(y01):
            if e > 65535//2:
                y01[i] = 65535//2
            if e < -65535//2:
                y01[i] = 65535//2
        pcm = valueList2pcm(y01)
        new_pcm_list.append(pcm)
    return new_pcm_list
    
def sampleValue(value_list, source_rate, dst_rate):
    if dst_rate > source_rate:
        print(get_cur_info(), 'error to sample!')
        sys.exit(0)
    step = source_rate / dst_rate
    ###原来有n个,现在是n/step个
    cnt = len(value_list) / step
    cnt = int(cnt)
    
    res_list = []
    for i in range(cnt):
        pos = step * i;
        x0 = int(pos)
        x1 = x0 + 1
        d0 = pos - x0
        d1 = x1 - pos
        v = value_list[x0] * d1 + value_list[x1] * d0
        res_list.append(v)
    return res_list    
        
if __name__ == '__main__':
#     ###初始化log信息
#     logFilename = "crifan_logging_demo.log";
#     initLogging(logFilename);

    t = range(10)
    r = sampleValue(t, 20, 10)
    print(r)
    sys.exit(0)
    
    dir = '/Users/daiqiang/EnglishPronunciation/SepNode_task/TraingText2FrontendInput/old.10月14日/14zh_ques/'
    file = dir + '140200.wav'
    pcm, wav_file_size, avgBytesPerSec, bitsPerSample = wav2Pcm(file)
    val_list = pcmValueList(pcm, 4, 2)
    print(val_list[:10])
    

    ###目前是16K的处理
    #res = genWavHeader()
    #print (res)#.decode('utf8'))
    file = '/Users/daiqiang/EnglishPronunciation/SepNode_task/TraingText2FrontendInput/old.8月27日/wav/'
    file += '00021000.wav'
    pcm, wav_file_size, avgBytesPerSec, bitsPerSample = wav2Pcm(file)
    
    saveWavFile(pcm, 'wav2pcm2wav01.wav')
    
    
    val_list = pcmValueList(pcm, 2)
    pcm02 = valueList2pcm(val_list)
    saveWavFile(pcm02, 'wav2pcm2wav02.wav')

# 
#         
#     old_len = len(pcm)
#     cur_len = int(old_len/3*2)
#     pcm = pcm[:cur_len]
# 
#     saveWavFile(pcm, 'wav2pcm2wav.wav')
