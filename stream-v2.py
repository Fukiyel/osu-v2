import matplotlib.pyplot as plt
import tkinter as tk


def spdGraph():
	spdGraph = [0]
	for i, val in enumerate(osu_periods):
		spdGraph.append(.1 * (1000 / val) ** 3)
	return spdGraph
def staGraph():
	staGraph = [0]
	break_counter = 0
	for i in range(len(staBookmarks) - 1):
		if staBookmarks[i + 1] in osu_breaks:
			break_counter += 1
			staGraph.append(0)
		else:
			if staGraph[-1] + 10 - (.9 * osu_periods[i - break_counter]) ** .5 > 0:
				staGraph.append(staGraph[-1] + 10 - (.9 * osu_periods[i - break_counter]) ** .5)
			else:
				staGraph.append(0)
	return staGraph


def HT(timestamps):
	for i in range(len(timestamps)):
		timestamps[i] = timestamps[i] / 0.75
	return timestamps
def FT(timestamps):
	for i in range(len(timestamps)):
		timestamps[i] = timestamps[i] / 1.25
	return timestamps
def DT(timestamps):
	for i in range(len(timestamps)):
		timestamps[i] = timestamps[i] / 1.5
	return timestamps


# Loading the Map
map_name = "Imperial Circus Dead Decadence - Yomi yori Kikoyu, Koukoku no Tou to Honoo no Shoujo. (DoKito) [Kyouaku]"

HalfTime = False
FasterTime = False
DoubleTime = False

osu_map = open("D:/Code/Python/osu!v2Streams/" + map_name + ".osu", "r", encoding="utf8").read()
osu_objects = osu_map.split("[HitObjects]\n")[1].split("\n")
osu_raw_breaks = osu_map.split("//")[2].lstrip("Break Periods\n").split("\n")

osu_raw_breaks.remove("")
osu_objects.remove("")

for i in range(len(osu_raw_breaks)):
	osu_raw_breaks[i] = int(osu_raw_breaks[i].split(",")[1])


osu_raw_active_timestamps = []
osu_active_timestamps = []
osu_breaks = []
osu_periods = []

for i in range(len(osu_objects)):
	osu_objects[i] = osu_objects[i].split(",")
	if not int(osu_objects[i][3]) & (1 << 3):
		osu_raw_active_timestamps.append(int(osu_objects[i][2]))


if HalfTime:
	osu_active_timestamps = HT(osu_raw_active_timestamps)
	osu_breaks = HT(osu_raw_breaks)
elif FasterTime:
	osu_active_timestamps = FT(osu_raw_active_timestamps)
	osu_breaks = FT(osu_raw_breaks)
elif DoubleTime:
	osu_active_timestamps = DT(osu_raw_active_timestamps)
	osu_breaks = DT(osu_raw_breaks)
else:
	osu_active_timestamps = osu_raw_active_timestamps
	osu_breaks = osu_raw_breaks


for i in range(len(osu_active_timestamps) - 1):
	osu_periods.append(osu_active_timestamps[i + 1] - osu_active_timestamps[i])


staBookmarks = sorted(osu_active_timestamps + osu_breaks)
osu_spdGraph = spdGraph()
osu_staGraph = staGraph()


# Creating Active Timestamps File
results = ""
for i in range(len(osu_active_timestamps)):
		results += str(osu_active_timestamps[i])
		results += "\n"
results_file = open("D:/Code/Python/osu!v2Streams/[osu!v2 - Speed] " + map_name + ".txt","w")
results_file.write(results)


# Iterations of Periods
"""periodsDict = {}
for i in range(len(osu_periods)):
	if osu_periods[i] in periodsDict:
		periodsDict[osu_periods[i]] += 1
	else:
		periodsDict[osu_periods[i]] = 1"""


# Pre-calculation for Window
position = 0
section = 0
spd_coeff = 0
sta_coeff = 0
val_index = 0
score_index = 0


speed_displayed = []
stamina_displayed = []
while position <= osu_active_timestamps[-1]:
	if not section >= len(osu_active_timestamps):
		if position > osu_active_timestamps[section]:
			spd_coeff = (osu_spdGraph[section + 1] - osu_spdGraph[section]) / osu_periods[section]
			sta_coeff = (osu_staGraph[section + 1] - osu_staGraph[section]) / osu_periods[section]
			speed_displayed.append(str(int((position - osu_active_timestamps[section]) * spd_coeff + osu_spdGraph[section])))
			stamina_displayed.append(str(round((position - osu_active_timestamps[section]) * sta_coeff + osu_staGraph[section], 1)))
			section += 1
		else:
			speed_displayed.append(str(int((position - osu_active_timestamps[section]) * spd_coeff + osu_spdGraph[section])))
			stamina_displayed.append(str(round((position - osu_active_timestamps[section]) * sta_coeff + osu_staGraph[section], 1)))
	position += 40


print("Stamina* =", max(osu_staGraph))


# Graphic Part
#plt.plot(osu_active_timestamps, osu_spdGraph, color="#ff0040", label="Speed", linewidth=0.2)
plt.plot(staBookmarks, osu_staGraph, color="#ff4000", label="Stamina")

plt.xlabel("Time (ms)")
plt.ylabel("Value")

plt.legend()
plt.grid(True)
plt.show()

# Creating the Displaying Window
def stream_refresh():
	global val_index
	#spd_value.set(speed_displayed[val_index])
	sta_value.set(stamina_displayed[val_index])
	val_index += 1
	stream_window.after(40, stream_refresh)


stream_window = tk.Tk()
stream_window.title("osu!v2 - " + map_name)
stream_window.geometry("400x175")
# vvv For when i'll find a gud system for speed vvv
"""
label = tk.LabelFrame(stream_window, text="Speed Value", font="Aller 18")
label.pack_propagate(0)
label.pack(fill="both", expand="yes")
spd_value = tk.StringVar()
tk.Label(label, textvariable=spd_value, font="Aller 72").pack()
"""
label = tk.LabelFrame(stream_window, text="Stamina Value", font="Aller 18")
label.pack_propagate(0)
label.pack(fill="both", expand="yes")
sta_value = tk.StringVar()
tk.Label(label, textvariable=sta_value, font="Aller 72").pack()

stream_refresh()
stream_window.mainloop()
