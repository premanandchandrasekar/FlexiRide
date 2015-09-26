from pytesseract import image_to_string
from StringIO import StringIO
from PIL import Image


class ImageProcessor(object):
    def __init__(self, data, pan_no=None):
        self._pan_no = pan_no
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def pan_no(self):
        return self._pan_no

    @property
    def text(self):
        return self._text

    def getIDfromText(self, text):
        result = "none"
        id_card = [x for x in text.split() if len(x) == 10]
        for _id in id_card:
            if _id[:5].isalpha() and _id[5:9].isdigit() and _id[-1].isalpha():
                result = _id
                break
        return result

    def process(self):
        img_file = Image.open(StringIO(self.data))
        text = image_to_string(img_file)
        result = self.getIDfromText(text)
        if result != "none":
            self._pan_no = result
            self._text = text
            return
        
        img_file = img_file.convert('L')
        text = image_to_string(img_file)
        result = self.getIDfromText(text)
        if result != "none":
            self._pan_no = result
            self._text = text
            return
        
        img_file = img_file.point(lambda x: 0 if x<100 else 255, '1')
        text = image_to_string(img_file)
        result = self.getIDfromText(text)
        self._pan_no = result
        self._text = text
