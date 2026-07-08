# FIGURE 2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
df = pd.read_csv("fig2.csv", sep=";").dropna()
df = df.rename(columns={"Control/CHD": "Group"})
sns.set(style="white")
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
colors = {"CHD": "red", "Control": "blue"}
positions = {
    "CHD": [0, 1],
    "Control": [3, 4]}
def plot_panel(ax, var_rest, var_max, ylabel, title):
    for x in [0, 1, 3, 4]:
        ax.axvline(x, color='lightgray', lw=1, zorder=0)
    for group in ["CHD", "Control"]:
        data = df[df["Group"] == group]
        x_rest, x_max = positions[group]
        for _, row in data.iterrows():
            ax.plot([x_rest, x_max],
                    [row[var_rest], row[var_max]],
                    color=colors[group],
                    alpha=0.8,
                    linewidth=0.8,
                    zorder=1)
        ax.scatter([x_rest] * len(data),
                   data[var_rest],
                   color=colors[group],
                   s=25,
                   zorder=2)
        ax.scatter([x_max] * len(data),
                   data[var_max],
                   color=colors[group],
                   s=25,
                   zorder=2)
        x = np.array(
            [x_rest] * len(data) +
            [x_max] * len(data))
        y = np.array(
            list(data[var_rest]) +
            list(data[var_max]))
        slope, intercept = np.polyfit(x, y, 1)
        x_line = np.linspace(x_rest, x_max, 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line,
            y_line,
            color='black',
            linewidth=2,
            linestyle=(0, (2, 2)),
            zorder=5)
        print(f"{title} - {group} slope: {slope:.3f}")
        ax.boxplot(
            [data[var_rest], data[var_max]],
            positions=[x_rest, x_max],
            widths=0.28,
            patch_artist=True,
            boxprops=dict(
                facecolor='none',
                edgecolor='black',
                linewidth=1.5,
                zorder=4),
            whiskerprops=dict(
                color='black',
                linewidth=1.5,
                zorder=4),
            capprops=dict(
                color='black',
                linewidth=1.5,
                zorder=4),
            medianprops=dict(
                color='black',
                linewidth=1.5,
                zorder=5))
    ax.set_xticks([0, 1, 3, 4])
    ax.set_xticklabels(["Rest", "Max", "Rest", "Max"])
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(bottom=0)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(False)
plot_panel(
    axes[0],
    "SV_rest",
    "SV_max",
    "SV (mL)",
    "Stroke Volume")
axes[0].text(
    -0.08, 1.08, "A",
    transform=axes[0].transAxes,
    fontsize=14,
    fontweight='bold',
    ha='left',
    va='top')
plot_panel(
    axes[1],
    "VO2_kg_rest",
    "VO2_kg_max",
    "VO$_2$ (mL/kg/min)",
    "Oxygen Uptake (VO$_2$)")
axes[1].text(
    -0.08, 1.08, "B",
    transform=axes[1].transAxes,
    fontsize=14,
    fontweight='bold',
    ha='left',
    va='top')
legend_elements = [
    Line2D([0], [0], color='red', lw=2, label='CHD'),
    Line2D([0], [0], color='blue', lw=2, label='Control')]
axes[0].legend(handles=legend_elements, loc='upper left')
axes[1].legend(handles=legend_elements, loc='upper left')
fig.supxlabel("Stages of exercise")
plt.tight_layout()
plt.savefig("Figure 2.png", dpi=300, bbox_inches="tight")
plt.show()


# FIGURE 3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
df = pd.read_csv("fig3.csv", sep=";")
df = df.dropna(subset=["Age group"])
groups = ["CHD", "Control"]
def create_summary(df, category_col, categories):
    summary = []
    for category in categories:
        for group in groups:
            vals = df[
                (df[category_col] == category) &
                (df["Control/CHD"] == group)
            ]["SVI_max"]
            n = len(vals)
            mean = vals.mean()
            if n > 1:
                sem = vals.std(ddof=1) / np.sqrt(n)
                ci95 = 1.96 * sem
            else:
                ci95 = 0
            summary.append({
                category_col: category,
                "Group": group,
                "Mean": mean,
                "CI95": ci95})
    return pd.DataFrame(summary)
age_order = [
    "Children",
    "Adults"]
age_summary = create_summary(
    df,
    "Age group",
    age_order)
sex_order = [
    "Female",
    "Male"]
sex_summary = create_summary(
    df,
    "Sex",
    sex_order)
fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 6),
    sharey=True)
def plot_panel(ax, summary, categories, xlabel):
    x = np.arange(len(categories))
    width = 0.35
    chd = summary[
        summary["Group"] == "CHD"]
    control = summary[
        summary["Group"] == "Control"]
    ax.bar(
        x - width/2,
        chd["Mean"],
        width,
        color="red",
        yerr=chd["CI95"],
        capsize=5)
    ax.bar(
        x + width/2,
        control["Mean"],
        width,
        color="blue",
        yerr=control["CI95"],
        capsize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_xlabel(xlabel)
plot_panel(
    axes[0],
    age_summary,
    age_order,
    "Age group")
plot_panel(
    axes[1],
    sex_summary,
    sex_order,
    "Sex")
axes[0].set_ylabel(
    "SVI (mL/m²)")
axes[0].text(
    -0.08,
    1.03,
    "A",
    transform=axes[0].transAxes,
    fontsize=16,
    fontweight="bold",
    va="top")
axes[1].text(
    -0.08,
    1.03,
    "B",
    transform=axes[1].transAxes,
    fontsize=16,
    fontweight="bold",
    va="top")
legend_elements = [
    Line2D(
        [0],
        [0],
        color="red",
        lw=2,
        label="CHD"),
    Line2D(
        [0],
        [0],
        color="blue",
        lw=2,
        label="Control")]
axes[0].legend(
    handles=legend_elements,
    loc="upper left",
    frameon=True)
axes[1].legend(
    handles=legend_elements,
    loc="upper left",
    frameon=True)
plt.tight_layout()
plt.savefig(
    "Figure 3.png",
    dpi=300,
    bbox_inches="tight")
plt.show()


# FIGURE 4 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
def load_dataset(file, value_name):
    df = pd.read_csv(file, sep=";", header=None)
    groups = df.iloc[0].values
    data = df.iloc[2:].reset_index(drop=True)
    records = []
    max_pairs = min(len(groups), data.shape[1])
    for i in range(0, max_pairs, 2):
        if i + 1 >= data.shape[1]:
            break
        group = groups[i]
        vo2 = pd.to_numeric(data.iloc[:, i], errors="coerce")
        val = pd.to_numeric(data.iloc[:, i + 1], errors="coerce")
        records.append(pd.DataFrame({
            "Group": group,
            "VO2_pct": vo2,
            value_name: val}))
    df_long = pd.concat(records, ignore_index=True).dropna()
    return df_long[df_long["Group"] == "Control"], df_long[df_long["Group"] == "CHD"]
def plot_smooth_lowess_with_anchors(ax, df, y_col, color, label):
    x = df["VO2_pct"].values
    y = df[y_col].values
    x_grid = np.linspace(0, 100, 200)
    smoothed = lowess(y, x, frac=0.4, return_sorted=True)
    x_s, y_s = smoothed[:, 0], smoothed[:, 1]
    y_lowess = np.interp(x_grid, x_s, y_s)
    mean_0 = df.loc[df["VO2_pct"] == 0, y_col].mean()
    mean_100 = df.loc[df["VO2_pct"] == 100, y_col].mean()
    w = np.ones_like(x_grid)
    left = x_grid <= 15
    right = x_grid >= 85
    w[left] = 0.5 * (1 - np.cos(np.pi * x_grid[left] / 15))
    w[right] = 0.5 * (1 - np.cos(np.pi * (100 - x_grid[right]) / 15))
    anchor = np.interp(
        x_grid,
        [0, 100],
        [mean_0, mean_100])
    y_final = w * y_lowess + (1 - w) * anchor
    n_boot = 300
    boot_preds = np.zeros((n_boot, len(x_grid)))
    for i in range(n_boot):
        idx = np.random.choice(len(x), len(x), replace=True)
        xb, yb = x[idx], y[idx]
        sm = lowess(yb, xb, frac=0.4, return_sorted=True)
        xb_s, yb_s = sm[:, 0], sm[:, 1]
        boot_lowess = np.interp(x_grid, xb_s, yb_s)
        boot_preds[i] = w * boot_lowess + (1 - w) * anchor
    lower = np.percentile(boot_preds, 2.5, axis=0)
    upper = np.percentile(boot_preds, 97.5, axis=0)
    ax.plot(x_grid, y_final, color=color, linewidth=2, label=label)
    ax.fill_between(x_grid, lower, upper, color=color, alpha=0.2)
control_svi, chd_svi = load_dataset("fig4svi.csv", "SVI")
control_hr, chd_hr = load_dataset("fig4hr.csv", "HR")
control_ci, chd_ci = load_dataset("fig4ci.csv", "CI")
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True)
plot_smooth_lowess_with_anchors(axes[0], control_svi, "SVI", "blue", "Control")
plot_smooth_lowess_with_anchors(axes[0], chd_svi, "SVI", "red", "CHD")
axes[0].set_title("Stroke Volume Index")
axes[0].set_ylabel("SVI (mL/m²)")
axes[0].legend(loc="lower right")
axes[0].set_box_aspect(1)
axes[0].text(-0.15, 1.08, "A",
             transform=axes[0].transAxes,
             fontsize=14,
             fontweight="bold",
             va="top")
plot_smooth_lowess_with_anchors(axes[1], control_hr, "HR", "blue", "Control")
plot_smooth_lowess_with_anchors(axes[1], chd_hr, "HR", "red", "CHD")
axes[1].set_title("Heart Rate")
axes[1].set_ylabel("HR (bpm)")
axes[1].legend(loc="lower right")
axes[1].set_box_aspect(1)
axes[1].text(-0.15, 1.08, "B",
             transform=axes[1].transAxes,
             fontsize=14,
             fontweight="bold",
             va="top")
plot_smooth_lowess_with_anchors(axes[2], control_ci, "CI", "blue", "Control")
plot_smooth_lowess_with_anchors(axes[2], chd_ci, "CI", "red", "CHD")
axes[2].set_title("Cardiac Index")
axes[2].set_ylabel("CI (L/min/m²)")
axes[2].legend(loc="lower right")
axes[2].set_box_aspect(1)
axes[2].text(-0.15, 1.08, "C",
             transform=axes[2].transAxes,
             fontsize=14,
             fontweight="bold",
             va="top")
for ax in axes:
    ax.set_xlabel("% VO$_2$ max")
    ax.set_xlim(0, 100)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("Figure 4.png", dpi=300)
plt.show()


# FIGURE 5
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("fig5.csv", sep=";")
df.columns = df.columns.str.strip()
df = df.rename(columns={
    "Control/CHD": "Group",
    "O2 pulse (mL/beat)": "O2_pulse",
    "SV (mL)": "SV"})
df["O2_pulse"] = pd.to_numeric(df["O2_pulse"], errors="coerce")
df["SV"] = pd.to_numeric(df["SV"], errors="coerce")
df = df.dropna(subset=["Group", "O2_pulse", "SV"])
control = df[df["Group"] == "Control"]
chd = df[df["Group"] == "CHD"]
plt.figure(figsize=(5,5))
ax = plt.gca()
plt.scatter(control["SV"], control["O2_pulse"], color="blue", s=25, label="Control")
plt.scatter(chd["SV"], chd["O2_pulse"], color="red", s=25, label="CHD")
xmin, xmax = 0, df["SV"].max() + 10
plt.xlim(xmin, xmax)
plt.ylim(0, df["O2_pulse"].max() + 2)
xmin = 0
xmax = df["SV"].max() + 20
x_line = np.linspace(xmin, xmax, 200)
if len(control) > 1:
    m_c, b_c = np.polyfit(control["SV"], control["O2_pulse"], 1)
    plt.plot(x_line, m_c * x_line + b_c, color="blue", linewidth=1)
if len(chd) > 1:
    m_h, b_h = np.polyfit(chd["SV"], chd["O2_pulse"], 1)
    plt.plot(x_line, m_h * x_line + b_h, color="red", linewidth=1)
plt.xlabel("Stroke Volume (mL/beat)")
plt.ylabel("O$_2$ pulse (mL/beat)")
plt.xticks(np.arange(0, df["SV"].max() + 20, 20))
plt.yticks(np.arange(0, 31, 5))
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
plt.legend(frameon=True, edgecolor="black", loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Figure 5.png", dpi=300, bbox_inches="tight")
plt.show()