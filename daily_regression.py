import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

complaints_df = pd.read_csv("smc_data.csv")
weather_df = pd.read_csv("weather_data.csv")

complaints_df["date"] = [time.strftime("%Y-%m-%d", time.strptime(dt, "%c")) for dt in complaints_df["date & time"]]

df = pd.DataFrame()

df["date"] = weather_df["date"]

daily_complaints = pd.DataFrame(complaints_df["date"].value_counts()).reset_index()
daily_complaints.columns = ["date", "daily complaints"]

df = df.merge(daily_complaints, on="date")

df = df.merge(weather_df, on="date")

X = df[["average_temp", "average_wind", "precipitation"]]
Y = df["daily complaints"]

X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()

print(f"\n{model.summary()}")

corr_matrix = df.corr()

print(f"\nCorrelation matrix:\n{corr_matrix}\n")

cmap = sns.diverging_palette(230, 20, as_cmap=True)
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, cmap=cmap, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.show()


#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:       daily complaints   R-squared:                       0.098
# Model:                            OLS   Adj. R-squared:                  0.094
# Method:                 Least Squares   F-statistic:                     20.53
# Date:                Fri, 08 Apr 2022   Prob (F-statistic):           1.22e-12
# Time:                        12:18:31   Log-Likelihood:                -1570.5
# No. Observations:                 568   AIC:                             3149.
# Df Residuals:                     564   BIC:                             3166.
# Df Model:                           3
# Covariance Type:            nonrobust
# =================================================================================
#                     coef    std err          t      P>|t|      [0.025      0.975]
# ---------------------------------------------------------------------------------
# const            -0.3239      0.725     -0.447      0.655      -1.747       1.100
# average_temp      0.0788      0.010      7.768      0.000       0.059       0.099
# average_wind      0.0283      0.012      2.353      0.019       0.005       0.052
# precipitation    -0.0003      0.002     -0.165      0.869      -0.004       0.004
# ==============================================================================
# Omnibus:                      234.185   Durbin-Watson:                   1.167
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):             1201.107
# Skew:                           1.780   Prob(JB):                    1.52e-261
# Kurtosis:                       9.170   Cond. No.                         403.
# ==============================================================================

# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

# Correlation matrix:
#                   daily complaints  average_temp  average_wind  precipitation
# daily complaints          1.000000      0.298952      0.044344       0.005069
# average_temp              0.298952      1.000000     -0.165350      -0.034605
# average_wind              0.044344     -0.165350      1.000000       0.232253
# precipitation             0.005069     -0.034605      0.232253       1.000000