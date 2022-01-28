import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

def millions(x, pos):
    return '%1.2fM' % (x * 1e-6)
formatter = FuncFormatter(millions)

txt = """
78278.7
153227
179202
246015
270831
330990
344913
353626
346366
336202
327740
326833
328893
320498
311341
305137
284828
282478
277404
275164
265050
268728
257698
247359
251119
227249
218437
224966
228589
228623
217698
"""

keys, values = [], []
idx = 0
for e in txt.split("\n"):
    if not e:
        continue

    idx += 1
    if idx % 2 == 1:
        continue

    keys.append(idx)
    values.append(float(e))

plt.rcParams["font.size"] = 30
matplotlib.rcParams['lines.markersize'] = 14
plt.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(figsize=(14, 9))
ax.yaxis.set_major_formatter(formatter)
ax.plot(keys, values, marker="s", label='one Paxos Stream', linewidth=3)

# ax.set(xlabel='# of threads',
#        ylabel='Throughput (txns/sec)',
#        title=None)
ax.set_xlabel("# of threads", fontname="serif")
ax.set_ylabel("Throughput (txns/sec)", fontname="serif")
ax.set_xticks([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30])
ax.set_xticklabels(["2", "", "6", "", "10", "", "14", "", "18", "", "22", "", "26", "", "30"])
ax.legend(bbox_to_anchor=(0, 0.92, 1, 0.22), mode="expand", ncol=1, loc="upper left", borderaxespad=0.2, frameon=False)
ax.yaxis.grid()
for tick in ax.get_xticklabels():
    tick.set_fontname("serif")

fig.tight_layout()
fig.savefig("single_paxos_group.eps", format='eps', dpi=1000)
plt.show()