import math
import random
from io import BytesIO

import itchat
from PIL import Image


# 根据微信好友数 微调图片大小
WIDTH = 400
HEIGHT = 400
FILE_NAME = "family.png"


def get_image_size(friends):
    """ 获取图片行列 """
    length = len(friends)
    size = int(math.sqrt((WIDTH * HEIGHT) // length))
    line = HEIGHT // size
    return length, size, line


def get_friends():
    """ 获取好友名称列表 """
    names = [friend["UserName"] for friend in itchat.get_friends()]
    random.shuffle(names)
    return names


def generate_photo():
    """ 生成全家福 """
    names = get_friends()
    length, size, line = get_image_size(names)
    photo = Image.new("RGBA", (WIDTH, HEIGHT)).convert("RGB")
    for i, name in enumerate(names):
        image = Image.open(BytesIO(itchat.get_head_img(userName=name)))
        image = image.resize((size, size), Image.ANTIALIAS)
        photo.paste(image, ((i % line) * size, (i // line) * size))
    photo.save(FILE_NAME)


if __name__ == "__main__":
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    generate_photo()
    itchat.send_image(FILE_NAME, "filehelper")
    itchat.logout()
