from beta_integration import *


# 单个小火焰解积分
def single_solution_integration(solution, x_name, x_ave, x_var, y_names):
    x = solution[x_name]  # Z的值

    f = np.empty((len(y_names), len(x)))

    for i, name in enumerate(y_names):
        if name.endswith('Variance'):
            f[i, :] = np.square(solution[name[:-8]])
        else:
            f[i, :] = solution[name]

    integration = beta_integration_table(f, x, x_ave, x_var)

    return integration


# 多个小火焰解(合并后)积分（针对Z）
def multiple_solution_integration(multi_solution, x_name, x_ave, x_var, y_names):
    numFlamelet = multi_solution.shape[0] // 201

    table = np.empty((y_names.size, x_ave.size, x_var.size, numFlamelet))

    for i in range(numFlamelet):
        solution = multi_solution[201 * i: 201 * (i + 1)]
        table[:, :, :, i] = single_solution_integration(solution, x_name, x_ave, x_var, y_names)

    return table


# 多个小火焰解(合并后)积分（针对C），采用beta积分
def table_integration_beta(f, x, x_ave, x_var):
    table = beta_integration_table(f, x, x_ave, x_var)

    return table


# 多个小火焰解(合并后)积分（针对PV和gamma），采用delta积分
def table_integration_delta(f, x, x_ave):
    table = delta_integration(f, x, x_ave)

    return table
