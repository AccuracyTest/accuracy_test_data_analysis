import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


def ReadFile(filename):
    path = './Data/'
    f = open(path + filename)
    lines = f.readlines()
    return lines


def Collating(lines):
    RobotComponents = []
    TimeStamps = []

    for line in lines:
        line = line.strip().split()
        robotcomponent = str(line[0])
        timeStamp = str(line[1])
        currentTime = 0
        currentTime = float(timeStamp)

        TimeStamps.append(currentTime)
        RobotComponents.append(robotcomponent)

    begining = TimeStamps[0]
    TimeStamps = [element - begining for element in TimeStamps]

    Names_RobotComponent = []
    Names_RobotComponent.append("ARM")
    Names_RobotComponent.append("Camera")
    Names_RobotComponent.append("EventBegin")

    return RobotComponents, TimeStamps, Names_RobotComponent


def Calculate_time_for_vision(lines):
    vision_time = []
    for i in range(len(lines)-1):
        lines[i] = lines[i].strip().split()
        robotcomponent = str(lines[i][0])
        if(robotcomponent == 'Camera'):
            timeStamp = str(lines[i][1])
            tmp = lines[i+1].strip().split()
            timeStamp_next = str(tmp[1])
            currentTime = float(timeStamp)

            nextTime = float(timeStamp_next)
            vision_time.append(nextTime - currentTime)
    # print(vision_time)
    return vision_time


def Time_Gannt(RobotComponents, TimeStamps, Names_RobotComponent):
    colorNames = []
    colorNames.append('tab:blue')
    colorNames.append('tab:orange')
    colorNames.append('tab:green')
    colorNames.append('tab:red')

    figure, ax = plt.subplots(figsize=(8, 6))

    for i in range(len(Names_RobotComponent)):
        name_RobotComponent = Names_RobotComponent[i]
        Times = []
        for j in range(len(RobotComponents)-1):
            robotConponent = RobotComponents[j]
            timeStamp_current = TimeStamps[j]
            timeStamp_next = TimeStamps[j+1]
            time = timeStamp_next - timeStamp_current

            if robotConponent == name_RobotComponent:
                time = (timeStamp_current, timeStamp_next - timeStamp_current)
                Times.append(time)

        ax.broken_barh(Times, (i, 1), label=name_RobotComponent, facecolors=(colorNames[i]))

    font1 = {'family': 'Times New Roman', 'weight': 'bold', 'style': 'normal', 'size': 15}

    ax.set_xlabel("Times [seconds]", font1)
    ax.set_ylabel("Robot Components", font1)

    y_pos = []
    for i in range(len(Names_RobotComponent)):
        y_pos.append(0.5 + float(i))
    # print("y_pos: ", y_pos)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(Names_RobotComponent, font=font1)

    plt.tick_params(labelsize=15)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    [label.set_fontstyle('italic') for label in labels]
    plt.title("Perfomances of the Hybrid-Robot", font1)
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("模板定位-闭环验证机器人各部件用时统计.png")
    plt.show()


def histogram(data):

    data_avg = np.mean(data)
    data_std = np.std(data)

    font1 = {'family': 'Times New Roman', 'weight': 'bold', 'style': 'normal', 'size': 15}
    font2 = {'family': 'Times New Roman', 'weight': 'bold', 'style': 'normal', 'size': 10}
    figure, ax = plt.subplots(figsize=(5, 4))
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['axes.unicode_minus'] = False
    hist, bins = np.histogram(data, bins=10, range=(0, 5))
    plt.plot(bins[:-1], hist, linewidth=3)
    plt.text(1.5, 40, 'Average Time Consumption: {data_avg}[sec]\nStandard Deviation: {data_std}[sec]'.format(data_avg=round(data_avg, 3), data_std=round(data_std, 3)), font2)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(20))
    plt.xlabel("Time consumption for calculation[sec]", font1)
    plt.ylabel("Counts", font1)
    plt.tick_params(labelsize=15)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    [label.set_fontstyle('italic') for label in labels]
    plt.grid()
    plt.title("Histogram of Time Comsumption for Calculation", font1)
    plt.tight_layout()
    plt.savefig("模板定位-闭环验证视觉计算时间直方图统计.png")
    plt.show()

    return data_avg, data_std


if __name__ == "__main__":
    lines = ReadFile('Time_model_i5_closeloop_1130.txt')
    RobotComponents, TimeStamps, Names_RobotComponent = Collating(lines)
    vision_time = Calculate_time_for_vision(lines)

    Time_Gannt(RobotComponents, TimeStamps, Names_RobotComponent)
    histogram(vision_time)
