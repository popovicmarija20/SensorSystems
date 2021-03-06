from numpy import mean
from matplotlib import pyplot

measurements = [90.208336,
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

measurements_freq_2 = list()
measurements_freq_3 = list()


for i in range(0, len(measurements), 2):
    measurements_freq_2.append(measurements[i])


for i in range(0, len(measurements), 3):
    measurements_freq_3.append(measurements[i])


thresholds = [0.0, 0.2, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0]



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


################
# % REDUCED TRANSMISSIONS - FREQUENCY 1
################


pyplot.subplot(xlabel='Threshold', ylabel='% of reduced transmissions - every day frequency ',
               title='Data for Bassel daily average air humidity from January 2010 - February 2010')
pyplot.plot(thresholds, reduced_transmissions(measurements, thresholds, 1),
            color='red', label='Linear Prediction', marker='.')
pyplot.plot(thresholds, reduced_transmissions(measurements, thresholds, 2),
            color='green', label='Moving Average - 2', marker='.')
pyplot.plot(thresholds, reduced_transmissions(measurements, thresholds, 3),
            color='blue', label='Moving Average - 3', marker='.')
pyplot.legend(loc='best')
pyplot.show()


################
# % REDUCED TRANSMISSIONS - FREQUENCY 2
################


pyplot.subplot(xlabel='Threshold', ylabel='% of reduced transmissions - every second day frequency',
               title='Data for Bassel daily average air humidity from January 2010 - February 2010')
pyplot.plot(thresholds, reduced_transmissions(measurements_freq_2, thresholds, 1),
            color='red', label='Linear Prediction', marker='.')
pyplot.plot(thresholds, reduced_transmissions(measurements_freq_2, thresholds, 2),
            color='green', label='Moving Average - 2', marker='.')
pyplot.plot(thresholds, reduced_transmissions(measurements_freq_2, thresholds, 3),
            color='blue', label='Moving Average - 3', marker='.')
pyplot.legend(loc='best')
pyplot.show()


################
# % REDUCED TRANSMISSIONS - FREQUENCY 3
################


pyplot.subplot(xlabel='Threshold', ylabel='% of reduced transmissions - every third day frequency',
               title='Data for Bassel daily average air humidity from January 2010 - February 2010')
pyplot.plot(thresholds, reduced_transmissions(measurements_freq_3, thresholds, 1),
            color='red', label='Linear Prediction', marker='.')
pyplot.plot(thresholds, reduced_transmissions(measurements_freq_3, thresholds, 2),
            color='green', label='Moving Average - 2', marker='.')
pyplot.plot(thresholds, reduced_transmissions(measurements_freq_3, thresholds, 3),
            color='blue', label='Moving Average - 3', marker='.')
pyplot.legend(loc='best')
pyplot.show()


#########
# MSE - FREQUENCY 1
#########


pyplot.subplot(xlabel='Threshold', ylabel='MSE every day frequency',
               title='Data for Bassel daily average air humidity from January 2010 - February 2010')
pyplot.plot(thresholds, MSE(measurements, thresholds, 1),
            color='red', label='Linear Prediction', marker='.')
pyplot.plot(thresholds, MSE(measurements, thresholds, 2),
            color='green', label='Moving Average - 2', marker='.')
pyplot.plot(thresholds, MSE(measurements, thresholds, 3),
            color='blue', label='Moving Average - 3', marker='.')
pyplot.legend(loc='best')
pyplot.show()


#########
# MSE - FREQUENCY 2
#########


pyplot.subplot(xlabel='Threshold', ylabel='MSE every second day frequency',
               title='Data for Bassel daily average air humidity from January 2010 - February 2010')
pyplot.plot(thresholds, MSE(measurements_freq_2, thresholds, 1),
            color='red', label='Linear Prediction', marker='.')
pyplot.plot(thresholds, MSE(measurements_freq_2, thresholds, 2),
            color='green', label='Moving Average - 2', marker='.')
pyplot.plot(thresholds, MSE(measurements_freq_2, thresholds, 3),
            color='blue', label='Moving Average - 3', marker='.')
pyplot.legend(loc='best')
pyplot.show()


#########
# MSE - FREQUENCY 3
#########


pyplot.subplot(xlabel='Threshold', ylabel='MSE every third day frequency',
               title='Data for Bassel daily average air humidity from January 2010 - February 2010')
pyplot.plot(thresholds, MSE(measurements_freq_3, thresholds, 1),
            color='red', label='Linear Prediction', marker='.')
pyplot.plot(thresholds, MSE(measurements_freq_3, thresholds, 2),
            color='green', label='Moving Average - 2', marker='.')
pyplot.plot(thresholds, MSE(measurements_freq_3, thresholds, 3),
            color='blue', label='Moving Average - 3', marker='.')
pyplot.legend(loc='best')
pyplot.show()