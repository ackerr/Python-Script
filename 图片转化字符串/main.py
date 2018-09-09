from PIL import Image
import argparse

###################################
# 1. 获取图片对象                   #
# 2. 转换为灰度值                   #
# 3. 保存字符图片                   #
###################################

# 对应的灰度值
ascii_char = list("$@AB%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_args():
    """ 命令行输入参数 """
    parse = argparse.ArgumentParser()
    parse.add_argument('input', default='cartoon.png')
    parse.add_argument('-o', '--output', default='cartoon.txt')
    parse.add_argument('--width', type=int, default=60)
    parse.add_argument('--height', type=int, default=60)

    args = parse.parse_args()
    image, output_file, width, height = args.input, args.output, args.width, args.height
    return image, output_file, width, height


def get_gary_char(r: int, g: int, b: int, alpha: int =256) -> str:
    """ 获取对应的灰度值 """
    if alpha == 0:
        return ' '  # 需要补个空格
    gary = int((2126 * r + 7152 * g + 722 * b) / 10000)
    index = int((gary / (alpha+1)) * len(ascii_char))  # 获取对应的灰度索引
    return ascii_char[index]


def save_output_image(input_image, output_image, width, height):
    """ 图片灰度 """
    content = ''
    image = Image.open(input_image)
    image = image.resize((width, height), Image.NEAREST)
    for i in range(height):
        for j in range(width):
            content += get_gary_char(*image.getpixel((j, i)))
        content += '\n'
    print(content)
    with open(output_image, 'w') as f:
        f.write(content)


def main():
    """ 解析图片 """
    input_file, output_file, width, height = get_args()
    save_output_image(input_file, output_file, width, height)


if __name__ == '__main__':
    main()

