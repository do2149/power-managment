import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from cffi.backend_ctypes import xrange

# -----------------------------------------日前计划模型--------------------------------------------------------------

MODEL = grb.Model()

# 定义变量

C_grid = MODEL.addVars(1, vtype=grb.GRB.CONTINUOUS, name="C_grid")
C_NG = MODEL.addVars(1, vtype=grb.GRB.CONTINUOUS, name="C_NG")
C_bt = MODEL.addVars(1, vtype=grb.GRB.CONTINUOUS, name="C_bt")
C_E = MODEL.addVars(1, vtype=grb.GRB.CONTINUOUS, name="C_E")
C_P2G = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="C_P2G")
C_H2G = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="C_H2G")

F_GB = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="F_GB")

P_WT = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_WT")
P_PV = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_PV")
P_MT = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_MT")
P_FC = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="P_FC")
P_grid = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, ub=2100, name="P_grid")
P_bt_chr = MODEL.addVars(24, lb=0, ub=200, vtype=grb.GRB.CONTINUOUS, name="P_bt_chr")
P_bt_dis = MODEL.addVars(24, lb=0, ub=200, vtype=grb.GRB.CONTINUOUS, name="P_bt_dis")
P_ISAC = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_ISAC")
P_a = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_a")
P_c = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_c")
P_EB = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, ub=1000, name="P_EB")
P_sell = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_sell")
P_H_e = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="P_H_e")

H_MT = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="H_MT")  # H_MT == H_HE
H_EB = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="H_EB")
H_GB = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, ub=1400, name="H_GB")
H_tst_chr = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, ub=200, name="H_tst_chr")
H_tst_dis = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, ub=150, name="H_tst_dis")

Q_MT = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="Q_MT")  # Q_MT == Q_AR
Q_a = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, ub=500, name="Q_a")
Q_c = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, ub=300, name="Q_c")
Q_d = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, ub=120, name="Q_d")

G_CH4 = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="G_CH4")  # 甲烷化功率
G_H_sto_in = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="G_H_sto_in")  # 注入储氢罐氢功率
G_H_sto_out = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="G_H_sto_out")  # 输出储氢罐氢功率
G_grid = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="G_grid")  # 气网
G_load = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="G_load")  # 气负荷
G_H_CH4 = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="G_H_CH4")  # 用于甲烷化的氢气
G_FC_H = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, name="G_FC_H")  # 用于氢氧燃料电池的氢气

S_SOC = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="S_SOC")
W_tst = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="W_tst")
S_ice = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="S_ice")
V_H2 = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="V_H2")

U_MT = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_MT")
U_FC = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_FC")
U_bt_chr = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_bt_chr")
U_bt_dis = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_bt_dis")
U_tst_chr = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_tst_chr")
U_tst_dis = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_tst_dis")
U_a = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_a")
U_c = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_c")
U_d = MODEL.addVars(24, vtype=grb.GRB.INTEGER, lb=0, ub=1, name="U_d")

E_CO2 = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="E_CO2")
E_SOX = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="E_SOX")
E_NOX = MODEL.addVars(24, vtype=grb.GRB.CONTINUOUS, lb=0, name="E_NOX")

# 电、热、冷负荷
P_load = [1200, 1240, 1250, 1255, 1350, 1400, 1500, 1600, 1700, 2050, 2000, 1750,
          1730, 1780, 1750, 1600, 1650, 1900, 2000, 1950, 1650, 1500, 1300, 1200]
H_load = [1700, 1750, 1770, 1720, 1670, 1690, 1690, 1670, 1720, 1690, 1520, 1500,
          1400, 1300, 1280, 1350, 1400, 1380, 1410, 1690, 1750, 1760, 1750, 1710]
Q_load = [200, 200, 190, 205, 200, 205, 450, 500, 600, 800, 1050, 1070,
          1080, 800, 850, 780, 750, 720, 600, 630, 400, 550, 200, 180]

# 风电、光电、地热能
WT_ub = [300, 250, 500, 500, 550, 560, 550, 580, 570, 500, 320, 570,
         550, 520, 520, 520, 150, 100, 80, 80, 100, 100, 320, 500]

WT_surplus = [300, 250, 500, 500, 550, 560, 550, 580, 570, 500, 320, 570,
              550, 520, 520, 520, 150, 100, 80, 80, 100, 100, 320, 500]

PV_ub = [0, 0, 0, 0, 0, 0, 80, 120, 130, 150, 200, 250,
         220, 210, 200, 120, 80, 0, 0, 0, 0, 0, 0, 0]

GT_ub = [220, 210, 200, 180, 170, 150, 130, 120, 100, 130, 160, 180,
         200, 250, 220, 210, 200, 120, 80, 60, 50, 50, 50, 40]

# 更新模型

MODEL.update()

l_P_MT = []
l_F_GB = []
l_P_EB = []
l_P_ISAC = []
l_P_grid = []
l_P_FC = []
l_P_bt_dis = []
l_P_bt_chr = []
l_S_SOC = []
l_U_MT = []
l_H_tst_chr = []
l_H_tst_dis = []
l_H_GB = []
l_P_a = []
l_P_c = []

# 优化

# 设置目标函数

MODEL.setObjective(C_grid[0] + C_NG[0] + C_bt[0], grb.GRB.MINIMIZE)

# 设置约束函数

I1 = [0, 1, 2, 3, 4, 5, 22, 23]  # 电价谷期
I2 = [11, 12, 13, 14, 15, 16]  # 电价平期
I3 = [6, 7, 8, 9, 10, 17, 18, 19, 20, 21]  # 电价峰期
I4 = list(xrange(0, 24))
# c = np.array(I1) + np.array(I2)
# print(c)
# exit(0)

MODEL.addConstr(C_grid[0] == grb.quicksum(P_grid[i1] * 0.3 - P_sell[i1] * 0.05 for i1 in I1) +
                grb.quicksum(P_grid[i2] * 0.45 - P_sell[i2] * 0.05 for i2 in I2) +
                grb.quicksum(P_grid[i3] * 0.6 - P_sell[i3] * 0.09 for i3 in I3))

MODEL.addConstr(C_bt[0] == grb.quicksum(0.2 * (U_bt_dis[i5] + U_bt_chr[i5]) for i5 in I4))

MODEL.addConstr(C_NG[0] == grb.quicksum(G_grid[i4] for i4 in I4) * 0.6 / 9.78)

MODEL.addConstr(C_E[0] == grb.quicksum(E_CO2[i5] + E_SOX[i5] + E_NOX[i5] for i5 in I4))

MODEL.addConstr(C_P2G[0] == grb.quicksum((G_H_sto_in[i5] * 0.001 + G_H_sto_out[i5] * 0.001) for i5 in I4))

MODEL.addConstr(C_H2G[0] == grb.quicksum((G_H_CH4[i5] * 0.001) for i5 in I4))

i = 0
while i < 24:

    MODEL.addConstr(P_WT[i] + P_PV[i] + P_MT[i] + P_FC[i] + P_grid[i] - P_bt_chr[i] + P_bt_dis[i] - P_sell[i]
                    == P_load[i] + P_ISAC[i] + P_EB[i], "Electricity_balance")  # 电平衡约束

    MODEL.addConstr(Q_MT[i] + Q_a[i] + Q_d[i] == Q_load[i], "cool_balance")  # 冷平衡约束

    MODEL.addConstr(H_MT[i] + GT_ub[i] + H_EB[i] + H_GB[i] - H_tst_chr[i] + H_tst_dis[i] == H_load[i])  # 热平衡约束

    MODEL.addConstr(G_CH4[i] + G_grid[i] == G_load[i])  # 气平衡约束

    MODEL.addConstr(G_load[i] == (2.64 * P_MT[i] + 66.2 * U_MT[i] + F_GB[i]) / 9.78)  # 气负荷

    MODEL.addConstr(P_WT[i] == WT_ub[i])  # 每时段风力功率限制
    MODEL.addConstr(P_PV[i] == PV_ub[i])  # 每时段光伏发电功率限制

    MODEL.addConstr(P_MT[i] <= U_MT[i] * 2000)  # P_MT 约束
    MODEL.addConstr(P_MT[i] >= U_MT[i] * 15)

    # MODEL.addConstr(P_FC[i] <= U_FC[i] * 2000)  # P_FC 约束
    # MODEL.addConstr(P_FC[i] >= U_FC[i] * 15)
    MODEL.addConstr(P_FC[i] == 62 * G_FC_H[i])

    MODEL.addConstr(H_MT[i] == 0.81 * P_MT[i])  # MT-HE, 将电能转化热能
    MODEL.addConstr(Q_MT[i] == 0.51 * P_MT[i])  # MT-AR, 将电能转化冷能

    MODEL.addConstr(H_EB[i] == 0.93 * P_EB[i])  # EB, 将电能转化为热能

    MODEL.addConstr(H_GB[i] == 0.9 * F_GB[i])  # GB, 将天然气转化为热能

    # 蓄电池ES
    MODEL.addConstr(P_bt_chr[i] <= U_bt_chr[i] * 200)  # P_bt_chr 充电约束
    MODEL.addConstr(P_bt_dis[i] <= U_bt_dis[i] * 200)  # P_bt_dis 放电约束
    MODEL.addConstr(U_bt_chr[i] + U_bt_dis[i] <= 1)  # 充放电互斥
    MODEL.addConstr(S_SOC[i] >= P_bt_dis[i] / 0.95)

    if i == 0:
        MODEL.addConstr(S_SOC[i] == 0.95 * P_bt_chr[i] - P_bt_dis[i] / 0.95 - P_sell[i])  # SOC约束
    else:
        MODEL.addConstr(S_SOC[i] == S_SOC[i - 1] + 0.95 * P_bt_chr[i] - P_bt_dis[i] / 0.95 - P_sell[i])  # SOC约束

    # 储氢罐
    if i == 0:
        MODEL.addConstr(V_H2[i] == G_H_sto_in[i] - (G_H_CH4[i] + G_FC_H[i]))
    else:
        MODEL.addConstr(V_H2[i] == V_H2[i - 1] + G_H_sto_in[i] - (G_H_CH4[i] + G_FC_H[i]))

    MODEL.addConstr(G_H_sto_in[i] == 0.4 * WT_surplus[i])  # 电解水产生氢气
    MODEL.addConstr(G_H_sto_out[i] == G_H_CH4[i] + G_FC_H[i])  # 输出氢气用于甲烷化和燃料电池
    MODEL.addConstr(G_H_CH4[i] * 0.25 == G_CH4[i])

    # 蓄热槽 HS_tst
    MODEL.addConstr(H_tst_chr[i] <= U_tst_chr[i] * 200)  # H_tst_chr 蓄热约束
    MODEL.addConstr(H_tst_dis[i] <= U_tst_dis[i] * 150)  # H_tst_dis 放热约束
    MODEL.addConstr(U_tst_chr[i] + U_tst_dis[i] <= 1)  # 蓄放热互斥

    if i == 0:
        MODEL.addConstr(W_tst[i] == 0.98 * H_tst_chr[i] - H_tst_dis[i] / 0.98)  # 蓄热槽容量约束
    else:
        MODEL.addConstr(W_tst[i] == W_tst[i - 1] * 0.98 + 0.98 * H_tst_chr[i] - H_tst_dis[i] / 0.98)  # 蓄热槽容量约束

    # ISAC系统 选择并联式ISAC系统 运行方式4：白天制冷，晚上蓄冰制冷，电价峰值时融冰
    MODEL.addConstr(Q_a[i] <= U_a[i] * 500)  # Q_a 输出冷功率约束
    MODEL.addConstr(Q_d[i] <= U_d[i] * 120)  # 融冰功率约束
    MODEL.addConstr(Q_c[i] <= U_c[i] * 300)  # 蓄冰功率约束
    MODEL.addConstr(Q_c[i] + Q_a[i] <= 500)  # 融蓄冰互斥

    MODEL.addConstr(P_a[i] * (0.001226 * Q_a[i] + 1.91) == Q_a[i])
    MODEL.addConstr(P_c[i] * (0.001226 * Q_c[i] + 1.91) == Q_c[i])
    MODEL.addConstr(P_ISAC[i] == P_a[i] + P_c[i])

    if 0 <= i <= 5 or 22 <= i <= 23:  # 电价谷时期
        MODEL.addConstr(U_d[i] == 0)  # 电价谷期不融冰，直接用电
    else:
        MODEL.addConstr(U_c[i] == 0)  # 当电价不处于谷期，不蓄冰
    if i == 0:
        MODEL.addConstr(S_ice[i] == 0.67 * Q_c[i] - Q_d[i] / 0.75)  # 蓄冷罐约束
    else:
        MODEL.addConstr(S_ice[i] == 0.98 * S_ice[i - 1] + 0.67 * Q_c[i] - Q_d[i] / 0.75)  # 蓄冷罐约束

    MODEL.addConstr(E_CO2[i] == 0.17644 * (2.64 * P_MT[i] + 66.2 * U_MT[i] + F_GB[i]) / 9.78 +
                    0.02072 * P_grid[i])  # CO2排放量
    MODEL.addConstr(E_SOX[i] == 1.5 * (2.64 * P_MT[i] + 66.2 * U_MT[i] + F_GB[i]) / 9.78)  # SOX排放量
    MODEL.addConstr(E_NOX[i] == 2.5 * (2.64 * P_MT[i] + 66.2 * U_MT[i] + F_GB[i]) / 9.78)  # NOX排放量

    i = i + 1

# 模型参数设置
# MODEL.Params.LogToConsole = True  # 显示求解过程
MODEL.Params.MIPGap = 0.0001  # 百分比界差
MODEL.Params.TimeLimit = 100  # 限制求解时间为 100s
MODEL.params.NonConvex = 2

MODEL.optimize()

l_U_bt_dis = []
l_U_bt_chr = []
l_H_MT = []
l_H_EB = []
l_Q_MT = []
l_Q_a = []
l_Q_d = []
i = 0
while i < 24:
    l_P_MT.append(P_MT[i].x)
    l_F_GB.append(F_GB[i].x)
    l_P_EB.append(P_EB[i].x)
    l_P_ISAC.append(P_ISAC[i].x)
    l_P_grid.append(P_grid[i].x)
    l_P_FC.append(P_FC[i].x)
    l_P_bt_dis.append(P_bt_dis[i].x)
    l_P_bt_chr.append(P_bt_chr[i].x)
    l_S_SOC.append(S_SOC[i].x)
    l_U_MT.append(U_MT[i].x)
    l_H_tst_chr.append(H_tst_chr[i].x)
    l_H_tst_dis.append(H_tst_dis[i].x)
    l_H_GB.append(H_GB[i].x)
    l_H_MT.append(H_MT[i].x)
    l_H_EB.append(H_EB[i].x)
    l_P_a.append(P_a[i].x)
    l_P_c.append(P_c[i].x)
    l_Q_MT.append(Q_MT[i].x)
    l_Q_a.append(Q_a[i].x)
    l_Q_d.append(Q_d[i].x)
    i1 = 0
    temp_1 = []
    temp_2 = []
    while i1 < 12:
        temp_1.append(U_bt_chr[i].x / 12)
        temp_2.append(U_bt_dis[i].x / 12)
        i1 = i1 + 1
    l_U_bt_chr.append(temp_1)
    l_U_bt_dis.append(temp_2)

    print("Optimal Objective Value", MODEL.objVal,
          "\nP_WT", [i], '=', P_WT[i].x,
          "\nP_PV", [i], '=', P_PV[i].x,
          "\nP_MT", [i], '=', P_MT[i].x,
          "\nP_FC", [i], '=', P_FC[i].x,
          "\nP_grid", [i], '=', P_grid[i].x,
          "\nP_bt_chr", [i], '=', P_bt_chr[i].x * -1,
          "\nP_bt_dis", [i], '=', P_bt_dis[i].x,
          "\nP_ISAC", [i], '=', P_ISAC[i].x * -1,
          "\nP_EB", [i], '=', P_EB[i].x * -1,
          "\nP_sell", [i], '=', P_sell[i].x * -1,
          "\nS_SOC", [i], '=', S_SOC[i].x,
          "\nH_MT", [i], '=', H_MT[i].x,
          "\nH_EB", [i], '=', H_EB[i].x,
          "\nH_GB", [i], '=', H_GB[i].x,
          "\nH_tst_chr", [i], '=', H_tst_chr[i].x * -1,
          "\nH_tst_dis", [i], '=', H_tst_dis[i].x,
          "\nQ_MT", [i], '=', Q_MT[i].x,
          "\nQ_a", [i], '=', Q_a[i].x,
          "\nQ_d", [i], '=', Q_d[i].x,
          "\nV_H2", [i], '=', V_H2[i].x,
          "\nG_CH4", [i], '=', G_CH4[i].x,
          "\nG_load", [i], '=', G_load[i].x,
          "\nG_H_sto_in", [i], '=', G_H_sto_in[i].x,
          "\nG_H_sto_out", [i], '=', G_H_sto_out[i].x,
          "\nG_grid", [i], '=', G_grid[i].x,
          "\nG_H_CH4", [i], '=', G_H_CH4[i].x,
          "\nG_FC_H", [i], '=', G_FC_H[i].x, "\n")

    i = i + 1

# exit(0)
# print(l_P_MT)
ind = np.arange(24)  # [ 0  1  2  3  4  5  6  7  8  9 10 11 12]
plt.xticks(ind, ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                 '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))
# -------------------------------------------日前-冷负荷平衡-----------------------------------------------------------
'''
plt.yticks(np.arange(0, 1200, 250))
plt.ylabel('cool balance')
ax = plt.gca()
plt.axhline(0, -3, 3, c="black")
width = 0.35
p1 = plt.bar(ind, l_Q_MT, width, color='black')
p2 = plt.bar(ind, l_Q_a, width, bottom=l_Q_MT, color='green')
a = np.array(l_Q_a) + np.array(l_Q_MT)
p3 = plt.bar(ind, l_Q_d, width, bottom=a, color='purple')
plt.plot(ind, Q_load)
plt.show()
'''
# -------------------------------------------日前-热负荷平衡-----------------------------------------------------------
'''
plt.yticks(np.arange(-250, 2000, 250))
plt.ylabel('heat balance')
ax = plt.gca()
plt.axhline(0, -3, 3, c="black")
width = 0.35
p1 = plt.bar(ind, l_H_MT, width, color='black')
p2 = plt.bar(ind, l_H_EB, width, bottom=l_H_MT, color='blue')
a = np.array(l_H_MT) + np.array(l_H_EB)
p3 = plt.bar(ind, l_H_GB, width, bottom=a, color='green')
a = np.array(a) + np.array(l_H_GB)
p4 = plt.bar(ind, l_H_tst_dis, width, bottom=a, color='purple')
p5 = plt.bar(ind, l_H_tst_chr, width, color='purple')
plt.plot(ind, H_load)
plt.show()
'''
# -------------------------------------------日前-电负荷平衡-----------------------------------------------------------
'''
plt.ylabel('eletricity balance')
plt.yticks(np.arange(-1000, 2501, 500))


i = 0
l1 = []
l2 = []
l3 = []
l4 = []
while i < 24:
    l1.append(-1 * l_P_bt_chr[i])
    l2.append(-1 * l_P_EB[i])
    l3.append(-1 * l_P_ISAC[i])
    l4.append(WT_ub[i])
    i = i + 1

ax = plt.gca()
plt.axhline(0, -3, 3, c="black")
# ax.spines['bottom'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.spines['bottom'].set_position(('data', 0))
width = 0.35  # 设置条形图一个长条的宽度
p1 = plt.bar(ind, l_P_MT, width, color='black')
p2 = plt.bar(ind, l_P_FC, width, bottom=l_P_MT, color='purple')
a = np.array(l_P_MT) + np.array(l_P_FC)
p3 = plt.bar(ind, l_P_grid, width, bottom=a, color='blue')
a = np.array(a) + np.array(l_P_grid)
p4 = plt.bar(ind, l4, width, bottom=a, color='green')
a = np.array(a) + np.array(l4)
p5 = plt.bar(ind, PV_ub, width, bottom=a, color='yellow')
a = np.array(a) + np.array(PV_ub)
p9 = plt.bar(ind, l_P_bt_dis, width, bottom=a, color='orange')
p6 = plt.bar(ind, l1, width, color='orange')
p7 = plt.bar(ind, l2, width, bottom=l1, color='red')
b = np.array(l1) + np.array(l2)
p8 = plt.bar(ind, l3, width, bottom=b, color='black')

# plt.legend((p1[0], p2[0], p3[0]), ('Bottom', 'Center', 'Top'), loc=3)
plt.plot(ind, P_load)
plt.show()

# exit(0)
'''
