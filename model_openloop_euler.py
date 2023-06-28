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
    Rx, Ry, Rz, x, y, z = [], [], [], [], [], []
    for line in lines:
        line = line.strip().split(',')
        for element in line:
            element = element.strip().split(':')
            if element[0] == 'Rx':
                Rx.append(float(element[1]))
            if element[0] == 'Ry':
                Ry.append(float(element[1]))
            if element[0] == 'Rz':
                Rz.append(float(element[1]))
            if element[0] == 'x':
                x.append(float(element[1]))
            if element[0] == 'y':
                y.append(float(element[1]))
            if element[0] == 'z':
                z.append(float(element[1]))
    return Rx, Ry, Rz, x, y, z


def normalization(data, expectation):
    normalized_data = []
    for element in data:
        normalized_data.append(element - expectation)
    return normalized_data


def calEuclidean(x, y, z):
    dist = []
    for i in range(len(x)):
        dist.append(np.sqrt(np.square(x[i]) + np.square(y[i]) + np.square(z[i])))
    return dist


if __name__ == "__main__":
    line = ReadFile("model_i5_openloop_Euler_1130.txt")
    Rx, Ry, Rz, x, y, z = Collating(line)
    Rx_norm = normalization(Rx, Rx[0])
    Ry_norm = normalization(Ry, Ry[0])
    Rz_norm = normalization(Rz, Rz[0])
    x_norm = normalization(x, x[0])
    y_norm = normalization(y, y[0])
    z_norm = normalization(z, z[0])
    euclidean = calEuclidean(x_norm[1:], y_norm[1:], z_norm[1:])
    euclidean_avg = np.mean(euclidean)
    euclidean_std = np.std(euclidean)
    euclidean_error = [euclidean_avg - 3 * euclidean_std, euclidean_avg + 3 * euclidean_std]

    print("euclidean_avg: ", euclidean_avg)
    print("euclidean_std: ", euclidean_std)
    print("euclidean_error: ", euclidean_error)

    Rx_avg = np.mean(Rx_norm[1:])
    Rx_std = np.std(Rx_norm[1:])
    Rx_error = [Rx_avg - 3 * Rx_std, Rx_avg + 3 * Rx_std]

    Ry_avg = np.mean(Ry_norm[1:])
    Ry_std = np.std(Ry_norm[1:])
    Ry_error = [Ry_avg - 3 * Ry_std, Ry_avg + 3 * Ry_std]

    Rz_avg = np.mean(Rz_norm[1:])
    Rz_std = np.std(Rz_norm[1:])
    Rz_error = [Rz_avg - 3 * Rz_std, Rz_avg + 3 * Rz_std]

    print("Rx_avg: ", Rx_avg)
    print("Rx_std: ", Rx_std)
    print("Rx_error: ", Rx_error)

    print("Ry_avg: ", Ry_avg)
    print("Ry_std: ", Ry_std)
    print("Ry_error: ", Ry_error)

    print("Rz_avg: ", Rz_avg)
    print("Rz_std: ", Rz_std)
    print("Rz_error: ", Rz_error)

    my_font = font_manager.FontProperties(fname='C:/WINDOWS/Fonts/simsun.ttc')
    plt.title('模板定位-开环验证位置定位精度测试结果', weight='bold', fontproperties=my_font, fontsize=14)
    plt.grid()
    plt.plot(euclidean, 'b-', linewidth=3, label="Measured Euclidean Distance")
    plt.plot([0, len(euclidean)], [euclidean_avg, euclidean_avg], 'g--', linewidth=3, label="Average Measured Euclidean Distance")
    plt.plot([0, len(euclidean)], [0, 0], 'r-.', linewidth=3, label="Teach Point")
    plt.text(len(euclidean)/2, 3, '平均欧式距离: {euclidean_avg}[mm]\n标准差：{euclidean_std}[mm]'.format(euclidean_avg=round(euclidean_avg, 3), euclidean_std=round(euclidean_std, 3)), fontproperties=my_font, fontsize=10)
    plt.xlabel('测试次数', fontproperties=my_font, fontsize=12)
    plt.ylabel('欧式距离[mm]', fontproperties=my_font, fontsize=12)
    plt.xlim(-5, len(euclidean)+5)
    plt.ylim(-10, 10)
    x_major_locator = MultipleLocator(20)
    y_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('模板定位-开环验证位置定位精度测试结果.png')
    plt.show()

    figure2 = plt.figure(figsize=(15, 4))
    plt.suptitle('模板定位-开环验证姿态定位精度测试结果', weight='bold', fontproperties=my_font, fontsize=14)
    ax1 = figure2.add_subplot(1, 3, 1)
    ax1.set_title('Rx精度', fontproperties=my_font, fontsize=12)
    ax1.grid()
    ax1.plot(Rx_norm[1:], 'b-', linewidth=3, label="Measured Rx")
    ax1.plot([0, len(Rx_norm[1:])], [Rx_avg, Rx_avg], 'g--', linewidth=3, label="Average Measured Rx")
    ax1.plot([0, len(Rx_norm[1:])], [0, 0], 'r-.', linewidth=3, label="Teach Point")
    ax1.text(len(Rx_norm[1:])/2, 1, '平均Rx: {Rx_avg}[deg]\n标准差：{Rx_std}[deg]'.format(Rx_avg=round(Rx_avg, 3), Rx_std=round(Rx_std, 3)), fontproperties=my_font, fontsize=10)
    ax1.set_xlabel('测试次数', fontproperties=my_font, fontsize=12)
    ax1.set_ylabel('Rx[deg]', fontproperties=my_font, fontsize=12)
    ax1.set_xlim((-5, len(Rx_norm[1:])+5))
    ax1.set_ylim((-10, 10))
    ax1.xaxis.set_major_locator(x_major_locator)
    ax1.yaxis.set_major_locator(y_major_locator)
    ax1.legend(loc='best')

    ax2 = figure2.add_subplot(1, 3, 2)
    ax2.set_title('Ry精度', fontproperties=my_font, fontsize=12)
    ax2.grid()
    ax2.plot(Ry_norm[1:], 'b-', linewidth=3, label="Measured Ry")
    ax2.plot([0, len(Ry_norm[1:])], [Ry_avg, Ry_avg], 'g--', linewidth=3, label="Average Measured Ry")
    ax2.plot([0, len(Ry_norm[1:])], [0, 0], 'r-.', linewidth=3, label="Teach Point")
    ax2.text(len(Ry_norm[1:])/2, 1, '平均Ry: {Ry_avg}[deg]\n标准差：{Ry_std}[deg]'.format(Ry_avg=round(Ry_avg, 3), Ry_std=round(Ry_std, 3)), fontproperties=my_font, fontsize=10)
    ax2.set_xlabel('测试次数', fontproperties=my_font, fontsize=12)
    ax2.set_ylabel('Ry[deg]', fontproperties=my_font, fontsize=12)
    ax2.set_xlim((-5, len(Ry_norm[1:])+5))
    ax2.set_ylim((-10, 10))
    ax2.xaxis.set_major_locator(x_major_locator)
    ax2.yaxis.set_major_locator(y_major_locator)
    ax2.legend(loc='best')

    ax3 = figure2.add_subplot(1, 3, 3)
    ax3.set_title('Rz精度', fontproperties=my_font, fontsize=12)
    ax3.grid()
    ax3.plot(Rz_norm[1:], 'b-', linewidth=3, label="Measured Rz")
    ax3.plot([0, len(Rz_norm[1:])], [Rz_avg, Rz_avg], 'g--', linewidth=3, label="Average Measured Rz")
    ax3.plot([0, len(Rz_norm[1:])], [0, 0], 'r-.', linewidth=3, label="Teach Point")
    ax3.text(len(Rz_norm[1:])/2, 1, '平均Rz: {Rz_avg}[deg]\n标准差：{Rz_std}[deg]'.format(Rz_avg=round(Rz_avg, 3), Rz_std=round(Rz_std, 3)), fontproperties=my_font, fontsize=10)
    ax3.set_xlabel('测试次数', fontproperties=my_font, fontsize=12)
    ax3.set_ylabel('Rz[deg]', fontproperties=my_font, fontsize=12)
    ax3.set_xlim((-5, len(Rz_norm[1:])+5))
    ax3.set_ylim((-10, 10))
    ax3.xaxis.set_major_locator(x_major_locator)
    ax3.yaxis.set_major_locator(y_major_locator)
    ax3.legend(loc='best')
    plt.tight_layout()
    plt.savefig('模板定位-开环验证姿态定位精度测试结果.png')
    plt.show()
