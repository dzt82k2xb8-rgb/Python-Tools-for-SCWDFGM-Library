import os
import matplotlib.pyplot as plt
from flamelet_integration import *

# 指定fL的值
fL = ['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1']

# 设置目标文件夹FGM_5D，用于储存ZCGamma_table文件
FGM_5D_folder = f'FGM_5D/'
os.makedirs(FGM_5D_folder, exist_ok=True)

# 遍历Gamma的值，读取不同的ZC_table并储存至ZC_tables
ZCGamma_tables = []
for fl in fL:
    file_path = f'FGM_4D/fL={fl}/ZCGamma_table.npy'
    data = np.load(file_path)
    ZCGamma_tables.append(data)

ZCGammaEta_table = np.stack(ZCGamma_tables, axis=0).transpose((1, 2, 3, 4, 5, 0))
np.save(f'FGM_5D/ZCGammaEta_table.npy', ZCGammaEta_table)
print(ZCGammaEta_table.shape)

# 绘制等高线图（验证制表正确性）
ZCGammaEta_table = np.load(f'FGM_5D/ZCGammaEta_table.npy')
Z = np.linspace(0, 1, 51)
C = np.linspace(0, 1, 51)
Z, C = np.meshgrid(Z, C)
plt.figure(figsize=(10, 8))
plt.contourf(C, Z, ZCGammaEta_table[0, :, 0, :, 0, 0], levels=101, cmap=plt.cm.rainbow)  # 该函数期望数据按照(y, x)的顺序排列
plt.colorbar()
plt.title('5D_Table Results (51×51)', fontsize=14)
plt.xlabel('Z', fontsize=12)
plt.ylabel('C', fontsize=12)
plt.grid(linestyle='--', linewidth=1)
plt.show()
