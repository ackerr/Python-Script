import argparse

from PIL import Image

###################################
# 1. 获取图片对象                   #
# 2. 转换为灰度值                   #
# 3. 保存字符图片                   #
###################################

# 对应的灰度值
# pylint c0103
char_list = list(
    r"$@AB%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
)


def get_args():
    """ 命令行输入参数 """
    parse = argparse.ArgumentParser()
    parse.add_argument("input", default="cartoon.png")
    parse.add_argument("-o", "--output", default="cartoon.txt")
    parse.add_argument("--width", type=int, default=60)
    parse.add_argument("--height", type=int, default=60)

    args = parse.parse_args()
    image, output_file, width, height = args.input, args.output, args.width, args.height
    return image, output_file, width, height


def get_gary_data(red: int, green: int, blue: int, alpha: int = 256) -> str:
    """ 获取对应的灰度值 """
    if alpha == 0:
        return " "  # 需要补个空格
    gary = int((2126 * red + 7152 * green + 722 * blue) / 10000)
    index = int((gary / (alpha + 1)) * len(char_list))  # 获取对应的灰度索引
    return char_list[index]


def save_output_image(input_image, output_image, width, height):
    """ 图片灰度 """
    content = ""
    image = Image.open(input_image)
    image = image.resize((width, height), Image.NEAREST)
    for i in range(height):
        for j in range(width):
            content += get_gary_data(*image.getpixel((j, i)))
        content += "\n"
    print(content)
    with open(output_image, "w") as image:
        image.write(content)


def main():
    """ 解析图片 """
    input_file, output_file, width, height = get_args()
    save_output_image(input_file, output_file, width, height)


if __name__ == "__main__":
    main()
