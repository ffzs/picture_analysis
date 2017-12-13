import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def make_pic(all_y,rge,type):
    all_x = np.arange(1, len(all_y) + 1, 1)
    all_y = np.array(all_y)
    plt.subplot(1, type[4], type[5])
    plt.plot(all_y, -all_x)
    plt.plot([min(all_y), max(all_y)], [-rge[0], -rge[0]], linestyle='--')
    plt.plot([min(all_y), max(all_y)], [-rge[1], -rge[1]], linestyle='--')
    plt.plot([90, 90], [-rge[1], -rge[0]], linestyle='--')
    plt.yticks([])
    plt.xticks([])
    plt.title(type[5])

def average(gray):
    sumy = 0
    ly,lx =gray.shape
    for y in range(0, ly):
        for x in range(0, lx):
            m = gray[y, x]
            sumy += int(m)
    return sumy/lx/ly

def get_pic_together(analysis_pic_path):
    paths = analysis_pic_path
    width, height = Image.open(paths[0]).size
    toImage = Image.new('RGBA', (width, height * len(paths)))
    for i in range(0, len(paths)):
        pic_fole_head = Image.open(paths[i])
        toImage.paste(pic_fole_head, (0, i * height, width, (i + 1) * height))
    toImage.save(out_path+pic_name+'/a--B--.png')

def make_save_dir(pic_name):
    paths = [out_path,collect_dir,analysis_dir]
    for path in paths:
        path = path+pic_name
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        else:
            continue

def get_pic_name(path):
    return path.split('.')[0]

def get_paths(dirpath):
    return os.listdir(dirpath)

def get_image(path):
    image = cv2.imread(path)
    return image

def get_gray(image):
    gary = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gary

def get_binary(gray,boundary):
    ret, binary = cv2.threshold(gray, boundary, 255, cv2.THRESH_BINARY)
    return ret,binary

def get_point_y(binary):
    sumy,m,pointy,ally,point_y,key_point_y,total = 0,0,[],{},[],[],0
    type=[0,0,0,0,0,0]   ###type [单排数0双排数1，数的宽度，传入y上坐标,多少行，多少列，列数]
    for y in range(0, ly):
        ally[y] = int(sumy / lx)
        sumy = 0
        for x in range(0, lx):
            m = binary[y, x]
            sumy += int(m)
    # print(ally)
    while m < ly:
        if ally[m] > 6:
            n = 0
            while ally[m + n] > 6:
                n += 1
                if m + n >= ly:
                    break
            if n > 5:
                point_y.append([m, n])
            m += n
        m += 1
    # print(point_y)
    for i in range(0,len(point_y)):
        if (point_y[0][1] - 1) <= point_y[i][1] <= (point_y[0][1] + 1):
            pointy.append(point_y[i][0])
    # print(pointy)
    i = 0
    while i<len(pointy)-1:
        if (point_y[0][1]) <(pointy[i+1]-pointy[i]) < (point_y[0][1]*3):
            key_point_y.append(pointy[i])
            key_point_y.append(pointy[i+1])
        i += 1
    if key_point_y[1] - key_point_y[0] < 35:
        key_point_y = key_point_y[::2]
        type[0] = 1
    key_point_y.append(ly)
    type[1]=point_y[0][1]+2
    return key_point_y,type

def get_mark(all_y):
    a,b = [],[]
    for i in range(3, len(all_y) - 3):
        if (all_y[i-1]<all_y[i] )&(all_y[i+2]<all_y[i+1]<all_y[i]):
            a.append(i)
            b.append(all_y[i])
    top = [a, b]
    max1 = max(top[1])
    i = 0
    while top[1][i] != max1:
        i += 1
    top = a[i:i + 5]
    if len(top)==4:
        top.append(len(all_y)-2)
    elif len(top)==3:
        for w in range(2):
            top.append(len(all_y)-2)
    return top

def get_top(all_y):
    top = []
    for i in range(3, len(all_y) - 3):
        if (all_aver<all_y[i-2]<all_y[i-1]<all_y[i] )&(all_aver<all_y[i+2]<all_y[i+1]<all_y[i]):  ###
            top.append(i)
    if len(top)==0:
        top = [0]
    return top

def get_sumy(pic):
    ky, kx = pic.shape
    pic = pic[0:ky, int(kx / 4):int(3 * kx / 4)]
    ky, kx = pic.shape
    all_y, sumy = [], 0
    for y in range(0, ky):
        sumy = 0
        for x in range(0, kx):
            m = pic[y, x]
            sumy += int(m)
        if kx>0:
            aver = round((sumy / kx), 3)
            all_y.append(aver)
    return all_y

def get_key_x(top_img):
    allx,key_point_x ,pointx1= {},[],[]
    sumx , m= 0,0
    print(top_img)
    (ky, kx) = top_img.shape
    print(ky,kx)
    for x in range(0, kx):
        allx[x] = int(sumx)
        sumx = 0
        for y in range(0, ky):
            m = top_img[y, x]
            sumx += int(m)
    while m < kx:
        if allx[m] < 100:
            n = 0
            while allx[m + n] < 100:
                n += 1
                if m + n >= kx:
                    break
            if  (n>3):
                pointx1.append(m)
                pointx1.append(m+n)
            m += n
        m += 1
    if determine == 1:
        spacing = round((pointx1[-3] - pointx1[1]-2) / (int(number / 2) * 2 - 1), 2)
    else:
        spacing =round((pointx1[-2]-pointx1[2]-2)/((len(pointx1)-4)-1),2)
    return spacing,pointx1[1]

def get_point_x(img,type,k):
    key_point_x = []
    boundary = [150,all_aver+10]
    gray = get_gray(img)
    (ky, kx) = gray.shape
    ret, binary = get_binary(gray, boundary[0])
    top_img = binary[0:type[1],0:lx]
    cv2.imwrite("top_img" + str(k + 1) + ".jpg", top_img)
    ####
    spacing,_ = get_key_x(top_img)
    ret, binary = get_binary(gray, boundary[1])
    cv2.imwrite("binary2" + str(k + 1) + ".jpg", binary)
    print(type[1],ky,kx)
    main_img = binary[type[1]*3:ky-1, 0:kx]
    cv2.imwrite("main_img" + str(k + 1) + ".jpg", main_img)
    blur_img = cv2.medianBlur(main_img, 3)
    cv2.imwrite("blur_img" + str(k + 1) + ".jpg", blur_img)
    _,point = get_key_x(blur_img)
    point = point - int(spacing/4)
    print(point,spacing)
    while point <= lx:
        key_point_x.append(int(point)-1)
        point += spacing
    return key_point_x

def analysis(all_y,tops,rge):
    a,b,c,total,ave = 0,0,0,0,0
    # print(rge[0],rge[1],tops)
    for item in all_y:
        total +=item
    ave = int(total/len(all_y))
    stan = min([ave+5,(all_aver+8)])
    # print(stan)
    if tops[0] !=0:
        for i in range(rge[0],rge[1]):
            if all_y[i] > stan:
                c += (all_y[i] - stan)
        for top in tops:
            if rge[0]<=top<=rge[1]:
                a += (all_y[top]+all_y[top-1]+all_y[top+1]+all_y[top-2]+all_y[top+2]-(all_aver-10)*5)
            else:
                b += (all_y[top]+all_y[top-1]+all_y[top+1]+all_y[top-2]+all_y[top+2]-(all_aver-10)*5)
    else:
        a , b = 0,0
    if a+c >0 :
        a = a+c
    else:
        a = 0
    return round(a,3),round(b,3)

def analysis_1(all_y,tops,rge):
    a, b, c, total, ave = 0, 0, [], 0, 0
    for item in all_y:
        total +=item
    ave = int(total/len(all_y))
    stan = max([ave,all_aver+10])
    for top in tops:
        if rge[0]<=top<=rge[1]:
            for num in range(top-2,top+3):
                c.append(num)
                a += (all_y[num]-all_aver)
            for num in range(rge[0],rge[1]+1):
                if (num not in c) & (all_y[num]>stan) :
                    a += (all_y[num]-all_aver)
        else:
            b += (all_y[top] + all_y[top - 1] + all_y[top + 1] + all_y[top - 2] + all_y[top + 2] - all_aver * 5)
    return round(a,3),round(b,3)

def get_range(mark):
    if mold == '1':
        return [mark[1]-1,mark[3]+1]
    if mold == '2':
        return [mark[0],mark[0]+3]

def get_grade(sum_in,sum_out):
    a = '0'
    if sum_in == 0:
        a = ' 0'
    elif sum_out == 0:
        a = ' 1'
    elif 0.35>sum_out/sum_in>0:
        a = '1.2'
    elif 0.7>sum_out/sum_in>=0.35:
        a = '1.5'
    elif 1.3>sum_out/sum_in>=0.7:
        a = ' 2'
    elif 1.8 > sum_out / sum_in >= 1.3:
        a = '2.5'
    elif 2.8 > sum_out / sum_in >= 1.8:
        a = ' 3'
    elif 5.8 > sum_out / sum_in >= 2.8:
        a = ' 4'
    elif sum_out / sum_in >= 5.8:
        a = ' 8'
    return a

def cut_x(picture,key_point_x,k,type):
    a = ['a','b','c','d']
    picture = get_gray(picture)
    (ky, kx) = picture.shape
    mark_pic = picture[type[1]*3:ky,key_point_x[0]:key_point_x[1]]
    all_y = get_sumy(mark_pic)
    mark = get_mark(all_y)
    rge = get_range(mark)
    for i in range(1,len(key_point_x)-1):
        type[5] = i
        # pic = picture[0:ky,key_point_x[i]:key_point_x[i+1]]
        # cv2.rectangle(picture, (key_point_x[i]+2, type[1] * 3), (key_point_x[i+1]-2, type[1] * 3 + mark[-1]), (0, 0, 255), 1)
        pic = picture[type[1] * 3:type[1] * 3 + mark[-1], key_point_x[i]:key_point_x[i + 1]]
        name = a[k] +str(i)
        cv2.imwrite(collect_dir+pic_name+'/image_' + name + '.jpg', pic)
        all_y = get_sumy(pic)
        tops = get_top(all_y)
        sum_in,sum_out = analysis(all_y, tops,rge)
        grade = get_grade(sum_in,sum_out)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, str(i), (key_point_x[i]+4, type[2] + type[1] * 2), font, 0.4, (255, 255, 0), 1)
        cv2.putText(image, grade, (key_point_x[i], type[2] + type[1] * 4), font, 0.4, (0, 255, 255),1)  # 添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细
        make_pic(all_y, rge, type)
        print("+++++++++"+name+"图像已经成功绘制完成+++++++++++")
    return rge

def cut_y(key_point_y,image,type):
    ana_pic_path =[]
    for i in range(0,len(key_point_y)-1):
        picture = image[key_point_y[i]-1:key_point_y[i+1]-1,0:lx]
        cv2.imwrite('picture' + str(i + 1) + '.jpg', picture)
        key_point_x = get_point_x(picture,type,i)
        type[2] = key_point_y[i]###type [单排数0双排数1，数的宽度，传入y上坐标]
        type[3] = len(key_point_y)-1
        type[4] = len(key_point_x)-1
        plt.figure(i+1,figsize=(24, 4))
        rge = cut_x(picture, key_point_x,i,type)
        plt.savefig(analysis_dir+pic_name+"/examples"+str(i+1)+".jpg")
        ana_pic_path.append(analysis_dir+pic_name+"/examples"+str(i+1)+".jpg")
        cv2.rectangle(image, (3, type[2] + type[1] * 3 + rge[0]), (lx - 3, type[2] + type[1] * 3 + rge[1]),(0, 0, 255), 1)
    cv2.imwrite(out_path+pic_name + '/--A--.jpg', image)
    return ana_pic_path

if __name__ == '__main__':
    print('----胶图分类对应序号：1.ITS1-5F ,2.16SV34...')
    mold = input("请输入序号：")
    print('----是否自动识别胶孔数：1.是 ，2.否--- 注：胶片数字太近，数字有间断请手动----')
    determine = int(input("1 or 2 ："))
    if determine == 1:
        print('----请输入每一行胶孔数-----注：手动模式一次只能识别一个胶图------')
        number = int(input("胶孔数："))
    dirpath = "F://pic_dir/"
    out_path = "F://pic_collect/"
    collect_dir = "F://pic_collect/collection/"
    analysis_dir = "F://pic_collect/analysis/"
    paths = get_paths(dirpath)
    boundary = 200
    for path in paths:
        print("+++++++++正在处理"+path+"图片+++++++++++")
        root_image = get_image(dirpath+path)
        image = cv2.copyMakeBorder(root_image, 0, 0,1, 1,  cv2.BORDER_CONSTANT, value=(0, 0, 0))
        pic_name = get_pic_name(path)
        make_save_dir(pic_name)
        gray = get_gray(image)
        ret, binary = get_binary(gray,boundary)
        (ly, lx) = binary.shape
        cv2.imwrite("binary.png",binary)
        key_point_y ,type = get_point_y(binary)
        all_aver = average(get_gray(root_image))
        print(all_aver)
        analysis_pic_path = cut_y(key_point_y,image,type)
        get_pic_together(analysis_pic_path)


