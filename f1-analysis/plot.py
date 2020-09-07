"""Functions for builing plots and plot settings"""

import matplotlib.pyplot as plt
import seaborn as sns

import data_tools
import style


# plot style settings
sns.set_style("whitegrid")
plt.rc("font", size=14)  # controls default text sizes
plt.rc("axes", titlesize=14)  # fontsize of the axes title
plt.rc("axes", labelsize=14)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=14)  # fontsize of the tick labels
plt.rc("ytick", labelsize=14)  # fontsize of the tick labels
plt.rc("legend", fontsize=14)  # legend fontsize
plt.rc("figure", titlesize=14)  # fontsize of the figure title
plt.rcParams["font.monospace"] = "consolas"
plt.rcParams["font.sans-serif"] = ["arial"]
plt.rcParams["font.serif"] = "times new roman"
plt.rcParams["font.family"] = "sans-serif"


def delta_chart(
    ergast, race, tgt_driver, driver_ids=None, driver_refs=None, driver_codes=None,
    figsize=(12, 7)
):
    raceId = data_tools.get_race_id(ergast, race)

    delta_table = data_tools.make_delta_table(
        ergast,
        raceId=raceId,
        tgt_driver=tgt_driver,
        driver_ids=driver_ids,
        driver_codes=driver_codes,
        driver_refs=driver_refs,
    )

    fig, ax = plt.subplots(figsize=figsize)
    sns.lineplot(
        data=delta_table,
        x="lap",
        y="delta_seconds",
        hue="driverRef",
        palette=data_tools.get_driver_color_dict(ergast, raceId, key="ref"),
        style="driverRef",
        dashes=style.dashes_2020,
        ax=ax,
    )

    ax.set(xlabel="lap", ylabel="seconds", title="delta from " + tgt_driver)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # seaborn specific remove legend title
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=handles[1:],  # remove seaborn default legend title
        labels=labels[1:],  # remove seaborn default legend title
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        frameon=False,
    )
    return fig, ax


def tire_overlay(ax):
    sns.lineplot(
        data=delta_table,
        x="lap",
        y="delta_seconds",
        hue="driverRef",
        palette=data_tools.get_driver_color_dict(ergast, raceId, key="ref"),
        style="driverRef",
        dashes=style.dashes_2020,
        ax=ax,
        ls=100
    )
