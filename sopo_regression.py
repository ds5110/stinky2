import time

import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm


df = pd.read_csv("./sample_data/merged_data.csv")

columns = ["average_temp", "average_wind", "WSF5", "sprague_miles", "portland_pipeline_miles", "south_portland_terminal_miles", "gulf_oil_miles", "global_miles", "citgo_miles", 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

X = df[columns]
X = sm.add_constant(X)

Y = df["daily complaints"]

model = sm.OLS(Y, X).fit()

print(f"\n{model.summary()}")

corr_matrix = df.corr()

print(f"\nCorrelation matrix:\n{corr_matrix}\n")

# cmap = sns.diverging_palette(230, 20, as_cmap=True)
# mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
# sns.heatmap(corr_matrix, mask=mask, cmap=cmap, center=0,
#             square=True, linewidths=.5, cbar_kws={"shrink": .5})
sns.pairplot(df, height=2.5) #, hue="daily complaints") #, palette="GnBu_d", diag_kind="kde", height=2.5)
# plt.show()
plt.savefig("sopo_scatterplot_matrix.png")


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



#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:       daily complaints   R-squared:                       0.098
# Model:                            OLS   Adj. R-squared:                  0.095
# Method:                 Least Squares   F-statistic:                     30.84
# Date:                Fri, 08 Apr 2022   Prob (F-statistic):           1.95e-13
# Time:                        21:17:30   Log-Likelihood:                -1570.5
# No. Observations:                 568   AIC:                             3147.
# Df Residuals:                     565   BIC:                             3160.
# Df Model:                           2
# Covariance Type:            nonrobust
# ================================================================================
#                    coef    std err          t      P>|t|      [0.025      0.975]
# --------------------------------------------------------------------------------
# const           -0.3184      0.723     -0.440      0.660      -1.739       1.102
# average_temp     0.0788      0.010      7.774      0.000       0.059       0.099
# average_wind     0.0279      0.012      2.380      0.018       0.005       0.051
# ==============================================================================
# Omnibus:                      234.465   Durbin-Watson:                   1.168
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):             1204.980
# Skew:                           1.782   Prob(JB):                    2.20e-262
# Kurtosis:                       9.182   Cond. No.                         285.
# ==============================================================================

# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

# Correlation matrix:
#                   daily complaints  average_temp  average_wind
# daily complaints          1.000000      0.298952      0.044344
# average_temp              0.298952      1.000000     -0.165350
# average_wind              0.044344     -0.165350      1.000000



#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:       daily complaints   R-squared:                       0.143
# Model:                            OLS   Adj. R-squared:                  0.124
# Method:                 Least Squares   F-statistic:                     7.702
# Date:                Fri, 15 Apr 2022   Prob (F-statistic):           1.95e-11
# Time:                        11:45:26   Log-Likelihood:                -1249.5
# No. Observations:                 473   AIC:                             2521.
# Df Residuals:                     462   BIC:                             2567.
# Df Model:                          10
# Covariance Type:            nonrobust
# =================================================================================================
#                                     coef    std err          t      P>|t|      [0.025      0.975]
# -------------------------------------------------------------------------------------------------
# const                            -0.8881      2.134     -0.416      0.678      -5.083       3.306
# average_temp                      0.0818      0.010      7.811      0.000       0.061       0.102
# average_wind                      0.0271      0.020      1.343      0.180      -0.013       0.067
# WSF5                              0.0041      0.008      0.528      0.598      -0.011       0.020
# WDF5                              0.0020      0.002      1.240      0.216      -0.001       0.005
# sprague_miles                   -21.7345     12.443     -1.747      0.081     -46.186       2.717
# portland_pipeline_miles          -0.3568      1.330     -0.268      0.789      -2.970       2.256
# south_portland_terminal_miles    34.1620     20.010      1.707      0.088      -5.160      73.484
# gulf_oil_miles                    0.0425      0.700      0.061      0.952      -1.332       1.417
# global_miles                    -11.5730      8.887     -1.302      0.193     -29.037       5.890
# citgo_miles                      -0.8424      1.461     -0.576      0.565      -3.714       2.030
# ==============================================================================
# Omnibus:                      191.937   Durbin-Watson:                   1.386
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):              939.132
# Skew:                           1.734   Prob(JB):                    1.17e-204
# Kurtosis:                       8.969   Cond. No.                     4.05e+04
# ==============================================================================



#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:       daily complaints   R-squared:                       0.170
# Model:                            OLS   Adj. R-squared:                  0.123
# Method:                 Least Squares   F-statistic:                     3.658
# Date:                Sun, 17 Apr 2022   Prob (F-statistic):           1.65e-08
# Time:                        15:07:47   Log-Likelihood:                -1242.0
# No. Observations:                 473   AIC:                             2536.
# Df Residuals:                     447   BIC:                             2644.
# Df Model:                          25
# Covariance Type:            nonrobust
# =================================================================================================
#                                     coef    std err          t      P>|t|      [0.025      0.975]
# -------------------------------------------------------------------------------------------------
# const                            -0.9346      2.212     -0.423      0.673      -5.281       3.412
# average_temp                      0.0706      0.012      6.020      0.000       0.048       0.094
# average_wind                      0.0280      0.021      1.358      0.175      -0.012       0.068
# WSF5                              0.0041      0.008      0.527      0.598      -0.011       0.020
# sprague_miles                   -22.8878     12.651     -1.809      0.071     -47.751       1.975
# portland_pipeline_miles          -0.1368      1.386     -0.099      0.921      -2.860       2.586
# south_portland_terminal_miles    36.7008     20.408      1.798      0.073      -3.406      76.807
# gulf_oil_miles                    0.0159      0.720      0.022      0.982      -1.399       1.431
# global_miles                    -13.0549      9.107     -1.434      0.152     -30.952       4.842
# citgo_miles                      -0.9626      1.519     -0.634      0.526      -3.947       2.022
# N                                 2.0390      0.825      2.472      0.014       0.418       3.660
# NNE                               0.6140      2.088      0.294      0.769      -3.489       4.717
# NE                                1.9270      1.342      1.436      0.152      -0.710       4.564
# ENE                               0.3839      0.807      0.476      0.635      -1.203       1.970
# E                                 1.7613      1.026      1.716      0.087      -0.255       3.778
# ESE                               0.8908      0.973      0.915      0.360      -1.021       2.803
# SE                                1.9123      0.781      2.449      0.015       0.378       3.447
# SSE                               1.7220      0.779      2.212      0.028       0.192       3.252
# S                                 0.5822      0.716      0.813      0.417      -0.826       1.990
# SSW                               1.9341      1.069      1.810      0.071      -0.166       4.035
# SW                                0.9869      0.771      1.280      0.201      -0.528       2.502
# WSW                               0.5713      1.111      0.514      0.607      -1.612       2.755
# W                                 0.5458      1.206      0.452      0.651      -1.825       2.917
# WNW                               1.2471      0.777      1.604      0.109      -0.281       2.775
# NW                                1.5279      0.802      1.906      0.057      -0.047       3.103
# NNW                               1.3867      1.276      1.087      0.278      -1.121       3.894
# ==============================================================================
# Omnibus:                      186.932   Durbin-Watson:                   1.414
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):              887.657
# Skew:                           1.693   Prob(JB):                    1.77e-193
# Kurtosis:                       8.794   Cond. No.                     2.03e+04
# ==============================================================================