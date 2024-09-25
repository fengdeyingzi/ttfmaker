# 导入系统库
from time import sleep
import fontforge, os,psMat


def main():
    '''
    主函数
    '''
    # 定义参数
    img_list = list()
    img_dir = './svg' 

    # 获取文件列表
    for file in os.listdir(img_dir):
            if os.path.splitext(file)[1].lower() in '.svg':
                img_list.append(file)
    print('当前总图片数量： %d' % len(img_list))
    
    # 循环处理图片
    index = 0
     # 创建字体
    codestr = "font"
    font = fontforge.font()
    font.encoding = 'UnicodeFull'
    font.version = '1.0'
    font.weight = 'Regular'
    font.fontname = 'uni'+codestr
    font.familyname = 'uni'+codestr
    font.fullname = 'uni'+codestr       
    for img_path in img_list:  
        print('当前处理 '+img_path)
        
        # 获取unicode
        codestr = os.path.splitext(img_path)[0]
        if codestr and codestr[0] != '$':
            # 如果第一个字符不是'$'，将codestr转换为unicode码
            codestr = ''.join(f'{ord(char):04x}' for char in codestr)
        else:
            codestr = codestr[1:]

        print("当前十六进制码为:"+codestr)
        if len(codestr) > 4:
             print('codestr 超出 4 位')
             continue
        code = int(codestr,16)
        
        
        
        # 创建字符
        glyph = font.createChar(code, "uni"+codestr)
        glyph.importOutlines(os.path.join(img_dir,img_path))
        
        # 位移调整
        base_matrix = psMat.translate(0,0)
        glyph.transform(base_matrix)
        
          
        index +=1
        # if index>1:
        #     break
        print('当前处理完 %d 张图片' % index)
        
        # 删除文件
        os.remove(os.path.join(img_dir,img_path))
    # 写入ttf
    font.generate('./ttf/font.ttf')    
    print('全部处理结束')


if __name__ == "__main__":
    '''
    程序入口
    '''
    main()
