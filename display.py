# -*- coding: utf-8 -*-
'''
Created by ch yy, 08/12/2015
Use d3.js to display
'''
import numpy as np
import d3py
import pandas
import knn
def display_knn():
    '''
    用D3.JS展示Knn算法的运行结果
    :return:
    '''
    testNum,errorRate, errorCount, classifierData, realData = knn.displayData(
        '/home/ch/pycharm_code/analytics_edx_data/edx_a.csv');
    x = np.linspace(0,testNum,testNum)
    df = pandas.DataFrame({
    'x' : x,
    'y' : classifierData[:testNum],
    'z' : realData[:testNum],
    })

    print "testNummber = %d \n" % testNum, "error rate : %f \n" % (errorCount/float(testNum)), "error count：%d \n" % errorCount

    with d3py.PandasFigure(df, 'disply_knn', width=20000, height=200,port = 9999) as fig:
        fig += d3py.geoms.Line('x', 'y', stroke='BlueViolet')
        fig += d3py.geoms.Line('x', 'z', stroke='DeepPink')
        fig += d3py.xAxis('x', label="test number")
        fig += d3py.yAxis('y', label="test label")
        fig.show()