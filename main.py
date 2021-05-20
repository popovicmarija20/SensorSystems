




from numpy import mean
import numpy as NP
from matplotlib import pyplot


measurements_temp = [4.7580285,
-0.80238795,
-0.8923881,
-3.1536381,
-3.3332217,
-2.0440547,
-0.046554774,
-0.3715546,
-1.6694713,
-3.2811384,
-4.1153045,
-2.1365545,
1.3096952,
1.6838619,
1.6767784,
2.466362,
6.3359447,
4.5805287,
2.060945,
1.701362,
4.181779,
2.4238617,
0.9626119,
3.233862,
2.7334452,
-0.3119713,
-1.8832213,
0.11136198,
2.3209453,
-0.44572136,
-2.1003048,
-2.0828047,
1.1596953,
4.892195,
4.284695,
4.9784455,
4.4646955,
2.8680289,
0.88177854,
2.0463622,
-2.5707214,
-2.4182215,
-1.0636381,
-1.3961382,
-1.0240546,
-1.8115548,
0.5751119,
3.3709452,
6.4826126,
4.975112,
2.749279,
4.5201116,
8.113862,
9.862613,
8.947612,
8.523862,
7.659696,
6.8567786,
8.741362
]



measurements_humid = [90.208336,
74.875,
71.25,
81.958336,
84.291664,
82.333336,
81.625,
84.083336,
82.583336,
87.5,
86.958336,
86.666664,
91.333336,
88.875,
84.625,
79.375,
78.791664,
86.25,
89.416664,
82.583336,
85.375,
88.25,
84.333336,
86.958336,
88.708336,
85.541664,
75.166664,
73,
76.125,
82.208336,
81.208336,
78.583336,
73.708336,
78.166664,
75.291664,
80.125,
81.958336,
90.25,
83.041664,
77.041664,
78.208336,
75.708336,
72.291664,
79.833336,
76.416664,
79.458336,
76.666664,
85.25,
82.916664,
88.125,
76.083336,
72.041664,
72.125,
71.875,
78.5,
71.875,
74.625,
66.666664,
62.75
]

measurements_temp_freq_2 = list()
measurements_temp_freq_3 = list()


measurements_humid_freq_2 = list()
measurements_humid_freq_3 = list()


for i in range(0, len(measurements_temp), 2):
    measurements_temp_freq_2.append(measurements_temp[i])
    measurements_humid_freq_2.append(measurements_humid[i])


for i in range(0, len(measurements_temp), 3):
    measurements_temp_freq_3.append(measurements_temp[i])
    measurements_humid_freq_3.append(measurements_humid[i])


thresholds_temp = [0.0, 0.2, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0]
thresholds_humid = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]


def reduced_transmissions(f_measurements, f_thresholds, MA):
    counters_list = list()
    for threshold in f_thresholds:
        counter = 0
        predictions = list()

        for i in range(0, MA):
            predictions.append(f_measurements[i])

        for i in range(MA, len(f_measurements) - MA):
            next_prediction = mean(predictions[-MA:])
            if abs(f_measurements[i] - next_prediction) > threshold:
                counter += 1
                predictions.append(f_measurements[i])
            else:
                predictions.append(next_prediction)

        counters_list.append(counter / len(f_measurements) * 100.0)
    return counters_list


def MSE(f_measurements, f_thresholds, MA):
    errors_list = list()

    for threshold in f_thresholds:
        predictions = list()
        thresh_errors = list()

        for i in range(0, MA):
            predictions.append(f_measurements[i])

        for i in range(MA, len(f_measurements) - MA):
            next_prediction = mean(predictions[-MA:])
            curr_error = f_measurements[i] - next_prediction

            if abs(curr_error) > threshold:
                predictions.append(f_measurements[i])
                thresh_errors.append(curr_error*curr_error)
            else:
                predictions.append(next_prediction)

        errors_list.append(mean(thresh_errors))

    return errors_list


def plotting_function_rt(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA, F):
    result = reduced_transmissions(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA)
    x = NP.array(list(map(lambda k: float(k.split(';')[0]), result.keys())))
    y = NP.array(list(map(lambda k: float(k.split(';')[1]), result.keys())))
    val = NP.array(list(result.values()))

    pyplot.xticks(NP.arange(NP.amin(x), NP.ceil(NP.amax(x)) + 1))
    pyplot.yticks(NP.arange(NP.amin(y), NP.ceil(NP.amax(y)) + 1))
    pyplot.scatter(x, y, c=val, s=100)
    pyplot.title(f'% reduced transmissions - Moving Average ' + str(MA) + ' Frequency Every ' + str(F) + ' day')
    pyplot.xlabel('Temperature thresholds')
    pyplot.ylabel('Humidity thresholds')
    pyplot.colorbar()
    pyplot.show()


def plotting_function_mse(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA, F):
    result = MSE(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA)
    x = NP.array(list(map(lambda k: float(k.split(';')[0]), result.keys())))
    y = NP.array(list(map(lambda k: float(k.split(';')[1]), result.keys())))
    val = NP.array(list(result.values()))

    pyplot.xticks(NP.arange(NP.amin(x), NP.ceil(NP.amax(x)) + 1))
    pyplot.yticks(NP.arange(NP.amin(y), NP.ceil(NP.amax(y)) + 1))
    pyplot.scatter(x, y, c=val, s=100)
    pyplot.title(f'MSE - Moving Average ' + str(MA) + ' Frequency Every ' + str(F) + ' day')
    pyplot.xlabel('Temperature thresholds')
    pyplot.ylabel('Humidity thresholds')
    pyplot.colorbar()
    pyplot.show()


################
# % REDUCED TRANSMISSIONS - FREQUENCY 1
################

plotting_function_rt(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 1, 1)
plotting_function_rt(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 2, 1)
plotting_function_rt(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 3, 1)

################
# % REDUCED TRANSMISSIONS - FREQUENCY 2
################

plotting_function_rt(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 1, 2)
plotting_function_rt(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 2, 2)
plotting_function_rt(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 3, 2)


################
# % REDUCED TRANSMISSIONS - FREQUENCY 3
################

plotting_function_rt(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 1, 3)
plotting_function_rt(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 2, 3)
plotting_function_rt(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 3, 3)

#########
# MSE - FREQUENCY 1
#########

plotting_function_mse(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 1, 1)
plotting_function_mse(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 2, 1)
plotting_function_mse(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 3, 1)


#########
# MSE - FREQUENCY 2
#########

plotting_function_mse(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 1, 2)
plotting_function_mse(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 2, 2)
plotting_function_mse(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 3, 2)

#########
# MSE - FREQUENCY 3
#########

plotting_function_mse(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 1, 3)
plotting_function_mse(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 2, 3)
plotting_function_mse(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 3, 3)