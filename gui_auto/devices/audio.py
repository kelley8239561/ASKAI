import base64
import os
import sounddevice
import soundfile
import numpy
import wave
import threading
import time,psutil

"""
_summary_
mic and speaker control which can be used by the assistant

"""

class AudioService():
    
    # 采样率
    __samplerate:int
    # 声道1 or 2
    __channels:int
    # 声音存储格式
    __dtype:str
    # inputstream结果存储
    inputStreamResult:numpy.ndarray
    tempStreamResult:numpy.ndarray
    # inputstream结果列表存储
    inputStreamResultList = []
    # recFlag是存放开始录制时间和停止录制时间的列表
    recFlag = []    
    # 流开始符：用于外部控制stream可以停止，初始False
    streamStart = False
    # 流暂停符：用于外部控制已经开始的stream停止，初始False
    streamStop = False
    # 流结束符
    streamQuit = False
    
    # initial
    def __init__(
            self,
            samplerate=16000,
            channels=1,
            dtype='int16',  
        ):
        #self.__frames = samplerate#录音帧数。一帧对应于所有通道的单个样本集合。例如，若要录制5秒的音频，并且采样率（samplerate）是44100，那么frames将是5*44100。
        self.__samplerate = samplerate  #采样率，以赫兹（Hz）为单位。这是每秒钟捕获和播放的样本数。常见的采样率包括44100（CD质量）、48000（专业音频设备）等。
        self.__channels = channels  #录制的通道数。单声道为1，立体声为2。
        self.__dtype = dtype  #指定录制数据的数据类型。常用类型包括'float32'和'int16'。'float32'将样本值范围规范化为从-1.0到+1.0，而'int16'是16位整型，表示的范围则是-32768到+32767。
        #out  #可选。输出的NumPy数组。如果指定了out参数，则将在该数组中放置录制的音频数据，否则内部会创建一个新数组。
        #mapping  #可选。这是一个指定哪些通道（从1开始编号）实际用于录音的序列。通常情况下，默认的设备所有通道都会被使用。（此参数并未在原文的注释中提到，但在函数API中存在。）
        #blocking  #可选。默认值为False。如果设置为True，函数调用将阻塞，直到录制完成。否则，它会立即返回，并且需要外部逻辑来确保录制完成，通常是通过sounddevice.wait()函数。
        #**kwargs  #其他一些可选的关键字参数，可能在未来版本的sounddevice模块中添加。
        #blocksize # (可选)块大小，定义了传递给 stream 回调函数的帧数。 0 表示使用主机 API 的最佳块大小。如果未指定，默认使用 sounddevice.default.blocksize 的设置。
        #device #(可选): 设备索引或查询字符串，指定要使用的音频输入设备。如果未指定，默认从 sounddevice.default.device 中获取输入设备的设置。
        #latency #(可选): 延迟，以秒为单位，表示流的期望延迟时间。值可以是具体的延迟时间，或字符串 'low' 和 'high'，分别代表设备的默认低延迟和高延迟配置。如果未指定，默认使用 sounddevice.default.latency 中的输入设备延迟。
        #extra_settings #(可选): 特定于主机 API 的额外设置，例如使用 ASIO 驱动时可指定的额外设置如 sounddevice.AsioSettings。
        #callback #(可选): 用户提供的回调函数，用于在流活动期间处理音频数据。回调函数接收几个参数：输入数据、帧数、时间信息以及状态，它必须返回 None。
        #finished_callback #(可选): 用户提供的回调函数，当流变为非活动状态时调用。例如，可以用于清理在录音过程中使用的资源。
        #clip_off #(可选): 布尔值，如果设置为 True，将关闭默认的剪裁功能，否则超出范围的样本将被剪裁为有效的最大/最小值。
        #dither_off #(可选): 布尔值，如果设置为 True，将关闭默认的抖动功能。
        #never_drop_input #(可选): 布尔值，对于全双工流，将此项设为 True 可以保证不会丢弃溢出的输入样本。
        #prime_output_buffers_using_stream_callback #(可选): 布尔值，如果设为 True，流的输出缓冲区会在开始时使用回调函数来填充，而不是默认的零填充。
        #inputStream临时存放
        self.inputStreamResult = numpy.empty((0,channels),dtype=dtype)
        self.tempStreamResult = numpy.empty((0,channels),dtype=dtype)
        return
        
    # 给定固定duration进行流录制
    def recStreamByDuration(self,duration):
        #清空inputStream的临时存放
        global inputStreamResult
        inputStreamResult = numpy.empty((0,self.__channels),dtype='float64')
        #print(inputStreamResult)
        # 回调函数处理录音数据
        def inputStreamCallback(indata, frames, time, status):
            #print("Start callback")
            global inputStreamResult
            inputStreamResult = numpy.concatenate((inputStreamResult,indata),axis=0)
        # 创建 InputStream 对象
        stream = sounddevice.InputStream(
                                         callback = inputStreamCallback,
                                         samplerate = self.__samplerate,
                                         #dtype = self.__dtype,
                                         channels = self.__channels,
                                         
                                         )

        # 开始录音
        with stream:
            print("start")
            sounddevice.sleep(duration)  # 录音 1 秒钟
        
        #写入wav文件方便测试
        self.audioStreamToWav(inputStreamResult,'last record')
        return inputStreamResult
    
    # 外部控制recStop进行流录制，每次启动和暂停中止流
    def recStreamByRecStop(self):
        
        #录音最小粒度，默认是0.5s
        stepLenth = 0.5
        #录制花费的粒度数量
        stepNum = 0
        # 回调函数处理录音数据
        def inputStreamCallback(indata, frames, time, status):
            #print("Start callback")
            self.inputStreamResult = numpy.concatenate((self.inputStreamResult,indata),axis=0)
        # 创建 InputStream 对象
        print("check start")
        while not self.streamQuit:
            #print("not quit")
            while self.streamStart:
                stream = sounddevice.InputStream(
                                                callback=inputStreamCallback,
                                                samplerate=self.__samplerate,
                                                #dtype=self.__dtype,
                                                channels=self.__channels,
                                                )
                with stream:
                    print('stream start')         
                    while not self.streamStop:
                        stepNum = stepNum + 1
                        sounddevice.sleep(int(stepLenth*1000))
                    
                self.audioStreamToWav(self.inputStreamResult,'last record'+time.strftime('%H%M%S',time.localtime()))
                self.inputStreamResult = numpy.empty((0,self.__channels),dtype=self.__dtype)
        return
    
    # 外部控制recStop进行流录制，流启动后持续，每次启动和暂停进行截取
    def recStreamByRecStopCut(self):
        """
        _summary_
            
        Returns:
            _type_: _description_
        """
        # 录音最小粒度，默认是0.5s
        stepLenth = 0.5
        # 录制花费的粒度数量
        stepNum = 0
        
        # 回调函数处理录音数据
        def inputStreamCallback(indata, frames, time, status):
            #print("callback:stream")
            self.inputStreamResult = numpy.concatenate((self.inputStreamResult,indata),axis=0)
         
        # 监控开始录制、停止录制、流结束的事件时间
        def recControl():
            print("callback:recControlThread")
            # 清空存放开始录制时间和停止录制时间的列表
            self.recFlag = []
            # 开始记录的时间，用来校准和流录制时间的差别
            recTime = time.time()
            print('rec start at',recTime)
            # 保存每次的开始录制时间和停止录制时间
            streamStartTime, streamStopTime = float(0),float(0)
            # 保存每次的开始录制和停止录制时inputStreamResult的长度
            streamStartIndex, streamStopIndex = -1,-1
            while not self.streamQuit:
                streamStartTime, streamStopTime = float(0),float(0)
                streamStartIndex = self.inputStreamResult.shape[0]
                streamStopIndex = -1
                while self.streamStart:
                    streamStartTime = time.time()
                    while not self.streamStop:
                        streamStopTime = time.time()
                        streamStopIndex = self.inputStreamResult.shape[0]
                #if(streamStartTime-streamStopTime) != 0:
                #    self.recFlag.append([streamStartTime,streamStopTime])
                # 有开始记录和结束记录事件，则讲一次记录存储到inputStreamResultList中
                if((streamStartIndex-streamStopIndex) != 0) and (streamStopIndex != -1):
                    self.recFlag.append([streamStartIndex,streamStopIndex])
                    tempResult = self.inputStreamResult[streamStartIndex : streamStopIndex]
                    print(streamStartIndex,streamStopIndex,streamStopIndex-streamStartIndex)
                    self.inputStreamResultList.append(tempResult)
                    self.audioStreamToWav(tempResult,time.strftime('%H%M%S',time.localtime())+' part')
                    self.audioStreamToPCM(tempResult,time.strftime('%H%M%S',time.localtime())+' part')
            self.inputStreamResultList.append(self.inputStreamResult)
            return
        
        #开启新线程，监控开始录制、停止录制、流结束的事件时间
        recControlThread = threading.Thread(target=recControl,args=())
        recControlThread.start()
        
        # 创建 InputStream 对象
        stream = sounddevice.InputStream(
                                        dtype=self.__dtype,
                                        callback=inputStreamCallback,
                                        samplerate=self.__samplerate,
                                        channels=self.__channels,
                                        )
        # 流开始
        with stream:
            streamTime = time.time()
            print('stream start at',streamTime)         
            while not self.streamQuit:
                stepNum = stepNum + 1
                sounddevice.sleep(int(stepLenth*1000))
        streamCloseTime = time.time()
        recControlThread.join()
            
        self.audioStreamToWav(self.inputStreamResult,time.strftime('%H%M%S',time.localtime())+' All')
        self.audioStreamToPCM(self.inputStreamResult,time.strftime('%H%M%S',time.localtime())+' All')
        #"""
        #记录状态调试
        print(self.recFlag.__len__())
        print(streamTime,streamCloseTime,streamCloseTime-streamTime)
        print(self.inputStreamResult.shape[0],(streamCloseTime-streamTime)*self.__samplerate)
        print(self.inputStreamResult.shape[0] - (streamCloseTime-streamTime)*self.__samplerate)
        print(self.inputStreamResult.shape[0] / ((streamCloseTime-streamTime)*self.__samplerate))
        #"""
        # 每个分段的情况
        for result in self.inputStreamResultList:
            print("rec分段情况",result.shape[0])
        return self.inputStreamResultList
    
    # 持续记录流
    def recStream(self,stepLenth=0.5):
        # 录音最小粒度0.5s
        tempStepLenth = stepLenth
        # 录制花费的粒度数量
        stepNum = 0
        
        # 回调函数处理录音数据
        def inputStreamCallback(indata, frames, time, status):
            # 【优化】比较占用内存，后续应该做优化
            self.inputStreamResult = numpy.concatenate((self.inputStreamResult,indata),axis=0)
            #print(os.getpid(),self.inputStreamResult.shape)
            
            self.tempStreamResult = numpy.concatenate((self.tempStreamResult,indata),axis=0)
            #print(os.getpid(),self.tempStreamResult.shape,'haha')
        
        # 创建 InputStream 对象
        stream = sounddevice.InputStream(
                                        dtype=self.__dtype,
                                        callback=inputStreamCallback,
                                        samplerate=self.__samplerate,
                                        channels=self.__channels,
                                        )
        # 流开始
        with stream:
            print(os.getpid(),'stream start at',time.time())
            # 每次记录 stepLenth，记录了stepNum次     
            while not self.streamQuit:
                #self.inputStreamResult = numpy.empty((0,self.__channels),dtype=self.__dtype)
                self.tempStreamResult = numpy.empty((0,self.__channels),dtype=self.__dtype)
                sounddevice.sleep(int(tempStepLenth*1000))
                #print(os.getpid(),self.inputStreamResult.shape)
                #print(os.getpid(),self.tempStreamResult.shape)
                yield self.tempStreamResult
            print(os.getpid(),'stream end at',time.time())
        '''
        # For Test
        n = 0
        while True:
            n += 1
            time.sleep(2)
            yield n
        '''
       
    # 录音    
    def rec(self):
        content_data = numpy.empty((0,self.__channels),dtype=self.__dtype)
        #step可以取无限长
        step = 10
        content_data = sounddevice.rec(frames=step*self.__samplerate,samplerate=self.__samplerate,channels=self.__channels,dtype=self.__dtype)
        #子线程监控状态，截取结果
        t = threading.Thread(target=self.ifStop,args=())
        t.start()
        while True:
            time.sleep(1)
            print(sounddevice)
        self.audioStreamToWav(content_data,'last record by rec')
        return content_data
    
    # 结束录音
    def ifStop(self):
        """
        stepLenth = 0.5
        n = 0
        while not self.recStop:
            n = n + 1
            time.sleep(stepLenth)
        """
        time.sleep(3)
        sounddevice.stop()
        return
    
    # 通过outputstream进行音频播放
    def playStream(self,audioBytes):
        
        def outputStreamCallback():
            print("callback",end=" ")
        # bytes 处理成 ndarray
        audioData = numpy.frombuffer(audioBytes,numpy.int16 if self.__dtype == 'int16' else numpy.float32)

        stream = sounddevice.OutputStream(
            dtype = self.__dtype,
            samplerate = self.__samplerate,
            channels=self.__channels,
        )
        with stream:
            print(type(audioData),audioData.dtype,audioData.shape)
            stream.write(audioData)   
        return
    
    def play(self,soundData):
        sounddevice.play(soundData,self.__samplerate)
        sounddevice.wait()
          
    def playByWav(self,url):
        dataset ,fsample  = soundfile.read(url)
        sounddevice.play(dataset,fsample)
        sounddevice.wait()
        return

    
    
    
    