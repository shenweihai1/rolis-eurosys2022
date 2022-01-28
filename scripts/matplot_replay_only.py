import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

def millions(x, pos):
    return '%1.1fM' % (x * 1e-6)
formatter = FuncFormatter(millions)

txt = """
107560.00	193824.16
214613.00	227130.71
246412.00	337090.89
351269.00	437606.28
383938.00	547724.62
487254.00	654998.83
519426.00	759217.82
618487.00	856812.07
651021.00	964925.88
747774.00	1067367.08
783443.00	1159696.45
878188.00	1276224.90
908210.00	1374889.50
994328.00	1477006.03
1035300.00	1562702.46
1124710.00	1658236.84
1156980.00	1741983.47
1245000.00	1834392.98
1279740.00	1920220.03
1369970.00	2049483.71
1400020.00	2126602.57
1491090.00	2207353.59
1513200.00	2295175.19
1609500.00	2369593.47
1639010.00	2420733.57
1726920.00	2563147.14
1745930.00	2647047.15
1832190.00	2715275.04
1852420.00	2751441.66
1925580.00	2835069.43
1953420.00	2875147.82
"""
keys, values, values2 = [], [], []
idx = 0
for l in txt.split("\n"):
    items = l.replace("\n", "").split("\t")
    if len(items) != 2:
        continue
    idx += 1
    if idx % 2 == 1:
        continue
    keys.append(idx)
    values.append(float(items[0]))
    values2.append(float(items[1]))

values=[float(e) for e in values]
values2=[float(e) for e in values2]

plt.rcParams["font.size"] = 30
matplotlib.rcParams['lines.markersize'] = 14
plt.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(figsize=(14, 9))

ax.yaxis.set_major_formatter(formatter)
ax.plot(keys, values, color="#1f77b4", marker="s", label='Silo', linewidth=3)
ax.plot(keys, values2, color="#ff7f0e", marker="^", label='Replay-only (Rolis)', linewidth=3)

ax.set_xticks([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30])
ax.set_xticklabels([2, "", 6, "", 10, "", 14, "", 18, "", 22, "", 26, "", 30])
ax.set_ylim([0, 3 * 10**6])

# ax.set(xlabel='# of threads',
#        ylabel='Throughput (txns/sec)',
#        title=None)
ax.set_xlabel("# of threads", fontname="serif")
ax.set_ylabel("Throughput (txns/sec)", fontname="serif")
ax.yaxis.grid()
ax.legend(bbox_to_anchor=(0, 0.92, 1, 0.2), mode="expand", ncol=2, loc="upper left", borderaxespad=0.2, frameon=False)

fig.tight_layout()
fig.savefig("exp_replay_only.eps", format='eps', dpi=1000)
plt.show()