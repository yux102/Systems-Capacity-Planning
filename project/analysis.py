import matplotlib.pyplot as plt
from scipy.stats import stats, t

import math
import random

import numpy

from simulation import simulations

'''
while analysising, do not write file(departure and mrt)
And change mrt to float
'''

def expon_distribution_arrival(lamb):
    x = []
    y_expected = []
    binwidth = 0.5
    for i in range(10000):
        x.append(-(math.log(1 - random.random())) / lamb)
    plt.hist(x, bins=numpy.arange(min(x), max(x) + binwidth, binwidth))

    plt.axis([0, 15, 0, 1600])
    for i in range(15):
        lower = i - binwidth / 2
        upper = i + binwidth / 2
        y_expected.append((1600 * math.exp(-lamb * lower) - math.exp(-lamb * upper)))
    x1 = [i for i in range(15)]
    plt.plot(x1, y_expected, 'r-', 1)
    plt.grid(True)
    plt.show()

def expon_distribution_service(mu):
    x = []
    for i in range(10000):
        x.append(sum([(-(math.log(1 - random.random())) / mu) for i in range(3)]))
    plt.hist(x, 50)
    plt.axis([0, 12, 0, 1000])
    plt.grid(True)
    # x1 = [i for i in numpy.arange(0,12,0.1)]
    # y1 = [1000 * (- ((i * mu) **2) / 2 * math.exp(-mu * i) - mu * i * math.exp(-mu * i) + 1 - math.exp(-mu * i) )for i in numpy.arange(0,12,0.1)]
    # plt.plot(x1, y1)
    plt.show()


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*numpy.array(data)
    mean, se = numpy.mean(a), stats.sem(a)
    h = se * t._ppf((1 + confidence) / 2., len(a)- 1)
    return mean, mean - h, mean + h


if __name__ == '__main__':
    # expon_distribution_arrival(0.35)
    # expon_distribution_service(1)


    mode =  'random'
    arrival = 0.35#
    service = 1.0#
    m = 5#
    setup_time = 5.0#
    time_end = 10**4
    x =[]
    # x=numpy.arange(0.1, 50, 0.1)
    # x = range(50,10**4,100)
    y = []
    i = 0.1
    y1 = []



