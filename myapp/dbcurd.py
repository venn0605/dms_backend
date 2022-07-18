from pathlib import Path
from sqlalchemy.orm import sessionmaker

# from models import Mf4FileInfo as files,Mf4PathInfo as paths,engine
from models import Mf4FileInfo as files, Mf4PathInfo as paths, engine

Session = sessionmaker(bind=engine)


class dbcurd():

    def __init__(self):
        self.session = Session()

    def select(self, pathss:str) -> bool:
        print(pathss)
        mf4data = self.session.query(paths).filter(paths.mf4path == pathss).first()
        if mf4data == None:
            return False
        else:
            return True

        # try:
        #     mf4data = self.session.query(paths).filter(paths.mf4path == pathss).first()
        # except Exception as e:
        #     return False
        # else: # 没有发生异常
        #     print(mf4data.mf4pathid)
        #     return True

        # print(mf4data)

    def selectdata(self, mf4path:str):
        ...
        mf4listdata = []
        retdata = self.session.query(paths).filter(paths.mf4path == mf4path).first()

        # mf4listdata.append(retdata.mf4filenumber)
        data = self.session.query(files).filter(files.mf4pathid == retdata.mf4pathid).all()
        for li in data:
            # print(li.mf4fileid,li.mf4name)
            tuples = (li.mf4fileid,li.mf4name)
            mf4listdata.append(tuples)
        # print(mf4listdata)
        retdict = {
            "mf4pathnumber":retdata.mf4filenumber,
            "mf4filelist":mf4listdata
        }
        # print(retdict)
        return retdict

        # print(tuple(1,"222"))

    def insert(self, mf4path:str, imgoutputpath:str, mf4list:list) -> bool:
        ...
        
        # 首先要判断该文件夹是否在数据库中
        if self.select(mf4path):
            print(f"{mf4path} 已存在")
            return False

        p = paths(mf4path, len(mf4list)) # print(p.mf4pathid)
        self.session.add(p)
        self.session.commit()
        
        # 批量添加数据
        mf4filelist = []
        for li in mf4list:
            imgoutputpaths = Path(imgoutputpath).joinpath(li.name.split(".")[0])
            f = files(li.name, imgoutputpaths,p.mf4pathid)
            mf4filelist.append(f)
        self.session.add_all(mf4filelist)
        self.session.commit()

    def delete(self, mf4path:str) ->bool():
        ...
        isflag = False
        try:
            deldata = self.session.query(paths).filter(paths.mf4path == mf4path).delete()
            self.session.commit()
        except Exception as e:
            pass
        else:
            isflag = True
        
        return isflag


    def update(self, mf4name:str):
        ...
        retdata = self.session.query(files).filter(files.mf4name == mf4name).update({"isok":True})
        self.session.commit()

        print(retdata)


    def isimgoutput(self, mf4name) ->bool:
        retdata = self.session.query(files).filter(files.mf4name == mf4name).filter(files.isok == True).first()
        if retdata == None:
            return False
        return True

    def test(self, mf4path):
        data = {}
        data['mf4Info'] = []
        retdata = self.session.query(paths).filter(paths.mf4path == mf4path).first()
        data['mf4FileNumber'] = retdata.mf4filenumber
        mf4data = self.session.query(files).join(paths).filter(paths.mf4path == mf4path).all()
        for i in range(len(mf4data)):
            data['mf4Info'].append((mf4data[i].mf4fileid, mf4data[i].mf4name))
        print('done')
        
        return retdata, mf4data

if __name__ == "__main__":
    ...

    d = dbcurd()
    mf4path = r"C:\Users\XFN1SZH\Desktop\DMS\tool_read"
    d.test(mf4path)
    # mf4name = r"CA_S311MCA_8519C_20210912_114553_001.mf4"
    # d.isimgoutput(mf4name)
    # d.select(r"C:\Users\XFN1SZH\Desktop\DMS\tool_read")

    # d.update("1V_Skoda_SuperB_5383C_20210514_163711_036.mf4")

    # mf4path = r"C:\Users\XFN1SZH\Desktop\DMS\tool_read"
    # d.delete(mf4path)

    # mf4path = r"C:\Users\XFN1SZH\Desktop\DMS\tool_read"
    # imgoutputpath = r"\\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\Temp_folder_for_isilon1\xpeng\aa\imgoutput"
    # d.insert(mf4path, imgoutputpath)
