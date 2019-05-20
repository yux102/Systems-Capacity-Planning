import simulation
# Read the file num_tests.txt.txt to determine the number of tests
with open("input/num_tests.txt", "r") as file:
    num_test = int(file.readline())
file.close()

for i in range(1, num_test + 1):
    #get mode
    with open("input/mode_" + str(i) + ".txt", "r") as modefile:
        mode = modefile.readline()
    modefile.close()

    #get parameter
    with open("input/para_" + str(i) + ".txt", "r") as parafile:
        m = int(parafile.readline())
        setup_time = float(parafile.readline())
        delayedoff_time = float(parafile.readline())
        if mode == 'random':
            time_end = float(parafile.readline())
    parafile.close()


    #get arrival
    with open("input/arrival_" + str(i) + ".txt", "r") as arrivalfile:
        if mode == 'trace':
            arrival = [float(i.strip()) for i in arrivalfile.readlines()]
        else:
            arrival = float(arrivalfile.readline().strip())
    arrivalfile.close()

    #get service
    with open("input/service_" + str(i) + ".txt", "r") as servicefile:
        if mode == 'trace':
            service = [float(i.strip()) for i in servicefile.readlines()]
        else:
            service = float(servicefile.readline().strip())
    servicefile.close()


    # call simulation function
    if mode == 'trace':
        simulation.simulations(i, mode,arrival, service, m, setup_time, delayedoff_time)
    else:
        simulation.simulations(i, mode, arrival, service, m, setup_time, delayedoff_time, time_end, 1)



