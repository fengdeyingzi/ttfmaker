# 导入系统库
import cv2
import os
import shutil
import hashlib

def get_temp_path():
    # 获取系统临时目录
    return os.environ['TEMP']

def calculate_md5(file_path):
    # 计算文件的MD5值
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_file_to_temp(file_path):
    # 获取临时路径
    temp_path = get_temp_path()
    
    # 计算MD5值
    md5_value = calculate_md5(file_path)
    
    # 复制文件到临时目录，并重命名
    destination = os.path.join(temp_path, f"{md5_value}.png")
    shutil.copy(file_path, destination)
    
    return destination

def main():
    '''主函数'''
    # 定义参数
    img_list = list()
    img_dir = './crop' 
    temp_path = os.getenv('TEMP')

    # svg宽度放大数量
    w_add = 0
    # svg高度放大数量
    h_add = 0
    # 横向偏移量
    x_offset = 0
    # 纵向偏移
    y_offset = 0
    print("Temp Path:", temp_path)
    # 获取文件列表
    for file in os.listdir(img_dir):
            if os.path.splitext(file)[1].lower() in '.png|.jpg':
                img_list.append(file)
    print('当前总图片数量： %d' % len(img_list))
    
    # 循环处理图片
    index = 0
    for img_path in img_list:
        print(os.path.join(img_dir,img_path))
        img_origin = os.path.join(img_dir,img_path)
        img_temp = copy_file_to_temp(img_origin)
        textimg = cv2.imread(img_temp,cv2.IMREAD_COLOR)
        if textimg is None:
            print(f"Error loading image: {img_path}. Skipping...")
            continue
        # 提取图形区域
        textimg = cv2.resize(textimg, dsize=(640, 640))
        
        blur = cv2.GaussianBlur(textimg, (5, 5), 0)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)               
        contours,hierarchy = cv2.findContours(thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        
        epsilon = 10
        h, w, _ = textimg.shape
        w = w + w_add
        h = h + h_add
        code = os.path.splitext(img_path)[0]
        svg_path = 'svg/'+code+'.svg'
        with open(svg_path, "w+") as f:
            f.write(f'<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="{w}.000000pt" height="{h}.000000pt" viewBox="0 0 {w+40}.000000 {h+40}.000000" preserveAspectRatio="xMidYMid meet">')      
            f.write(f'<g transform="scale(1.00000,1.00000)">')
            for c in contours:
                f.write('<path d="M')
                approx = cv2.approxPolyDP(c,epsilon,False)
                for i in range(len(approx)):
                    x, y = approx[i][0]
                    x = x + x_offset
                    y = y + y_offset
                    if i == len(approx)-1:
                        f.write(f"{x} {y}")
                    else:
                        f.write(f"{x} {y} ")
                f.write('"/>')                
            f.write(f'</g>')
            f.write("</svg>")
        index +=1
        print('当前处理完 %d 张图片' % index)
    print('全部处理结束')

if __name__ == "__main__":
    '''程序入口'''
    main()
