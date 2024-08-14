"""
_summary_
# screen control 


"""
import PIL
import PIL.ImageGrab
from auto.file import file

def getScreenShot(bbox=[],fileName=''):
    screenImage = PIL.ImageGrab.grab(bbox)
    file.picSave(screenImage)
    return screenImage

def show():
    return


bbox = [100,200,800,1200]
url = 'asset/recordings/pics'
image = getScreenShot(bbox,)
imageList = []
# print(image.getdata())
for item in image.getdata():
    imageList.append(item)
print(imageList.__len__())
