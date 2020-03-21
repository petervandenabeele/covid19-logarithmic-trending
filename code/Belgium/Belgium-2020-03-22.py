# WORK IN PROCESS BELGIUM 22 March 2020
# Copyright Peter Vandenabeele and Kris Peeters
# Licensed under BSD license (see below)
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import log, exp, pow
import numpy as np
import pandas as pd


# Set-up the data
day_of_march  = [14, 15, 16, 17, 18, 19, 20, 21]
day_of_march_future = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

hosp = [97, 163, 252, 361, 496, 634, 837, 1089]
ICU = [24, 33, 53, 79, 100, 130, 164, 238]
deceased = [4, 4, 5, 10, 14, 21, 37, 67]

log2_hosp = [log(x, 2) for x in hosp if x]
log2_ICU = [log(x, 2) for x in ICU if x]
log2_deceased = [log(x, 2) for x in deceased if x]

# Average "doubling" time over last 2 data points
last_log2_diff_hosp = log2_hosp[-1] - log2_hosp[-2]
last_log2_diff_ICU = log2_ICU[-1] - log2_ICU[-2]
average_last_log2_diff = (last_log2_diff_hosp + last_log2_diff_ICU)/2
print("Average doubling days = %.2f" % (1/average_last_log2_diff))


# Fitting Polynomial Regression to the dataset
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

X = [[x] for x in day_of_march]
X_ = [[x] for x in day_of_march_future]
y = log2_hosp
trendline_dates = [[21],[22],[23],[24],[25]]
#trendline_dates = X_ # use this to see all trendline values, also in the past

poly_1 = PolynomialFeatures(degree = 1)
X_poly_1 = poly_1.fit_transform(X)

poly_1.fit(X_poly_1, y)
lin2_1 = LinearRegression()
lin2_1.fit(X_poly_1, y)

trend_1 = [pow(2, x) for x in lin2_1.predict(poly_1.fit_transform(X_))]

log2_hosp_trend_1 = lin2_1.predict(poly_1.fit_transform(trendline_dates))
print(f"Days of March:     {trendline_dates}")
print(f"Trendline numbers:  {[int(pow(2, x)) for x in log2_hosp_trend_1]}")


# Prepare the plot
figure(num=1, figsize=(10, 8))
plt.yscale("log")

values = [10, 25, 50, 100, 200, 400, 600, 800, 1000, 1500, 2000]
plt.yticks(values, ['%d' % val for val in values])

plt.plot(X_, trend_1, color = 'blue', dashes=[2, 4], label="hospitlisations trendline")
plt.plot(day_of_march, hosp, 's-', label="hospitalisations")
plt.plot(day_of_march, ICU, 's-', label="ICU")
#plt.plot(day_of_march, deceased, 's-', label="deceased")

plt.xlabel("day of March")
plt.ylabel("Total numbers")
plt.title("BELGIUM hospitalisation, ICU; \n 22 March The trendline IS NOT A PREDICTION ! ")
plt.legend()
plt.show()
