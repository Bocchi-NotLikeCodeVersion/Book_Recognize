# OCR代码
import paddlehub as hub
# 定义识别类，可以文字识别
class Recognition:
    def __init__(self, img):
        # 初始化对象，接收图片作为参数
        self.img = img

    def text_recognize(self)-> list:
        # 加载PaddleHub中的中文OCR模块
        ocr = hub.Module(name="chinese_ocr_db_crnn_server")
        # 使用OCR模块进行文本识别，不使用GPU
        result = ocr.recognize_text(images=[self.img], use_gpu=False)
        # 返回识别结果
        return result

if __name__=="__main__":

    pass