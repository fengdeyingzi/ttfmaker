import os
import math
from lxml import etree

def process_svg_file(file_path):
    # 解析 SVG 文件
    tree = etree.parse(file_path)
    root = tree.getroot()

    # 找到所有 path 元素
    for path in root.xpath('//svg:path', namespaces={'svg': 'http://www.w3.org/2000/svg'}):
        d = path.get('d')  # 获取 path 的 d 属性
        if d:
            # 分割路径命令和参数
            commands = d.split()
            new_commands = []

            # 处理路径中的坐标点
            for cmd in commands:
                if cmd.isalpha():  # 如果是命令（如 M, L, Z 等），则直接添加
                    new_commands.append(cmd)
                else:
                    # 处理坐标点
                    points = cmd.split(',')
                    new_points = []

                    for point in points:
                        # 分割 x 和 y 坐标
                        coords = point.split()
                        new_coord = []
                        coord_head = ""
                        for coord in coords:
                            if coord:  # 防止空字符串
                                # 转换为 float，除以 40，四舍五入后再乘以 40
                                if coord[0] == 'M':
                                    coord_head = coord[0]
                                    coord = coord[1:]
                                new_value = round(float(coord) / 40) * 40
                                new_coord.append(coord_head + str(new_value))
                        # 将处理后的坐标重新组合，并加入新点列表
                        new_points.append(" ".join(new_coord))

                    # 替换原有的坐标点
                    new_commands.append(",".join(new_points))

            # 更新 d 属性
            path.set('d', " ".join(new_commands))

    # 保存修改后的 SVG 文件
    tree.write(file_path, xml_declaration=True, encoding='utf-8', pretty_print=True)

def process_svg_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.svg'):
            file_path = os.path.join(directory, filename)
            process_svg_file(file_path)
            print(f'Processed file: {file_path}')

# 设置要处理的 SVG 目录
svg_directory = './svg'
process_svg_directory(svg_directory)