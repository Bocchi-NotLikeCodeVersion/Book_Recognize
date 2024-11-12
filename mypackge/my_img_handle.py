import cv2
import numpy as np

# 进行图片处理
# 定义图片处理类
class ImgProcess:
    def __init__(self,img):
        self.img=img
    def process(self):
        img1=cv2.imread(self.img)
        img2=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        img3=cv2.morphologyEx(img2, cv2.MORPH_BLACKHAT, np.ones((5,5)))
        img4=cv2.GaussianBlur(img3,(17,17),2)
        img5=cv2.Canny(img4,50, 100)
        img6=cv2.dilate(img5,np.ones((19,19)),3)
        contours, hierarchy = cv2.findContours(img6, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img8=0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # print(x, y, w, h)
            if w > 150:
                img7 = cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 100, 0), 2)
                # 可以裁剪出来
                img8 = img7[y:y + h, x:x + w]
        img9 = cv2.resize(img8, (200, 100))
        # cv2.imshow("img", img9)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return img9
if __name__ == '__main__':
    img_process1=ImgProcess("../assets/xiyou4.png") # luoluo2 xiyou1
    img_process1.process()
    pass
