import PySide2
from PySide2.QtGui import QImage
import py_seq_access
import os
from random import randint
import sys
from pathlib import Path

class mdflib():

    def __init__(self, files,outputPath,setp):
        self._file = files
        seq_reader, video_stream, number_frame = self.load_seq(files)
        self._outputPath = outputPath
        self._seqReader = seq_reader
        self._video_stream = video_stream
        self._number_frame = number_frame # 总的帧数
        self.setp = setp

    def load_seq(self, sequence):
        seqReader = py_seq_access.SeqReader()
        (_, seq_name) = os.path.split(sequence)
        (base_name, _) = os.path.splitext(seq_name)
        video_stream = None
        if seqReader.open(sequence):
            number_frames = seqReader.number_of_frames()
            """
            print(seqReader.number_of_frames())
            print(seqReader.get_available_eds_data())
            print(seqReader.get_video_stream_info())
            """
        video_stream = seqReader.get_image_stream(0) #, r2dtwo=r2dtwo_dict
        return seqReader, video_stream, number_frames


    def read_rgb_image(self, frame_index):
        if frame_index < self._number_frame:
            img_number = self._video_stream.get_image_number_from_raw_image(frame_index)
            rgb_image = self._video_stream.get_RGB_image_at_frame_count(py_seq_access.RawImage, img_number)
        return img_number, rgb_image


    def imgSave(self): # frame_index 帧数 setp 步长
        # 获取到总的帧数  self._number_frame
        # self._file # mf4 file path
        # mf4 name self._file
        
        # 进行for循环 保存imgs
        filename = self._file.split("\\")[-1].split(".")[0]
        print(filename)
        nums = int(self._number_frame/self.setp)

        outputPaths = Path(Path(self._outputPath).joinpath(filename))
        
        if outputPaths.exists():
            return
            
        if not outputPaths.exists():
            outputPaths.mkdir(exist_ok=True)

        for li in range(self.setp):
            img_number,rgb_image = self.read_rgb_image(nums * (li))
            image = QImage(rgb_image, rgb_image.shape[1]/3, rgb_image.shape[0], rgb_image.shape[1],PySide2.QtGui.QImage.Format_RGB888)

            # save imgs
            print(f"{str(outputPaths)}//{filename}_{li + 1}.png")
            image.save(f"{str(outputPaths)}//{filename}_{li + 1}.png")


    # def tests(self):
    #     print(self._number_frame)
    #     nums = int(self._number_frame/6) # int 是向下取整

    #     for li in range(6):
    #         print(nums * (li))


if __name__ == "__main__":
    
    pass
    # mf4path = r"C:\Users\XFN1SZH\Desktop\DMS\tool_read\1V_Skoda_SuperB_5383C_20210514_163711_036.mf4"
    # outputmf4path = r"C:\Users\XFN1SZH\Desktop\DMS\tool_read"
    # data_reader = mdflib(mf4path,outputmf4path,6)

    # data_reader.imgSave()
    # data_reader.tests()

    # frameNumber = data_reader.getFrameNumber()
    # # print(frameNumber)
    # img_number,rgb_image = data_reader.read_rgb_image(100 - randint(50, 100))
    # # print(img_number)
    # # print(rgb_image.shape)
    # # im = PySide2.QtGui.QImage(rgb_image, rgb_image.shape[1]/3, rgb_image.shape[0], rgb_image.shape[1], PySide2.QtGui.QImage.Format_RGB888)
    # im = QImage(rgb_image, rgb_image.shape[1]/3, rgb_image.shape[0], rgb_image.shape[1],PySide2.QtGui.QImage.Format_RGB888)
    # # PySide2.QtGui.QImage()
    # # PySide2.QtGui.QImage()
    # im.save("./aa.jpg",None)

    