import os
import matplotlib.pyplot as plt
from flamelet_integration import *

# 指定Gamma和fL的值
Gamma = '1'    # (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 1)
fL    = '1'    # (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)

# 读取Combined_all.csv文件
multi_solution = np.genfromtxt(f'Flamelet/Gamma={Gamma}/fL={fL}/Combined_all.csv', names=True, delimiter=',')

# 设置目标文件夹FGM_3D，用于储存ZC_table文件
FGM_3D_folder = f'FGM_3D/Gamma={Gamma}/fL={fL}/'
os.makedirs(FGM_3D_folder, exist_ok=True)

# 定义对Z积分所需的参数
Z_name = 'Z'
Z_ave = np.linspace(0, 1, 51)
Z_var = np.linspace(0, 1, 6)
variable_Z = np.array(['T', 'H2', 'O2', 'H2O', 'H', 'O', 'OH', 'HO2', 'H2O2', 'AR',
                       'rho', 'Cps', 'alpha', 'mu', 'PV', 'SourcePV', 'psi', 'TE', 'AbsCoeff'])  # 19个被积分的标量

# 计算Z_st
Z_H1 = 0.025579 + 0.974421 * (1.008 * 2 / 18.015)
Z_O1 = 0.974421 * (15.999 * 1 / 18.015)
Z_H2 = float(Gamma) * (1.008 * 2 / 18.015)
Z_O2 = 0.444758 * (1 - float(Gamma)) + float(Gamma) * (15.999 * 1 / 18.015)
Consum_oxi = 0.025579 / 2.016 / 2 * 31.999 / 0.444758 / (1 - float(Gamma))
Z_H = (Z_H1 + Z_H2 * Consum_oxi) / (1 + Consum_oxi)
Z_O = (Z_O1 + Z_O2 * Consum_oxi) / (1 + Consum_oxi)
Z_st = (0.5 * (Z_H - Z_H2) / 1.008 - (Z_O - Z_O2) / 15.999) / (0.5 * (Z_H1 - Z_H2) / 1.008 - (Z_O1 - Z_O2) / 15.999)
print("Z_st = {:.6f}".format(Z_st))

# 对Z进行Beta积分,并保存结果
Z_table = multiple_solution_integration(multi_solution, Z_name, Z_ave, Z_var, variable_Z)
print(Z_table.shape)

# 定义对C积分所需的参数
PV_values = np.array([])
numFlamelet = multi_solution.shape[0] // 201
for i in range(numFlamelet):
    Z = multi_solution[201 * i: 201 * (i + 1)]['Z']
    PV = multi_solution[201 * i: 201 * (i + 1)]['PV']
    PV_index = np.argmin(np.abs(Z - Z_st))
    PV_value = PV[PV_index]
    PV_values = np.append(PV_values, PV_value)
PV_values = np.sort(PV_values)
C_values = (PV_values - PV_values.min()) / (PV_values.max() - PV_values.min())
C_ave = np.linspace(0, 1, 51)

# 对C进行Delta积分,并保存结果
ZC_table = table_integration_delta(Z_table, C_values, C_ave)

# ZC_table = np.zeros((19, 51, 6, 51))
# for i in range(ZC_table.shape[0]):
#     for j in range(ZC_table.shape[1]):
#         for k in range(ZC_table.shape[2]):
#             ZC_table[i, j, k, :] = Z_table[i, j, k, 0]

np.save(f'FGM_3D/Gamma={Gamma}/fL={fL}/ZC_table.npy', ZC_table)
print(ZC_table.shape)


# 绘制等高线图（验证制表正确性）
ZC_table = np.load(f'FGM_3D/Gamma={Gamma}/fL={fL}/ZC_table.npy')
Z = np.linspace(0, 1, 51)
C = np.linspace(0, 1, 51)
Z, C = np.meshgrid(Z, C)
plt.figure(figsize=(10, 8))
plt.contourf(C, Z, ZC_table[0, :, 0, :], levels=101, cmap=plt.cm.rainbow)  # 该函数期望数据按照(y, x)的顺序排列
plt.colorbar()
plt.title('3D_Table Results (51×51)', fontsize=14)
plt.xlabel('Z', fontsize=12)
plt.ylabel('C', fontsize=12)
plt.grid(linestyle='--', linewidth=1)
plt.show()

# # 绘制曲线图（验证制表正确性）
# ZC_table = np.load(f'FGM_3D/Gamma={Gamma}/fL={fL}/ZC_table.npy')
# Z = np.linspace(0, 1, 51)
# plt.figure(figsize=(10, 8))
# for i in range(51):
#     values = ZC_table[0, :, 1, i]
#     plt.plot(Z, values, label=f'C={i / 50}')
# plt.xlabel('Z', fontsize=12)
# plt.ylabel('Phi', fontsize=12)
# plt.title('4D_Table Results (51×51)')
# plt.legend()
# plt.grid(linestyle='--', linewidth=1)
# plt.show()
