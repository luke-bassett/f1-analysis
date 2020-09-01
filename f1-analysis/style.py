"""Style config used for plotting"""

# Colors extracted from images on formula1.com.
team_colors = {
    "mercedes": "#03d1bf",
    "ferrari": "#dc0000",
    "red_bull": "#1b43ff",
    "renault": "#FFF500",
    "haas": "#9c9c9c",
    "racing_point": "#f496c8",
    "alphatauri": "#15151d",
    "mclaren": "#ff8700",
    "alfa": "#9a0000",
    "williams": "#459bfe",
}

# based on t-cam color; black is solid yellow is dashed
solid = (1, 0)
dashed = (3, 1)
dashes_2020 = {
    # qualified formula 1 drivers
    "hamilton": solid,
    "bottas": dashed,
    "max_verstappen": solid,
    "albon": dashed,
    "perez": solid,
    "stroll": dashed,
    "ricciardo": solid,
    "ocon": dashed,
    "gasly": dashed,
    "kvyat": solid,
    "sainz": solid,
    "norris": dashed,
    "leclerc": dashed,
    "vettel": solid,
    "raikkonen": solid,
    "giovinazzi": dashed,
    "russell": solid,
    "latifi": dashed,
    "kevin_magnussen": dashed,
    "hulkenberg": solid,
    # other
    "grosjean": solid,
}
