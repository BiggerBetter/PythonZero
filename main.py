from Utils import test
import zipfile
import os
from pathlib import Path

def main():
    folder = "/Users/Jenius/Desktop/unzip 2"
    path = "/Users/Jenius/Desktop/test1.zip"

    folderList = [folder]
    # fileList = [folderList]
    while len(folderList):
        foldePath = folderList.pop()
        returenList = unZipFolder(foldePath)
        return
        if len(returenList):
            folderList.append(returenList)

    # zFile = zipfile.ZipFile(path,"r")
    # for filee in zFile.namelist():
    #     zFile.extract(filee,"/Users/Jenius/Desktop")
    # zFile.close()

def unZipFolder(folderPath):
    for i, j, k in os.walk(folderPath):
        # i为根路径
        # j为文件夹集合字符串
        # k为子文件名集合字符串
        # print(i)
        tmpFoldeList = []

        # 如果文件名zip结尾就解压缩它，顺便判断是解压出来的是不是文件夹，是的话，加入到folderList中
        for tmpName in k:

            if(tmpName.endswith("zip")):
                # tmpName.TransFormChain
                # 	去掉</think>("zip")
                zipFilePath = i+"/"+tmpName
                print(zipFilePath)

                zFile = zipfile.ZipFile(zipFilePath,"r")
                for filee in zFile.namelist():
                    # filee = filee.encode('cp437').decode('UTF8')
                    zFile.extract(filee, i)



























                    #后面把只把文件名格式化不就行了
                    # oldname = unicode(name, 'gbk')
                    # os.rename(os.path.join(root, oldname), os.path.join(root, newname))
                    # (i+"/"+tmpName).rename(filee.encode('cp437').decode('gbk'))
                    # extracted_path = Path(zFile.extract(filee))
                    # extracted_path.rename(filee.encode('cp437').decode('UTF8'))




                zFile.close()

        # for(fileName in jd):





        # print(k)
        break




if __name__ == '__main__':
    main()

