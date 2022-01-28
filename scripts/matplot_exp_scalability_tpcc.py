import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

def millions(x, pos):
    return '%1.2f' % (x * 1e-6)
formatter = FuncFormatter(millions)

tpcc = """
89352.70	85807.80	107560.00
174187.00	167545.00	214613.00
198122.00	191751.00	246412.00
276521.00	269796.00	351269.00
302461.00	292732.00	383938.00
376884.00	360858.00	487254.00
405960.00	385456.00	519426.00
475641.00	452601.00	618487.00
499349.00	474632.00	651021.00
559656.00	538919.00	747774.00
595069.00	564021.00	783443.00
648229.00	617214.00	878188.00
681921.00	649657.00	908210.00
742488.00	699113.00	994328.00
767960.00	730758.00	1035300.00
824539.00	788437.00	1124710.00
846596.00	807017.00	1156980.00
910919.00	858126.00	1245000.00
933846.00	888529.00	1279740.00
994711.00	935598.00	1369970.00
1011710.00	957550.00	1400020.00
1070100.00	1005650.00	1491090.00
1083850.00	1035730.00	1513200.00
1148890.00	1080890.00	1609500.00
1169510.00	1101100.00	1639010.00
1219020.00	1140290.00	1726920.00
1236490.00	1162260.00	1745930.00
1263550.00	1195050.00	1832190.00
1288060.00	1203580.00	1852420.00
1319780.00	1240020.00	1925580.00
1331630.00	1243640.00	1953420.00
"""

# only show even numbers
keys, values, values2, values3, values0, values20, values30 = [], [], [], [], [], [], []
idx = 0
for l in tpcc.split("\n"):
    items = l.replace("\n", "").split("\t")
    if len(items) != 3:
        continue
    idx += 1
    if idx % 2 == 1:
        continue
    keys.append(idx)
    values.append(float(items[0]))
    values2.append(float(items[1]))
    values3.append(float(items[2]))


# plt.rcParams["font.size"] = 24
# matplotlib.rcParams['lines.markersize'] = 24
# fig, ax = plt.subplots(figsize=(10, 10))

plt.rcParams["font.size"] = 48
matplotlib.rcParams['lines.markersize'] = 14
plt.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(figsize=(16, 10))

ax.yaxis.set_major_formatter(formatter)
#ax.plot(keys, values, marker="o", label='2-replica', linewidth=6)
ax.plot(keys, values2, marker="s", label='Rolis', linewidth=6)
ax.plot(keys, values3, marker="^", label='Silo', linewidth=6)

# https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot/43439132#43439132
ax.set_xticks([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30])
ax.set_xticklabels(["2", "", "", "8", "", "", "", "16", "", "", "", "24", "", "", "30"], fontsize=60)
ax.set_xlabel("# of threads", fontsize=60, fontname="serif")

ax.set_yticks([0 * 10**6, 0.4 * 10**6, 0.8 * 10**6, 1.2 * 10**6, 1.6 * 10**6, 2 * 10**6])
ax.set_yticklabels(["0", "0.4", "0.8", "1.2", "1.6", "2.0"], fontsize=60)
ax.legend(bbox_to_anchor=(0.004, -0.01, 0.4, 1), mode="expand", ncol=1, loc="upper left", borderaxespad=0, frameon=True, fancybox=False, framealpha=1)
for tick in ax.get_xticklabels():
    tick.set_fontname("serif")
for tick in ax.get_yticklabels():
    tick.set_fontname("serif")
ax.yaxis.grid()

fig.tight_layout()
fig.savefig("exp_scalability_tpcc.eps", format='eps', dpi=1000)
plt.show()