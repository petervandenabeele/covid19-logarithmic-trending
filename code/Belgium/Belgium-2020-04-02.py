# BELGIUM 2 April 2020 (day 32)
# LINEAR + QUADRATIC trend line
# Copyright Peter Vandenabeele and Kris Peeters
# Licensed under BSD license (see below)

# UPDATE: now plotting hospitalisations as
# * ADMITTED: all patients that WHERE admitted
# * CURRENT: ADMITTED minus DISCHARGED

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import log, exp, pow
import numpy as np
import pandas as pd

# Set-up the data
country = "BELGIUM"

day_of_march  =   [ 14,  15,  16,  17,  18,  19,   20,   21,   22,   23,   24,   25,   26,   27,   28,   29,   30,   31,   32,   33]
hosp_discharged = [  1,   1,   1,  14,  31, 155,  240,  298,  340,  350,  410,  525,  653,  836, 1063, 1359, 1527, 1696, 2132, 2495]
hosp_current =    [ 97, 163, 252, 361, 496, 634,  837, 1089, 1380, 1643, 1859, 2152, 2652, 3042, 3717, 4138, 4524, 4940, 4995, 5376]
hosp_admitted =   [ 98, 164, 253, 372, 527, 789, 1077, 1387, 1720, 1993, 2269, 2677, 3305, 3878, 4780, 5497, 6051, 6636, 7127, 7871] # calculated
day_of_march_ICU  = day_of_march
ICU =             [ 24,  33,  53,  79, 100, 130,  164,  238,  290,  322,  381,  474,  605,  690,  789,  867,  927, 1021, 1088, 1144]


from operator import add
deceased_OLD =    [  4,   4,   5,  10,  14,  21,   37,   67,   75,   88,  122,  178,  220,  289,  353,  431,  513,  705]
redistribute =    [  2,   0,   0,   2,   2,   3,    5,    6,    8,    9,    7,   11,   10,    9,   20,   66,   32,    0]
# deceased = list(map(add, deceased_OLD, redistribute))
deceased =        [  6,   4,   5,   12, 16,  24,   42,   73,   83,   97,  129,  189,  230,  298,  373,  497,  545,  705,  828, 1011]

current_day = day_of_march[-1]

log2_hosp = [log(x, 2) for x in hosp_admitted]
log2_ICU =  [log(x, 2) for x in ICU]
log2_deceased = [log(x, 2) for x in deceased]

# Average "doubling" time over last 2 days (to average out daily noise)
# last_log2_diff_hosp = log2_hosp[-1] - log2_hosp[-3]
# last_log2_diff_ICU = log2_ICU[-1] - log2_ICU[-3]
# print("Hospitalisations doubling days = %.2f" % (2/last_log2_diff_hosp))
# print("ICU admissions   doubling days = %.2f" % (2/last_log2_diff_ICU))


# Fitting Polynomial Regression to the dataset
# ONLY USING THE LAST WEEK (LAST 7 days)
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

extrapolation_days = 4 # how many extrapolate in future
previous_days = 7 # how many days regression in past

X = [[x] for x in day_of_march[-previous_days:]]
first_future_day = current_day + 1
trendline_dates = [[x] for x in range(first_future_day, first_future_day + extrapolation_days)]
X_ = X + trendline_dates
y = log2_hosp[-previous_days:]
# print(f"Days of April:               {[(x[0] - 31) for x in trendline_dates]}")

# linear (degree 1)
poly_1 = PolynomialFeatures(degree = 1)
X_poly_1 = poly_1.fit_transform(X)

poly_1.fit(X_poly_1, y)
lin2_1 = LinearRegression()
lin2_1.fit(X_poly_1, y)

trend_1 = [pow(2, x) for x in lin2_1.predict(poly_1.fit_transform(X_))]

log2_hosp_trend_1 = lin2_1.predict(poly_1.fit_transform(trendline_dates))
# print(f"Trendline LINEAR numbers:    {[int(pow(2, x)) for x in log2_hosp_trend_1]}")

# quadratic (degree 2)
poly_2 = PolynomialFeatures(degree = 2)
X_poly_2 = poly_2.fit_transform(X)

poly_2.fit(X_poly_2, y)
lin2_2 = LinearRegression()
lin2_2.fit(X_poly_2, y)

trend_2 = [pow(2, x) for x in lin2_2.predict(poly_2.fit_transform(X_))]

log2_hosp_trend_2 = lin2_2.predict(poly_2.fit_transform(trendline_dates))
# print(f"Trendline QUADRATIC numbers: {[int(pow(2, x)) for x in log2_hosp_trend_2]}")


# Prepare the plot
figure(num=1, figsize=(10, 8))
plt.xlim(((day_of_march[0] - 0.5), (first_future_day + extrapolation_days - 0.5)))
# LIN
# plt.ylim((0,8000))
# values = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

#LOG
plt.yscale("log")
plt.ylim((20,10000))
values = [25, 50, 100, 200, 400, 600, 800, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 8000, 10000]

plt.yticks(values, ['%d' % val for val in values])

# plt.plot(X_, trend_1, color = 'green', dashes=[2, 4], label="hospitalisations trendline LINEAR")
# plt.plot(X_, trend_2, color = 'gray', dashes=[2, 4], label="hospitalisations trendline QUADRATIC")
plt.plot(day_of_march, hosp_current, 's-', color = 'gray', label="hospitalisations CURRENT")
plt.plot(day_of_march, hosp_admitted, 's-', color = 'C0', label="hospitalisations CUMULATIVE")
plt.plot(day_of_march_ICU, ICU, 's-', color = 'C1', label="ICU admissions CURRENT")
plt.plot(day_of_march, deceased, 's-', color = 'C2', label="deceased CUMULATIVE")


plt.xlabel("days since begin March")
plt.ylabel("Total numbers")
plt.title(f"\n* CALL TO ACTION * : Call a HOME ALONE person today ! #SocialConnection #PhysicalDistancing\n\n{country} hosp. admitted and current, ICU, deceased on {(current_day - 31)} April")
plt.legend()
plt.grid()
plt.show()
