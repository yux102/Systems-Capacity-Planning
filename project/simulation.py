
import math
import random

import numpy
from decimal import Decimal


all_service_time = []

'''
simulation function:

1. A parameter mode of string type. This parameter is to control whether your program will run simulation using randomly generated arrival and service times, or in trace driven mode. The value that the parameter mode can take is either random or trace.
2. A parameter arrival for supplying arrival information to the program. The meaning of arrival depends on mode. We will provide more information later on.
3. A parameter service for supplying service time information to the program. The meaning of service depends on mode. We will provide more information later on.
4. A parameter m which is the number of servers. This parameter is a positive integer.
5. A parameter setup_time for the setup time. This parameter is a positive floating point number.
6. A parameter delayedoff_time for the initial value of the countdown timer Tc. This parameter is a positive floating point number.
7. A parameter time_end which stops the simulation if the master clock exceeds this value. This parameter is only relevant when mode is random. This parameter is a positive floating point number.



'''
def simulations(i, mode, arrival, service, m, setup_time, delayedoff_time, time_end=999999,seed = 0):
    global rep
    rep = get_replication_sequence(seed)
    global num
    num = i
    # print(mode, arrival, service, m, setup_time, delayedoff_time, time_end)
    jobs, mrt = _simulations(mode, arrival, service, m, setup_time, delayedoff_time, time_end)
    return jobs, mrt

def _simulations(mode, arrival, service, m, setup_time, delayedoff_time, time_end):
    # server: OFF, SETUP, BUSY, DELAYEDOFF
    server = [('OFF', 0)] * m
    # server = [('DELAYEDOFF', 30), ('DELAYEDOFF', 27),('OFF',0)]
    INF = 9999999999
    master_clock = 10
    departure_time = []
    response_time = []
    current_job = 0
    # dispatcher:(10,1,M): arrival time is 10, server is 1, M for Marked (UM for UnMarked)
    dispatcher = []
    next_departure = INF
    next_arrive = 0
    job_list = []
    # event: 'A':Arrival, 'D':Departure, 'S': Setup, 'E': Delayedoff
    event = ['']
    while 1:
        if event[0] == 'A':
            server = sorted(server, key=lambda x: (x[0] == 'DELAYEDOFF', x[1]), reverse=True)
            #if there is at least one DELAYEDOFF server, set DELAYEDOFF server to BUSY
            if server[0][0] == 'DELAYEDOFF':
                for i in job_list:
                    if i[2] == server[0][1]:
                        job_list.remove(i)
                server = server[1:]
                server.append(('BUSY', master_clock + event[2]))
                job_list.append(('D', master_clock, master_clock + event[2]))

            elif server.count(('OFF', 0)):
                #if all server is OFF, set one to SETUP
                server.remove(('OFF', 0))
                server.append(('SETUP', setup_time + master_clock))
                dispatcher.append((master_clock, event[2], 'M'))
                job_list.append(('S', master_clock, setup_time + master_clock))

            else:
                #if all busy, put job at the end of dispatcher and UNMAKRED
                dispatcher.append((master_clock, event[2], 'UM'))

        elif event[0] == 'D':
            server.remove(('BUSY', master_clock))
            job_list = job_list[1:]
            # print('--D--:', event[1], master_clock)
            # get the job departure time and response time
            departure_time.append((event[1], master_clock))
            response_time.append(master_clock - event[1])

            if not len(dispatcher):
                #if on jobs waiting in dispatcher, then set server to DELAYEDOFF
                server.append(('DELAYEDOFF', delayedoff_time + master_clock))
                job_list.append(('E', master_clock, delayedoff_time + master_clock))
            else:
                #if there are jobs waiting in dispatcher, then get the first one
                server.append(('BUSY', master_clock + dispatcher[0][1]))
                job_list.append(('D', dispatcher[0][0], master_clock + dispatcher[0][1]))

                #if this job is MARKED:
                if dispatcher[0][2] == 'M':
                    flag = 0
                    # if there is a job is UNMARKED in dispatcher, set it to MARKED
                    for i in dispatcher:
                        if i[2] == 'UM':
                            dispatcher.append((i[0], i[1], 'M'))
                            dispatcher.remove(i)
                            flag = 1
                            break
                    if not flag:
                        #if none of jobs is UNMARKED, then set a SETUP server to OFF
                        server = sorted(server, key=lambda x: (x[0] == 'SETUP', x[1]), reverse=True)
                        for i in job_list:
                            if i[2] == server[0][1]:
                                job_list.remove(i)
                        server.append(('OFF', 0))
                        server = server[1:]
                dispatcher = dispatcher[1:]

        elif event[0] == 'S':
            server.remove(('SETUP', master_clock))
            job_list = job_list[1:]
            # server already SETUP, get the first job in dispatcher
            server.append(('BUSY', dispatcher[0][1] + master_clock))
            job_list.append(('D', dispatcher[0][0], dispatcher[0][1] + master_clock))
            # queue-1
            dispatcher = dispatcher[1:]

        elif event[0] == 'E':
            #countdown to 0, set the server OFF
            job_list = job_list[1:]
            server.remove(('DELAYEDOFF', master_clock))
            server.append(('OFF', 0))

        # print(master_clock, dispatcher, server, event)

        if arrival == [] and server.count(('OFF', 0)) == m:
            break
        elif master_clock >= time_end:
            break
        elif arrival == []:
            next_arrive = INF
        elif mode == 'trace':
            next_arrive = arrival[0]
        else:
            next_arrive = master_clock + get_arrival_time(arrival, current_job)


        if len(job_list):
            # print('job_list:  ',job_list)
            if len(job_list) > 1:
                job_list = sorted(job_list, key=lambda x: x[2])
            next_event = job_list[0]
            # print('next_event:  ',next_event)

            if next_arrive < next_event[2]:
                master_clock = next_arrive
                if mode =='random':
                    event = ("A", next_arrive, get_serivce_time(service, current_job))
                else:
                    event = ("A", next_arrive, service[current_job])
                    # print('service:', next_arrive, service[current_job])
                    arrival = arrival[1:]
                current_job += 1
            elif next_event[0] == 'D':
                event = ("D", next_event[1], next_event[2])
                interval = next_departure - master_clock
                master_clock = next_event[2]
            elif next_event[0] == 'S':
                event = ("S", next_event[1], next_event[2])
                master_clock = next_event[2]
            elif next_event[0] == 'E':
                event = ("E", next_event[1], next_event[2])
                master_clock = next_event[2]
        else:
            master_clock = next_arrive
            if mode == 'random':
                event = ("A", next_arrive, get_serivce_time(service, current_job))
            else:
                event = ("A", next_arrive, service[current_job])
                # print('service:', next_arrive, service[current_job])
                arrival = arrival[1:]
            current_job += 1

        # Write the departure time to file
        get_departure_time(departure_time)

    # if write file, use decimal
    mrt = Decimal(sum(response_time) / current_job).quantize(Decimal('.001'))

    # if generate mean_confidence_interval, use float
    # mrt = sum(response_time) / current_job

    # Write the mrt to file
    get_mean_response_time(mrt)

    # print(mrt, current_job)
    # print(job_list)

    return current_job, mrt



def get_arrival_time(lamb,num):
    random.seed(rep[num])
    a = -(math.log(1 - random.random())) / lamb
    return a


def get_serivce_time(mu, num):
    random.seed(rep[num])
    s = sum([ (-(math.log(1 - random.random())) / mu) for i in range(3)])
    all_service_time.append(s)
    return s



def get_departure_time(departure):
    with open("output/departure_" + str(num) + ".txt", "w") as file:
        for i in departure:
            file.write(str(Decimal(i[0]).quantize(Decimal('.001'))) + '\t' + str(Decimal(i[1]).quantize(Decimal('.001'))) +'\n')
    file.close()


def get_mean_response_time(mrt):
    with open("output/mrt_" + str(num) + ".txt", "w") as file:
        file.write(str(mrt))
    file.close()


def get_replication_sequence(seed):
    numpy.random.seed(seed)
    rep = numpy.random.rand(20000)
    return rep


