# OCR代码
import paddlehub as hub
# 定义识别类，可以文字识别
class Recognition:
    def __init__(self, img):
        self.img = img
    def text_recognize(self)-> list:
        ocr = hub.Module(name="chinese_ocr_db_crnn_server")
        result = ocr.recognize_text(images=[self.img],use_gpu=False)
        return result
if __name__=="__main__":

    pass