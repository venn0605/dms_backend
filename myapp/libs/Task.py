from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from myapp.libs.mdflib import mdflib
# from mdflib import mdflib
from myapp.dbcurd import dbcurd


class Task():

    def __init__(self,mf4TxtPath,imgoutput):
        self.mf4txtpath = mf4TxtPath
        self.imgoutput = imgoutput
        self.workerNum = 2
        self.dbs = dbcurd()

    def mf4toimgs(self):
        # mf4List = []
        # 1 判断txt文件是否存在 兵器 读取mf4路径文件
        # print("txtpath = ",self.mf4txtpath)
        filePath = Path(self.mf4txtpath)
        if not filePath.exists():
            return 
        # 2 打开txt 文件 读取mf4文件路径
        datas = []
        with open(str(filePath),"r",encoding="utf-8") as fp:
            for data in fp.readlines():
                # print("aa = ",data)
                mf4List = []
                mf4filepath = data.rstrip()
                mf4list = [datas for datas in Path(mf4filepath).glob("*.mf4")]
                datas.append((mf4filepath,mf4list))
                # 调用数据库库接口 执行数据的插入操作
                self.dbs.insert(mf4filepath, self.imgoutput, mf4list)

        ### add func 

                # 3  开启多线程 进行mf4 to imgs
        self.ThreadPool(datas)
        # print(datas)


    def workers(self,mf4FilePath):
        # print(mf4FilePath)

        #  mf4 imgs file output folder is exists found
        # 判断文件是否已经提取图片
        mf4filepaths = Path(mf4FilePath).name
        if not self.dbs.isimgoutput(mf4filepaths):
            mdfs = mdflib(mf4FilePath, self.imgoutput, 6)
            mdfs.imgSave()
            self.dbs.update(mf4filepaths)
        else:
            print("文件图片已提取...")

    # 开启线程执行 mf4 to img 的函数
    def ThreadPool(self,mf4List):

        threadpools = ThreadPoolExecutor(max_workers=self.workerNum,thread_name_prefix="mf4toimgs") # 开启线程池
        for li in mf4List:
            for da in li[1]:
                threadpools.submit(self.workers,str(da))
        threadpools.shutdown(wait=True)


    def run(self,timesnumber):
        backs = BackgroundScheduler()
        backs.add_job(func=self.mf4toimgs,id='mf4toimgs',trigger='cron',hour=9,minute=20)
        return backs


# if __name__ == "__main__":

#     confPath = r"C:\Users\XFN1SZH\Desktop\env\eshdms\testss\myapp\conf\conf.ini"

#     conf = ConfigParser()
#     conf.read(confpath)
#     task = Task(conf.get("data","mf4txtpath"),conf.get("data","imgoutput"))
#     task.run(timesnumber=4).start() # 开启后台执行