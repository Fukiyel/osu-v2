import matplotlib.pyplot as plt
import v2


# Input
path = "C:/Users/Péridot/AppData/Local/osu!/Songs"
folder = "461744 Imperial Circus Dead Decadence - Yomi yori Kikoyu, Koukoku no Tou to Honoo no Shoujo"
map_name = "Imperial Circus Dead Decadence - Yomi yori Kikoyu, Koukoku no Tou to Honoo no Shoujo. (DoKito) [Kyouaku]"
ht = False
ft = False
dt = False


# Calculating v2
map = v2.osu_map(path, folder, map_name)
objects = v2.active_objects(v2.objects(map))

coordinates = v2.coordinates(objects)
spacing = v2.spacing(coordinates)
timestamps = v2.timestamps(objects, ht, ft, dt)

aim = v2.aim(spacing, timestamps)
speed = v2.speed(timestamps)
stamina = v2.stamina(timestamps)

print("max Aim =", max(aim))
print("Speed* =", v2.global_speed(speed))
print("Stamina* =", v2.global_stamina(stamina))


# Graphic Part
aim_x, aim_y = timestamps, [0] + aim
speed_x, speed_y = [], []
stamina_x, stamina_y = list(stamina.keys()), list(stamina.values())

for i in range(len(speed) - 1):
	speed_x.append(list(speed.keys())[i])
	speed_y.append(list(speed.values())[i])
	speed_x.append(list(speed.keys())[i + 1] - 1e-9)
	speed_y.append(list(speed.values())[i])
speed_x.append(timestamps[-1])
speed_y.append(speed_y[-1])


plt.plot(aim_x, aim_y, color="#0080ff", label="Aim", linewidth=1)
plt.plot(speed_x, speed_y, color="#ff0000", label="Speed", linewidth=.5)
plt.plot(stamina_x, stamina_y, color="#ff8000", label="Stamina", linewidth=.5)

plt.xlabel("Time (ms)")
plt.ylabel("Value")

plt.legend()
plt.grid(True)
plt.show()
