import os
import numpy as np

# 打开工作路径
work_dir = r'E:\Work\Comparison of combustion models\Python_pre\FGM_table_5D_R'
os.chdir(work_dir)

# 新建文件夹FGM_table，用于储存table文件
table_folder = os.path.join(work_dir, 'FGM_table')
os.makedirs(table_folder, exist_ok=True)

# 读取ZC_table文件
ZCGammaEta_table = np.load(f'FGM_5D/ZCGammaEta_table.npy')

# 定义变量的名称，用于文件命名
variable_names = np.array(['T', 'H2', 'O2', 'H2O', 'H', 'O', 'OH', 'HO2', 'H2O2', 'AR',
                           'rho', 'Cps', 'alpha', 'mu', 'PV', 'SourcePV', 'psi', 'TE', 'AbsCoeff'])  # 19个被积分的标量

# 通过6层循环，将ZCGammaEta_table的内容输出至文件
for i in range(ZCGammaEta_table.shape[0]):
    file_path = os.path.join(table_folder, f'{variable_names[i]}_table')

    with open(file_path, 'w') as file:
        file.write("/*--------------------------------*- C++ -*----------------------------------*\\" + "\n")
        file.write("  =========                 |" + "\n")
        file.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox" + "\n")
        file.write("   \\\\    /   O peration     | Website:  https://openfoam.org" + "\n")
        file.write("    \\\\  /    A nd           | Version:  6" + "\n")
        file.write("     \\\\/     M anipulation  |" + "\n")
        file.write("\\*---------------------------------------------------------------------------*/" + "\n")
        file.write("FoamFile" + "\n")
        file.write("{   version     2.0;" + "\n")
        file.write("    format      ascii;" + "\n")
        file.write("    class       dictionary;" + "\n")
        file.write('    location    "FGM_table";' + "\n")
        file.write("    object      " + f'{variable_names[i]}_table;' + "\n")
        file.write("}" + "\n")
        file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //" + "\n\n")
        file.write(f'{variable_names[i]}_table' + "\n\n")
        file.write(str(ZCGammaEta_table.shape[5]) + "\n")
        file.write("(\n")

        for n in range(ZCGammaEta_table.shape[5]):
            file.write(str(ZCGammaEta_table.shape[4]) + "\n")
            file.write("(\n")

            for m in range(ZCGammaEta_table.shape[4]):
                file.write(str(ZCGammaEta_table.shape[3]) + "\n")
                file.write("(\n")

                for l in range(ZCGammaEta_table.shape[3]):
                    file.write(str(ZCGammaEta_table.shape[2]) + "\n")
                    file.write("(\n")

                    for k in range(ZCGammaEta_table.shape[2]):
                        file.write(str(ZCGammaEta_table.shape[1]) + "\n")
                        file.write("(\n")

                        for j in range(ZCGammaEta_table.shape[1]):
                            file.write(f"{ZCGammaEta_table[i, j, k, l, m, n]:.6e}" + "\n")

                        file.write(")\n")
                    file.write(")\n")
                file.write(")\n")
            file.write(")\n")
        file.write(")\n;")

# 输出PVmin
file_path = os.path.join(table_folder, 'PVmin_table')
with open(file_path, 'w') as file:
    file.write("/*--------------------------------*- C++ -*----------------------------------*\\" + "\n")
    file.write("  =========                 |" + "\n")
    file.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox" + "\n")
    file.write("   \\\\    /   O peration     | Website:  https://openfoam.org" + "\n")
    file.write("    \\\\  /    A nd           | Version:  6" + "\n")
    file.write("     \\\\/     M anipulation  |" + "\n")
    file.write("\\*---------------------------------------------------------------------------*/" + "\n")
    file.write("FoamFile" + "\n")
    file.write("{   version     2.0;" + "\n")
    file.write("    format      ascii;" + "\n")
    file.write("    class       dictionary;" + "\n")
    file.write('    location    "FGM_table";' + "\n")
    file.write("    object      PVmin_table;" + "\n")
    file.write("}" + "\n")
    file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //" + "\n\n")
    file.write('PVmin_table' + "\n\n")
    file.write(str(ZCGammaEta_table.shape[4]) + "\n")
    file.write("(\n")

    for m in range(ZCGammaEta_table.shape[4]):
        file.write(str(ZCGammaEta_table.shape[2]) + "\n")
        file.write("(\n")

        for j in range(ZCGammaEta_table.shape[2]):
            file.write(str(ZCGammaEta_table.shape[1]) + "\n")
            file.write("(\n")

            for i in range(ZCGammaEta_table.shape[1]):
                file.write(f"{ZCGammaEta_table[14, i, j, :, m, :].min():.6e}" + "\n")

            file.write(")\n")
        file.write(")\n")
    file.write(")\n;")

# 输出PVmax
file_path = os.path.join(table_folder, 'PVmax_table')
with open(file_path, 'w') as file:
    file.write("/*--------------------------------*- C++ -*----------------------------------*\\" + "\n")
    file.write("  =========                 |" + "\n")
    file.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox" + "\n")
    file.write("   \\\\    /   O peration     | Website:  https://openfoam.org" + "\n")
    file.write("    \\\\  /    A nd           | Version:  6" + "\n")
    file.write("     \\\\/     M anipulation  |" + "\n")
    file.write("\\*---------------------------------------------------------------------------*/" + "\n")
    file.write("FoamFile" + "\n")
    file.write("{   version     2.0;" + "\n")
    file.write("    format      ascii;" + "\n")
    file.write("    class       dictionary;" + "\n")
    file.write('    location    "FGM_table";' + "\n")
    file.write("    object      PVmax_table;" + "\n")
    file.write("}" + "\n")
    file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //" + "\n\n")
    file.write('PVmax_table' + "\n\n")
    file.write(str(ZCGammaEta_table.shape[4]) + "\n")
    file.write("(\n")

    for m in range(ZCGammaEta_table.shape[4]):
        file.write(str(ZCGammaEta_table.shape[2]) + "\n")
        file.write("(\n")

        for j in range(ZCGammaEta_table.shape[2]):
            file.write(str(ZCGammaEta_table.shape[1]) + "\n")
            file.write("(\n")

            for i in range(ZCGammaEta_table.shape[1]):
                file.write(f"{ZCGammaEta_table[14, i, j, :, m, :].max():.6e}" + "\n")

            file.write(")\n")
        file.write(")\n")
    file.write(")\n;")

# 输出TEmin
file_path = os.path.join(table_folder, 'TEmin_table')
with open(file_path, 'w') as file:
    file.write("/*--------------------------------*- C++ -*----------------------------------*\\" + "\n")
    file.write("  =========                 |" + "\n")
    file.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox" + "\n")
    file.write("   \\\\    /   O peration     | Website:  https://openfoam.org" + "\n")
    file.write("    \\\\  /    A nd           | Version:  6" + "\n")
    file.write("     \\\\/     M anipulation  |" + "\n")
    file.write("\\*---------------------------------------------------------------------------*/" + "\n")
    file.write("FoamFile" + "\n")
    file.write("{   version     2.0;" + "\n")
    file.write("    format      ascii;" + "\n")
    file.write("    class       dictionary;" + "\n")
    file.write('    location    "FGM_table";' + "\n")
    file.write("    object      TEmin_table;" + "\n")
    file.write("}" + "\n")
    file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //" + "\n\n")
    file.write('TEmin_table' + "\n\n")
    file.write(str(ZCGammaEta_table.shape[4]) + "\n")
    file.write("(\n")

    for n in range(ZCGammaEta_table.shape[4]):
        file.write(str(ZCGammaEta_table.shape[3]) + "\n")
        file.write("(\n")

        for m in range(ZCGammaEta_table.shape[3]):
            file.write(str(ZCGammaEta_table.shape[2]) + "\n")
            file.write("(\n")

            for j in range(ZCGammaEta_table.shape[2]):
                file.write(str(ZCGammaEta_table.shape[1]) + "\n")
                file.write("(\n")

                for i in range(ZCGammaEta_table.shape[1]):
                    file.write(f"{ZCGammaEta_table[17, i, j, m, n, :].min():.6e}" + "\n")

                file.write(")\n")
            file.write(")\n")
        file.write(")\n")
    file.write(")\n;")

# 输出TEmax
file_path = os.path.join(table_folder, 'TEmax_table')
with open(file_path, 'w') as file:
    file.write("/*--------------------------------*- C++ -*----------------------------------*\\" + "\n")
    file.write("  =========                 |" + "\n")
    file.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox" + "\n")
    file.write("   \\\\    /   O peration     | Website:  https://openfoam.org" + "\n")
    file.write("    \\\\  /    A nd           | Version:  6" + "\n")
    file.write("     \\\\/     M anipulation  |" + "\n")
    file.write("\\*---------------------------------------------------------------------------*/" + "\n")
    file.write("FoamFile" + "\n")
    file.write("{   version     2.0;" + "\n")
    file.write("    format      ascii;" + "\n")
    file.write("    class       dictionary;" + "\n")
    file.write('    location    "FGM_table";' + "\n")
    file.write("    object      TEmax_table;" + "\n")
    file.write("}" + "\n")
    file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //" + "\n\n")
    file.write('TEmax_table' + "\n\n")
    file.write(str(ZCGammaEta_table.shape[4]) + "\n")
    file.write("(\n")

    for n in range(ZCGammaEta_table.shape[4]):
        file.write(str(ZCGammaEta_table.shape[3]) + "\n")
        file.write("(\n")

        for m in range(ZCGammaEta_table.shape[3]):
            file.write(str(ZCGammaEta_table.shape[2]) + "\n")
            file.write("(\n")

            for j in range(ZCGammaEta_table.shape[2]):
                file.write(str(ZCGammaEta_table.shape[1]) + "\n")
                file.write("(\n")

                for i in range(ZCGammaEta_table.shape[1]):
                    file.write(f"{ZCGammaEta_table[17, i, j, m, n, :].max():.6e}" + "\n")

                file.write(")\n")
            file.write(")\n")
        file.write(")\n")
    file.write(")\n;")
