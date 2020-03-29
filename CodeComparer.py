import os

import PySimpleGUI as sg
import psutil
import matplotlib.pyplot as plt
import numpy as np

program1 = []
program2 = []
parallel = []
sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Insert two python algorithm files')],

          [sg.Text('File 1 /Algo 1')],
          [sg.Input(), sg.FileBrowse()],
          [sg.Text('File 2 /Algo 2')],
          [sg.Input(), sg.FileBrowse()],
          [sg.Button('Begin Comparison'), sg.Button('Cancel')], ]

# Create the Window
window = sg.Window('Algorithm Compare', layout)


# Event Loop to process "events" and get the "values" of the inputs

def runner(val, i):
    print("********************************This is for the file************************************" + val)
    metrics = []
    os.system(val)
    pid = os.getpid()
    print(pid)
    py = psutil.Process(pid)
    temp = py.memory_full_info()
    cput = psutil.cpu_times_percent(interval=0.4, percpu=False).user
    print("How much cpu is used : " + str(psutil.cpu_times_percent(interval=0.4, percpu=False)))  # 1
    metrics.append(cput)
    print('Memory percent : ' + str(py.memory_percent()))  # 2
    metrics.append(py.memory_percent())
    disk = psutil.disk_usage('/').used
    print('Disk Usage' + str(psutil.disk_usage('/').used))  # 3
    metrics.append(disk)
    memoryUse = py.memory_info()[0] / 2. ** 30
    print('memory use:', memoryUse, "GB")  # 4
    metrics.append(memoryUse)
    memoryUse = py.memory_info()[1] / 2. ** 30
    print('memory (vms):', memoryUse, "GB")  # 5
    metrics.append(memoryUse)
    print('page faults' + str(temp[2]))  # 6
    metrics.append(temp[2])
    if (i == 1):
        program1 = metrics.copy()
        print(program1)
        return program1
    else:
        program2 = metrics.copy()
        print(program2)
        return program2

def runnerpal(val, val2):
    print("********************************Parallel************************************")
    metrics = []
    cmd = 'python ' + val
    cmd += ' && python ' + val2
    os.system(cmd)
    print(cmd)
    pid = os.getpid()
    print(pid)
    py = psutil.Process(pid)
    temp = py.memory_full_info()
    cput=psutil.cpu_times_percent(interval=0.4, percpu=False).user
    print("How much cpu is used : " + str(psutil.cpu_times_percent(interval=0.4, percpu=False).user))  # 1
    metrics.append(cput)
    print('Memory percent : ' + str(py.memory_percent()))  # 2
    metrics.append(py.memory_percent())
    disk=psutil.disk_usage('/').used
    print('Disk Usage' + str(psutil.disk_usage('/').used))  # 3
    metrics.append(disk)
    memoryUse = py.memory_info()[0] / 2. ** 30
    print('memory use:', memoryUse, "GB")  # 4
    metrics.append(memoryUse)
    memoryUse = py.memory_info()[1] / 2. ** 30
    print('memory (vms):', memoryUse, "GB")  # 5
    metrics.append(memoryUse)
    print('page faults' + str(temp[2]))  # 6
    metrics.append(temp[2])
    parallel = metrics.copy()
    return parallel

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()/2
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def makegraph():
    #print('here')
    objects = ('Program 1', 'Program 2', 'P1 and p2 in Parallel')
    title = ['1) CPU usage',
             '2) Memory usage',
             '3) Hard drive usage',
             '4) RSS',
             '5) VMS',
             '6) Number of page faults']
    y_pos = np.arange(len(objects))


    index=1
    for i in range(6):

        local = []
        #print(i)
        #print('p1: '+str(program1[i]))
        #print('p2: '+str(program2[i]))
        #print('parallel: '+str(parallel[i]))

        plt.ylim()
        local.append(program1[i])
        local.append(program2[i])
        local.append(parallel[i])
        ax=plt.subplot(3, 2, index)
        rect =plt.bar(y_pos, local, align='center', alpha=0.9)
        plt.xticks(y_pos, objects)
        plt.ylabel(title[i])

        autolabel(rect,ax)
        #plt.title('Comparing the algorithms')

        index+=1

    return plt


while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    ##print('File number 1 ', values[0])
    #print('File number 2 ', values[1])
    program1=runner(values[0], 1)
    program2=runner(values[1], 2)
    parallel=runnerpal(values[0], values[1])

    res=makegraph()
    res.show()
    ##loadresults()

window.close()
