# 图表与结果

本文件用于选择、修饰和导出统计型赛题图表。

## 选图原则

先问每张图回答论文里的哪个问题。

隐变量估计与不确定性：

- 估计份额或估计得分的时间轨迹图；
- 带上下界或可信区间的不确定性通道图；
- 个体 x 时间热力图；
- 关键时间点的条形图或区间图；
- 确定性、区间宽度、熵、决策边际的分布图。

机制比较：

- 信号 A 对信号 B 的散点图，叠加决策区域或规则输出；
- 排名一致性热力图；
- 按时间或组别的规则差异率图；
- 边界或高影响样本的案例轨迹图；
- 展示哪类信号占主导的权衡散点图。

特征效应：

- 带区间的系数图；
- 通道差异条形图；
- 分组效应热力图；
- 使用混合专家时的门控曲线或偏好曲线；
- 只有在能支持数量/比例结论时才加入小型嵌入饼图。

如果论文只能放三张图，优先选择：

1. 一张解释模型输出和不确定性；
2. 一张回答主要机制比较；
3. 一张支撑因素影响或案例结论。

## 单位与坐标轴

不要因为数值范围类似就把不同单位叠在一张图里。

- 两个归一化信号都在 0 到 1，也可能含义不同；要么解释清楚，要么拆图。
- 原始分数、排名、归一化份额、综合分数，默认分面或分图展示，除非已经转换成共同指数。
- 使用综合分数时，图注或正文必须给出公式。
- 对象离开分母集合或取值为结构性零后，不再继续画轨迹。

解释末期低份额前，先验证分母集合是否正确。

## 样式要求

论文/PPT 图表建议：

- 默认白色背景；
- 需要清爽论文图时去掉网格线；
- 坐标轴和边框用黑色，必要时加粗；
- 刻度线要清晰可见；
- 标签字号一致且可读；
- 英文论文图可用 `Times New Roman`;
- SVG 文字可编辑：`matplotlib.rcParams["svg.fonttype"] = "none"`;
- 同时导出高 DPI PNG 和 SVG。

Matplotlib 模板：

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["font.family"] = "Times New Roman"
mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
ax.grid(False)
for spine in ax.spines.values():
    spine.set_color("black")
    spine.set_linewidth(2.5)
ax.tick_params(axis="both", which="both", direction="out", length=6, width=1.6, colors="black")
ax.set_xlabel("X label", fontsize=24, fontweight="bold")
ax.set_ylabel("Y label", fontsize=24, fontweight="bold")
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(24)
    label.set_fontweight("bold")
```

不要把 `grid_*` 参数传给 `tick_params`；网格样式属于 `ax.grid(...)`。

## 配色

用颜色表达结论：

- 不同实体曲线使用 paired 或分类色板；
- 效应大小使用顺序色板或发散色板；
- 高密度散点使用 alpha blending；
- 条形和散点同时出现时，用可区分的颜色；
- 粉彩色可以用，但不能牺牲可读性。

密度映射必须说明密度变量，并提供 colorbar 或图例。

不要只依赖很细微的颜色差异；必要时加入点形、线型、标签或分面。

## 图例与注释

- 图例放在图内时，不能遮挡关键数据。
- 背景复杂或散点密集时，给图例加边框。
- 系列很多时，用两列图例。
- 避免重复图例项，只给第一次出现的对象设置 label。
- 已知事件、边界样本或规则变化能解释结果时，添加短注释。

## 导出约定

最终图同时保存位图和矢量图：

```python
fig.tight_layout()
fig.savefig("figure_name.png", dpi=300, bbox_inches="tight")
fig.savefig("figure_name.svg", bbox_inches="tight")
```

结果报告同时导出：

- 画图用的精确 CSV；
- 包含关键数值的文本或 Markdown 摘要；
- 图文件名与论文位置的对应表。
