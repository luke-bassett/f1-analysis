"""Fuctions for transforming and referencing"""

import style


def load_race_laps(ergast, raceId):
    """return dataframe from laps_times table for a race"""
    laps = ergast.data["lap_times"].copy()
    laps = laps[laps["raceId"] == raceId]
    return laps


def load_race_results(ergast, raceId):
    """return dataframe from results table for a race"""
    res = ergast.data["results"].copy()
    res = res[res["raceId"] == raceId]
    return res


def calc_total_milliseconds(df):
    """returns copy of df with total_milliseconds added"""
    df["total_milliseconds"] = df.groupby("driverId")["milliseconds"].cumsum()
    return df.copy()


def tgt_driver_delta(grp, tgt):
    """to use with groupby: finds delta between tgt and other drivers in race"""
    tgt_time = grp.loc[grp["driverId"] == tgt, "total_milliseconds"].to_numpy()[0]
    grp["delta"] = grp["total_milliseconds"] - tgt_time
    return grp


def get_driver_codes(ergast):
    """return dict where key is driverId and val is code"""
    return ergast.data["drivers"].set_index("driverId")[["code"]].to_dict()["code"]


def make_delta_table(
    ergast, raceId, tgt_driver, driver_ids=None, driver_refs=None, driver_codes=None
):
    """tgt_driver must be reference(str) or id(int)"""

    if isinstance(tgt_driver, str):
        tgt_driver = get_driverref_to_driverid_dict(ergast)[tgt_driver]

    laps = load_race_laps(ergast, raceId)

    laps = calc_total_milliseconds(laps)

    if driver_ids:
        laps = laps[laps["driverId"].isin(driver_ids)]
    elif driver_refs:
        laps["driverRef"] = laps["driverId"].map(get_driverid_to_driverref_dict(ergast))
        laps = laps[laps["driverRef"].isin(driver_refs)]
    elif driver_codes:
        codes = get_driver_codes(ergast)
        laps["driver_code"] = laps["driverId"].map(codes)
        laps = laps[laps["driver_code"].isin(driver_codes)]

    # remove laps which targer driver did not complete
    laps = laps[laps["lap"] <= laps.loc[laps["driverId"] == tgt_driver, "lap"].max()]

    # calculate delta from target driver each lap
    # (adds "delta" column in milliseconds)
    laps = laps.groupby("lap").apply(tgt_driver_delta, tgt_driver)
    laps["delta_seconds"] = laps["delta"] * 0.001

    laps["driverRef"] = laps["driverId"].map(
        get_driverid_to_driverref_dict(ergast, laps["driverId"].unique())
    )

    return laps


def get_driver_color_dict(ergast, raceId, key="id"):
    """return a dictionary with driverId as key and hex color as val"""

    res = load_race_results(ergast, raceId)
    driver_ids = res["driverId"].unique()

    colors = {}
    for driverId in driver_ids:
        constructorId = res.loc[
            res["driverId"] == driverId, "constructorId"
        ].to_numpy()[0]
        con = ergast.data["constructors"].copy()
        constructor = con.loc[
            con["constructorId"] == constructorId, "constructorRef"
        ].to_numpy()[0]
        colors[driverId] = style.team_colors[constructor]

    if key == "ref":
        id_to_ref = get_driverid_to_driverref_dict(ergast, driver_ids)
        ref_colors = {id_to_ref[k]: v for k, v in colors.items()}
        return ref_colors
    return colors


def get_driverid_to_driverref_dict(ergast, driver_ids="all"):
    """return a dict where key is driverId and val is code"""
    d = ergast.data["drivers"].copy()

    if str(driver_ids) != "all":
        driver_ids = list(driver_ids)
        d = d[d["driverId"].isin(driver_ids)]

    d.set_index("driverId", inplace=True)
    return d["driverRef"].to_dict()


def get_driverid_to_code_dict(ergast, driver_ids="all"):
    """return a dict where key is driverId and val is code"""
    d = ergast.data["drivers"].copy()

    if str(driver_ids) != "all":
        driver_ids = list(driver_ids)
        d = d[d["driverId"].isin(driver_ids)]

    d.set_index("driverId", inplace=True)
    return d["code"].to_dict()


def get_code_to_driverid_dict(ergast, codes="all"):
    """return a dict where key is code and val is driverId"""
    d = ergast.data["drivers"].copy()

    if str(codes) != "all":
        codes = list(codes)
        d = d[d["code"].isin(codes)]

    d = d[d["code"] != "\\N"]

    d.set_index("code", inplace=True)
    return d["driverId"].to_dict()


def get_driverref_to_driverid_dict(ergast, driver_refs="all"):
    """return a dict where key is driverId and val is code"""
    d = ergast.data["drivers"].copy()

    if str(driver_refs) != "all":
        driver_refs = list(driver_refs)
        d = d[d["driverRef"].isin(driver_refs)]

    d.set_index("driverRef", inplace=True)
    return d["driverId"].to_dict()


def driverid_to_driverref(driver_ids):
    d = get_driverid_to_driverref_dict(list(driver_ids))
    return [d[x] for x in driver_ids]


def get_race_id(ergast, race):
    if isinstance(race, int):
        return race

    races = ergast.data["races"].copy()

    if isinstance(race, str):
        races["text_id"] = (
            races["year"].astype(str)
            + "_"
            + races["name"].str.replace(" ", "_").str.lower()
        )
        return races.loc[races["text_id"] == race, "raceId"].array[0]

    elif isinstance(race, tuple):
        return races.loc[
            (races["year"] == race[0]) & (races["round"] == race[1]), "raceId"
        ].array[0]
