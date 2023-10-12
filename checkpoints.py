import pandas as pd
import argparse

def to_tick(x):
    return int(x * 20)

def to_sec(x):
    return x / 20

target_dir = "AppData/roaming/.minecraft/config/racehud/checkpoints/"

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("-i", "--interval", default=0.05, type=float, help="time interval for checkpoints (default=0.05)")
parser.add_argument("-s", "--start_time", default=0, type=float, help="time at the starting point (default=0)")
parser.add_argument("-d", "--duration", default=0, type=float, help="duration of the lap")
parser.add_argument("-o", "--output", nargs="?", default=None, help="save the file with the filename given")
args = parser.parse_args()

end_time = to_sec(to_tick(args.start_time) + to_tick(args.duration))

times = [to_sec(i) for i in range(to_tick(args.start_time), to_tick(end_time), to_tick(args.interval))]

df = pd.read_csv(args.file)
df["xDir"] = round((df["xPos"].shift(-1) - df["xPos"]) / df["speed"].shift(-1) * 20, 4)
df["zDir"] = round((df["zPos"].shift(-1) - df["zPos"]) / df["speed"].shift(-1) * 20, 4)
df["dotProduct"] = df["xPos"] * df["xDir"] + df["zPos"] * df["zDir"]

df = df[df["time"].isin(times)]
df["time"] = ["{:.2f}".format(t - args.start_time) for t in df["time"]]
df = df[["time", "speed", "xDir", "zDir", "dotProduct"]]

if args.output is not None:
    df.to_csv(target_dir + args.output, index=False, float_format="{:.4f}".format)
