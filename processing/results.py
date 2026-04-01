import pandas as pd
import json
import os

def load_races():

    files = [
        "data/cache/iR_2026_S1_Sportscar_Races.json",
        "data/cache/iR_2026_S2_Sportscar_Races.json"
    ]

    all_races = []

    for file in files:

        # Load the raw JSON
        with open(file) as f:
            raw = json.load(f)

        open_file = pd.json_normalize(raw[0])
        all_races.append(open_file)
    
    combined = pd.concat(all_races)

    combined = combined.rename(columns={
        "track.track_id": "track_id",
        "track.track_name": "track_name",
        "track.config_name": "track_config"
    })
    combined.to_csv("data/cache/races.csv", index=False)
    print("💾 Saved to data/cache/races.csv")
    return combined

if __name__ == "__main__":
    df = load_races()
    print(df.shape)
    print(df.columns.tolist())
    print(df[["track_name", "track_config", "finish_position"]].head())