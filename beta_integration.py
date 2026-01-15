import numpy as np
import scipy as sp
from scipy.interpolate import interp1d
from scipy.stats import beta


# 计算Beta_pdf的系数a和b
def beta_coef(ave, var):
    a = ave * (1. / var - 1.)
    b = (1. - ave) * (1. / var - 1.)

    return a, b


# 计算Beta_pdf的积分(牛顿-莱布尼茨公式)
def beta_integration_analytic(f, x, B, CDF0, CDF1):
    c0 = np.zeros(x.size)
    c1 = np.zeros(x.size)

    for i in range(x.size - 1):
        cl1 = (f[i + 1] - f[i]) / (x[i + 1] - x[i])  #
        cl0 = f[i] - cl1 * x[i]  #

        c0[i] -= cl0
        c0[i + 1] += cl0

        c1[i] -= cl1  #
        c1[i + 1] += cl1

    c1 *= B

    return np.sum(c0 * CDF0 + c1 * CDF1)  #


# 计算Delta积分
def delta_integration(f, x, x_ave):
    y = interp1d(x, f, kind='linear')

    return y(x_ave)


# 计算Bimodal积分
def bimodal_integration(f, x_ave):
    return f[0] * (1. - x_ave) + f[-1] * x_ave


# 计算Beta积分（首先判断x_ave和x_var在不在0~1范围内）
def beta_integration(f, x, x_ave, x_var, B, CDF0, CDF1, EPS):
    if x_ave < EPS:
        return f[0]
    elif x_ave > 1. - EPS:
        return f[-1]
    elif x_var < EPS:
        return delta_integration(f, x, x_ave)
    elif x_var > 1. - EPS:
        return bimodal_integration(f, x_ave)
    else:
        return beta_integration_analytic(f, x, B, CDF0, CDF1)


# 计算Beta积分的系数（用于计算Beta积分）
def beta_integration_coef(x, x_ave, x_var):
    a, b = beta_coef(x_ave, x_var)

    rv0 = beta(a, b)
    cdf0 = rv0.cdf(x)
    B0 = sp.special.beta(a, b)

    rv1 = beta(a + 1., b)
    cdf1 = rv1.cdf(x)
    B1 = sp.special.beta(a + 1, b)

    B = B1 / B0

    return B, cdf0, cdf1


# # 计算Beta积分的系数（多个）
def beta_integration_coef_table(x, x_ave, x_var, EPS):
    B = np.empty((x_ave.size, x_var.size))
    CDF0 = np.empty((x_ave.size, x_var.size, x.size))
    CDF1 = np.empty((x_ave.size, x_var.size, x.size))

    for j, ave in enumerate(x_ave):
        for k, var in enumerate(x_var):
            if EPS < ave < 1. - EPS and EPS < var < 1. - EPS:
                B[j, k], CDF0[j, k, :], CDF1[j, k, :] = beta_integration_coef(x, ave, var)

    return B, CDF0, CDF1


# 计算Beta积分（表格）
def beta_integration_table(f, x, x_ave, x_var, EPS=1.e-9):
    f_flatten = np.reshape(f, (-1, x.size), order='F')

    variable_number = f_flatten.shape[0]

    table_flatten = np.empty((variable_number, x_ave.size, x_var.size))

    B, CDF0, CDF1 = beta_integration_coef_table(x, x_ave, x_var, EPS)

    for i, v in enumerate(f_flatten):
        for j, ave in enumerate(x_ave):
            for k, var in enumerate(x_var):
                table_flatten[i, j, k] = beta_integration(v, x, ave, var, B[j, k], CDF0[j, k, :], CDF1[j, k, :], EPS)

    table = np.reshape(table_flatten, f.shape[:-1] + (x_ave.size, x_var.size), order='F')

    return table
