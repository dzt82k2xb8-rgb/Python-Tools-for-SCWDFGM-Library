import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator

# 指定Gamma、T_oxi、fL的值
Gamma = '0'      # (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 1)
T_oxi = '405'    # (405, 615, 661, 683, 706, 727, 747, 764, 779, 786, 793, 805)
fL    = '0'      # (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)

# 打开工作路径
work_dir = r'E:\Work\Comparison of combustion models\Python_pre\FGM_table_5D_R'
os.chdir(work_dir)

# 设置目标文件夹Flamelet，用于储存csv文件
target_folder = os.path.join(work_dir, f'Flamelet/Gamma={Gamma}/fL={fL}')
os.makedirs(target_folder, exist_ok=True)

# 获取LT_up中所有以'.kg'结尾的文件名称
Filenames_up = [f for f in os.listdir(os.path.join(work_dir, f'LT/Gamma={Gamma}/fL={fL}/LT_up')) if f.endswith('.kg')]
source_folder_up = os.path.join(work_dir, f'LT/Gamma={Gamma}/fL={fL}/LT_up')

# 读取LT_up中所有文件，并转化为csv格式
for i, filename in enumerate(Filenames_up):
    chi_st = float(filename.split("H2_p250_0chi")[1].split(f"tf0805to0{T_oxi}.kg")[0])
    new_filename = f'Table_up_{chi_st}.csv'

    source_file_path = os.path.join(source_folder_up, filename)
    target_file_path = os.path.join(target_folder, new_filename)

    A = pd.read_csv(source_file_path, header=1, sep='\t')
    A.to_csv(target_file_path, index=False)

# 获取LT_mid中所有以'.kg'结尾的文件名称
Filenames_mid = [f for f in os.listdir(os.path.join(work_dir, f'LT/Gamma={Gamma}/fL={fL}/LT_mid')) if f.endswith('.kg')]
source_folder_mid = os.path.join(work_dir, f'LT/Gamma={Gamma}/fL={fL}/LT_mid')

# 读取LT_mid中所有文件，并转化为csv格式
for i, filename in enumerate(Filenames_mid):
    chi_st = float(filename.split("H2_p250_0chi")[1].split(f"tf0805to0{T_oxi}.kg")[0])
    new_filename = f'Table_mid_{chi_st}.csv'

    source_file_path = os.path.join(source_folder_mid, filename)
    target_file_path = os.path.join(target_folder, new_filename)

    B = pd.read_csv(source_file_path, header=1, sep='\t')
    B.to_csv(target_file_path, index=False)

# 读取转化后的csv文件，并按照PV从小到大的顺序排序后放入C中
file_names = os.listdir(target_folder)
file_names_mid = [f for f in file_names if 'Table_mid' in f]
file_names_mid.sort(key=lambda x: float(os.path.splitext(x)[0].split('_')[-1]))
file_names_up = [f for f in file_names if 'Table_up' in f]
file_names_up.sort(key=lambda x: -float(os.path.splitext(x)[0].split('_')[-1]))
file_names_all = file_names_mid + file_names_up

C = pd.DataFrame()
for file in file_names_all:
    file_path = os.path.join(target_folder, file)
    df = pd.read_csv(file_path)
    C = pd.concat([C, df.iloc[:201]], ignore_index=True)

# 修改列的名称以方便引用
C.columns = ['Z', 'T', 'H2', 'O2', 'H2O', 'H', 'O', 'OH', 'HO2', 'H2O2', 'AR',
             'W', 'ZBilger', 'chi', 'rho', 'lambda', 'Cps', 'alpha', 'mu', 'ProdRateCO2',
             'ProdRateH2O', 'ProdRateCO', 'ProdRateH2', 'PV', 'SourcePV', 'TotalEnthalpy', 'HRR']

# 重新计算PV和SourcePV，并添加psi
C['PV'] = (C['H2O'] - 0.974421 / 0.025579 * C['H2']).clip(lower=0)
C['SourcePV'] = (C['ProdRateH2O'] - 0.974421 / 0.025579 * C['ProdRateH2']).clip(lower=0)
C['psi'] = C['rho'] / 25000000
C['TE'] = C['TotalEnthalpy']

# 计算吸收系数absCoeff
C['X_H2'] = C['H2'] / 2.016 / (C['H2'] / 2.016 + C['O2'] / 31.999 + C['H2O'] / 18.015 + C['AR'] / 39.948)
C['X_O2'] = C['O2'] / 31.999 / (C['H2'] / 2.016 + C['O2'] / 31.999 + C['H2O'] / 18.015 + C['AR'] / 39.948)
C['X_H2O'] = C['H2O'] / 18.015 / (C['H2'] / 2.016 + C['O2'] / 31.999 + C['H2O'] / 18.015 + C['AR'] / 39.948)
C['X_AR'] = C['AR'] / 39.948 / (C['H2'] / 2.016 + C['O2'] / 31.999 + C['H2O'] / 18.015 + C['AR'] / 39.948)

C['tem'] = 1.0 / C['T']
C['a_H2'] = 0.1
C['a_O2'] = 0.1
C['a_H2O'] = -0.23093 + C['tem'] * (-1.12390e3 + C['tem'] * (9.4153e6 + C['tem'] * (-2.99885e9 + C['tem'] * (0.51382e12 + C['tem'] * (-1.868e10)))))
C['a_AR'] = 0.1

C['AbsCoeff'] = 25000000 / 101325 * (C['X_H2'] * C['a_H2'] + C['X_O2'] * C['a_O2'] + C['X_H2O'] * C['a_H2O'] + C['X_AR'] * C['a_AR'])

# 删除不需要的列
D = C.drop(['W', 'ZBilger', 'chi', 'lambda', 'ProdRateCO2', 'ProdRateH2O', 'ProdRateCO', 'ProdRateH2', 'TotalEnthalpy', 'HRR', 'X_H2', 'X_O2', 'X_H2O', 'X_AR', 'tem', 'a_H2','a_O2','a_H2O','a_AR'], axis=1)

# 将排序合并后的小火焰解保存成csv格式
D.to_csv(os.path.join(target_folder, 'Combined_all.csv'), index=False)

# 定义插值函数F
Z_value = D['Z'].values
PV_value = D['PV'].values
points = np.column_stack((Z_value, PV_value))
Phi_value = D['T'].values
values = np.array(Phi_value)
F = LinearNDInterpolator(points, values)

# 定义网格并插值
xi = np.linspace(0, 1, 501)
yi = np.linspace(0, 1, 501)
xi, yi = np.meshgrid(xi, yi)
zi = F(xi, yi)

# 绘制等高线图
plt.figure(figsize=(10, 8))
plt.contourf(xi, yi, zi, levels=501, cmap=plt.cm.rainbow)
plt.colorbar()
plt.title('Interpolation Results (51×51)', fontsize=14)
plt.xlabel('Z', fontsize=12)
plt.ylabel('PV', fontsize=12)
plt.grid(linestyle='--', linewidth=1)
plt.show()
