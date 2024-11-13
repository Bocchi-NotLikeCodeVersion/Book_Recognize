# pysimplegui 程序
import PySimpleGUI as sg
import re
from PIL import Image
import os
from mypackge import my_ocr,my_img_handle,operate_db_mode
from datetime import datetime
def demo():
    # 定义布局
    layout = [
        [sg.Text("书名:", size=(10, 1)), sg.InputText(key="book_name")],
        [sg.Text("简介:", size=(10, 1)), sg.InputText(key="book_introduce")],
        [sg.Input("请选择一张图片", key="img_filepath", enable_events=True), sg.FileBrowse(file_types=(("Image Files", "*.jpg *.png"),))],
        [sg.Text("选择的图片如下所示", key="input_tips_text")],
        [sg.Image(key='-IMAGE-')],
        [sg.Text(key="author_tips_text")],
        [sg.Image(key='author')],
        [sg.Button('上传书籍信息(传入作者图片)'), sg.Button('关闭'), sg.Button('识别书籍(仅限png图片)')]
    ]

    # 创建窗口
    window = sg.Window('书籍识别系统', layout)

    while True:
        # 读取窗口信息 返回窗口的数据和鼠标事件
        event, value_dict = window.read()

        # 定义图片和文本文件的保存路径
        img_filepath = fr'D:\images\{datetime.now().strftime("%Y%m%d %H%M%S")}.png'
        img_filepath2 = fr'D:\\images\\{datetime.now().strftime("%Y%m%d %H%M%S")}.png'
        txt_filepath = fr'D:\images\{datetime.now().strftime("%Y%m%d %H%M%S")}.txt'
        txt_filepath2 = fr'D:\\images\\{datetime.now().strftime("%Y%m%d %H%M%S")}.txt'

        if event in ('关闭', None):
            print("窗口关闭")
            break

        elif event == '识别书籍(仅限png图片)' and re.findall(r'\.[a-zA-Z]{3}$', value_dict["img_filepath"]):
            # 检查选择的图片是否为png格式
            if value_dict["img_filepath"][::-1][0:3] == "gnp":
                recognize_img = value_dict["img_filepath"]
                window['-IMAGE-'].update(filename=recognize_img)

                # 处理图片
                img_handle = my_img_handle.ImgProcess(recognize_img)
                tailor_img = img_handle.process()

                # 识别图片中的文字
                orc = my_ocr.Recognition(tailor_img)
                result1 = orc.text_recognize()
                book_name1 = result1[0]["data"][0]["text"]
                # print(book_name1)

                # 查询数据库中的书籍信息
                db3 = operate_db_mode.Operate_DB("opencv_images1")
                result2 = db3.select_table(table_name="books", bequeried_column="book_name", judgment_conditions_column2="book_name", value1=book_name1)
                # print(result2)

                if result2[0]:
                    # 获取书籍简介和作者图片
                    introduce = db3.select_table(table_name="books", bequeried_column="book_introduce_path", judgment_conditions_column2="book_name", value1=book_name1)
                    author = db3.select_table(table_name="books", bequeried_column="book_image_path", judgment_conditions_column2="book_name", value1=book_name1)
                    # print(introduce)

                    # 读取书籍简介并显示
                    f = open(introduce[1][0][0], 'r')
                    introduce_info = f.read()
                    sg.popup(introduce_info, line_width=10, grab_anywhere=True, image=author[1][0][0])
                    window['author_tips_text'].update("作者图片如下")
                    window['author'].update(filename=author[1][0][0])
                    f.close()
                else:
                    sg.popup("该书籍不存在，请先录入书籍信息")
                pass
            else:
                sg.popup("请选择png图片")

        elif event == "上传书籍信息(传入作者图片)" and re.findall(r'\.[a-zA-Z]{3}$', value_dict["img_filepath"]):
            # 检查书籍名称是否已存在
            db1 = operate_db_mode.Operate_DB("opencv_images1")
            result1 = db1.select_table(table_name="books", bequeried_column="book_name", judgment_conditions_column2="book_name", value1=value_dict['book_name'])
            if result1[0]:
                sg.popup("该书籍已存在")
                if os.path.exists(img_filepath):
                    os.remove(img_filepath)
            else:
                # 上传书籍信息
                if "img_filepath" in value_dict and re.findall(r'\.[a-zA-Z]{3}$', value_dict["img_filepath"]):
                    f = open(txt_filepath, 'w')
                    f.write(value_dict["book_introduce"])
                    f.close()

                    # 插入书籍信息到数据库
                    db2 = operate_db_mode.Operate_DB("opencv_images1")
                    result3 = db2.insert_table(table_name="books", info1=value_dict["book_name"], info2=txt_filepath2, info3=img_filepath2)

                    # 保存图片
                    image_path = value_dict["img_filepath"]
                    image = Image.open(image_path)
                    image.save(img_filepath, 'PNG')
                    window['-IMAGE-'].update(filename=img_filepath)

                    # 删除非png格式的图片
                    if os.path.exists(image_path) and image_path[::-1][0:3] != "gnp":
                        os.remove(image_path)

                    # 显示上传结果
                    if result3:
                        sg.popup("上传成功")
                    else:
                        sg.popup("上传失败")
                    pass
                else:
                    sg.popup("请选择图片")

    # 关闭窗口
    window.close()

if __name__ == '__main__':
    demo()