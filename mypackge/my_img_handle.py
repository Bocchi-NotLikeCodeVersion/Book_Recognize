import cv2
import numpy as np

# 进行图片处理
# 定义图片处理类
class ImgProcess:
    def __init__(self,img):
        # 初始化图片处理类，接收图片路径作为参数
        self.img = img

    def process(self):
        # 读取图片
        img1 = cv2.imread(self.img)
        # 将图片转换为灰度图
        img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        # 对灰度图进行形态学操作，使用黑帽操作
        img3 = cv2.morphologyEx(img2, cv2.MORPH_BLACKHAT, np.ones((5, 5)))
        # 对处理后的灰度图进行高斯模糊
        img4 = cv2.GaussianBlur(img3, (17, 17), 2)
        # 对模糊后的图片进行边缘检测
        img5 = cv2.Canny(img4, 50, 100)
        # 对边缘检测后的图片进行膨胀操作
        img6 = cv2.dilate(img5, np.ones((19, 19)), 3)
        # 查找图片的轮廓
        contours, hierarchy = cv2.findContours(img6, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img8 = 0
        # 遍历所有轮廓
        for contour in contours:
            # 获取轮廓的外接矩形
            x, y, w, h = cv2.boundingRect(contour)
            # print(x, y, w, h)
            # 如果外接矩形的宽度大于150，则进行后续处理
            if w > 150:
                # 在原始图片上绘制矩形框
                img7 = cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 100, 0), 2)
                # 可以裁剪出来
                # 裁剪出矩形框内的图片部分
                img8 = img7[y:y + h, x:x + w]
        # 对裁剪后的图片进行缩放
        img9 = cv2.resize(img8, (200, 100))
        # cv2.imshow("img", img9)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 返回处理后的图片
        return img9

if __name__ == '__main__':
    img_process1=ImgProcess("../assets/xiyou4.png") # luoluo2 xiyou1
    img_process1.process()
    pass
