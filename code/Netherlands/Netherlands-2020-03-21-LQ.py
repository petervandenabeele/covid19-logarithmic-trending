# NETHERLANDS 21 March 2020
# LINEAR + QUADRATIC trend line
# Copyright Peter Vandenabeele and Kris Peeters
# Licensed under BSD license (see below)
# Sources:
# https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus
# ICU : NOS drawing
# 21 March : https://www.nu.nl/coronavirus/6036016/flinke-stijging-ziekenhuisopnamen-in-nederland.html
# Correction on 21 March of the number of ICU admissions

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import log, exp, pow
import numpy as np
import pandas as pd
 
# Set-up the data
country = "NETHERLANDS"
day_of_march  = [14, 15, 16, 17, 18, 19, 20, 21]
day_of_march_ICU  = [16, 17, 18, 19, 20, 21]

hosp = [136, 162, 205, 314, 408, 489, 643, 836]
ICU = [96, 135, 178, 210, 281, 354]
deceased = [12, 20, 24, 43, 58, 76, 106, 136]

log2_hosp = [log(x, 2) for x in hosp]
log2_ICU = [log(x, 2) for x in ICU]
log2_deceased = [log(x, 2) for x in deceased]

# Average "doubling" time over last 2 data points
last_log2_diff_hosp = log2_hosp[-1] - log2_hosp[-2]
last_log2_diff_ICU = log2_ICU[-1] - log2_ICU[-2]
average_last_log2_diff = (last_log2_diff_hosp + last_log2_diff_ICU)/2
print("Average doubling days = %.2f" % (1/average_last_log2_diff))


# Fitting Polynomial Regression to the dataset
# ONLY USING THE LAST WEEK (LAST 7 days)
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

extrapolation_days = 4 # how many extrapolate in future
previous_days = 7 # how many days regression in past

X = [[x] for x in day_of_march[-previous_days:]]
first_future_day = day_of_march[-1] + 1
trendline_dates = [[x] for x in range(first_future_day, first_future_day + extrapolation_days)]
X_ = X + trendline_dates
y = log2_hosp[-previous_days:]
print(f"Days of March:               {trendline_dates}")

# linear (degree 1)
poly_1 = PolynomialFeatures(degree = 1)
X_poly_1 = poly_1.fit_transform(X)

poly_1.fit(X_poly_1, y)
lin2_1 = LinearRegression()
lin2_1.fit(X_poly_1, y)

trend_1 = [pow(2, x) for x in lin2_1.predict(poly_1.fit_transform(X_))]

log2_hosp_trend_1 = lin2_1.predict(poly_1.fit_transform(trendline_dates))
print(f"Trendline LINEAR numbers:    {[int(pow(2, x)) for x in log2_hosp_trend_1]}")

# quadratic (degree 2)
poly_2 = PolynomialFeatures(degree = 2)
X_poly_2 = poly_2.fit_transform(X)

poly_2.fit(X_poly_2, y)
lin2_2 = LinearRegression()
lin2_2.fit(X_poly_2, y)

trend_2 = [pow(2, x) for x in lin2_2.predict(poly_2.fit_transform(X_))]

log2_hosp_trend_2 = lin2_2.predict(poly_2.fit_transform(trendline_dates))
print(f"Trendline QUADRATIC numbers: {[int(pow(2, x)) for x in log2_hosp_trend_2]}")


# Prepare the plot
figure(num=1, figsize=(10, 8))
plt.yscale("log")

values = [10, 25, 50, 100, 200, 400, 600, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
plt.yticks(values, ['%d' % val for val in values])

plt.plot(X_, trend_1, color = 'green', dashes=[2, 4], label="hospitlisations trendline LINEAR")
plt.plot(X_, trend_2, color = 'gray', dashes=[2, 4], label="hospitlisations trendline QUADRATIC")
plt.plot(day_of_march, hosp, 's-', label="hospitalisations")
plt.plot(day_of_march_ICU, ICU, 's-', label="ICU")
#plt.plot(day_of_march, deceased, 's-', label="deceased")

plt.xlabel("day of March")
plt.ylabel("Total numbers")
plt.title(f"{country} hospitalisation, ICU on 21 March\nThe trendline IS NOT A PREDICTION ! ")
plt.legend()
plt.show()
