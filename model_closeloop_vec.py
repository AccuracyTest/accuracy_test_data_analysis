import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.pyplot import MultipleLocator


def ReadFile(filename):
    path = './Data/'
    f = open(path + filename)
    lines = f.readlines()
    return lines


def Collating(lines):
    x, y, z = [], [], []
    for line in lines:
        line = line.strip().split(',')
        for element in line:
            element = element.strip().split(':')
            # print(element)
            if element[0] == 'x':
                x.append(float(element[1]))
            if element[0] == 'y':
                y.append(float(element[1]))
            if element[0] == 'z':
                z.append(float(element[1]))
    return x, y, z


def Calculate_angle(vec1, vec2):
    dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]
    modulus_vec1 = np.sqrt(vec1[0] * vec1[0] + vec1[1] * vec1[1] + vec1[2] * vec1[2])
    modulus_vec2 = np.sqrt(vec2[0] * vec2[0] + vec2[1] * vec2[1] + vec2[2] * vec2[2])
    cos_ = dot_product / (modulus_vec1 * modulus_vec2)
    angle = np.arccos(cos_) * 180 / np.pi

    return angle


if __name__ == "__main__":
    line = ReadFile("model_i5_closeloop_Vec_1130.txt")
    x, y, z = Collating(line)
    teach_vector = [x[0], y[0], z[0]]
    angle = []
    x.pop(0)
    y.pop(0)
    z.pop(0)

    for i in range(len(x)):
        angle.append(Calculate_angle(teach_vector, [x[i], y[i], z[i]]))

    angle_avg = np.mean(angle)
    angle_std = np.std(angle)
    angle_error = [angle_avg - 3 * angle_std, angle_avg + 3 * angle_std]
    print("angle_avg: ", angle_avg)
    print("angle_std: ", angle_std)
    print("angle_error: ", angle_error)
    my_font = font_manager.FontProperties(fname='C:/WINDOWS/Fonts/simsun.ttc')
    figure = plt.figure(figsize=(5, 4))

    plt.title('模板定位-闭环验证姿态定位精度测试结果', weight='bold', fontproperties=my_font, fontsize=14)
    plt.grid()
    plt.plot(angle, 'b-', linewidth=3, label='Measured Orientation')
    plt.plot([0, len(angle)], [angle_avg, angle_avg], 'g--', linewidth=3, label='Average Measured Orientation')
    plt.plot([0, len(angle)], [0, 0], 'r-.', linewidth=3, label='Teach Orientation')
    plt.text(len(angle)/2, 2, '平均姿态: {angle_avg}[deg]\n标准差：{angle_std}[deg]'.format(angle_avg=round(angle_avg, 3), angle_std=round(angle_std, 3)), fontproperties=my_font, fontsize=10)
    plt.xlabel('测试次数', fontproperties=my_font, fontsize=12)
    plt.ylabel('姿态[deg]', fontproperties=my_font, fontsize=12)
    plt.xlim(-5, len(angle)+5)
    plt.ylim(-10, 10)
    x_major_locator = MultipleLocator(20)
    y_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('模板定位-闭环验证姿态定位精度测试结果-向量夹角法.png')
    plt.show()
