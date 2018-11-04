import matplotlib.pyplot as plt
import tkinter as tk
import math
import v2


# Loading the Map
path = "C:/Users/Péridot/AppData/Local/osu!/Songs"
folder = "387311 Inferi - Those Who from the Heavens Came"
map_name = "Inferi - Those Who from the Heavens Came (Mazzerin) [Fengshen Yanyi]"
ht = False
ft = False
dt = False


map = v2.osu_map(path, folder, map_name)
objects = v2.objects(map)
active_objects = v2.active_objects(objects)
active_timestamps = v2.timestamps(active_objects, ht, ft, dt)
active_periods = v2.periods(active_timestamps)

speed = v2.speed(active_timestamps)
stamina = v2.stamina(active_timestamps)
print("Speed* =", v2.global_speed(speed))
print("Stamina* =", v2.global_stamina(stamina))


# Graphic Part
speed_x, stamina_x = [], list(stamina.keys())
speed_y, stamina_y = [], list(stamina.values())

for i in range(len(speed) - 1):
	speed_x.append(list(speed.keys())[i])
	speed_y.append(list(speed.values())[i])
	speed_x.append(list(speed.keys())[i + 1] - 1e-9)
	speed_y.append(list(speed.values())[i])
speed_x.append(active_timestamps[-1])
speed_y.append(speed_y[-1])

plt.plot(speed_x, speed_y, color="#ff0000", label="Speed")
plt.plot(stamina_x, stamina_y, color="#ff8000", label="Stamina")

plt.xlabel("Time (ms)")
plt.ylabel("Value")

plt.legend()
plt.grid(True)
plt.show()

# Pre-calculation for Window
fps = 20
fps = int(1000 / fps)

t = fps
speed_coeff, stamina_coeff = 0, 0
speed_i, stamina_i = 0, 0

speed_displayed = [0]
stamina_displayed = [0]

while t < active_timestamps[-1]:
	if speed_i < len(speed_x) - 2 and stamina_i < len(stamina_x) - 2:
		if speed_x[speed_i] < t:
			speed_coeff = (speed_y[speed_i + 1] - speed_y[speed_i]) / (speed_x[speed_i + 1] - speed_x[speed_i])
			speed_i += 1
		if stamina_x[stamina_i] < t:
			stamina_coeff = (stamina_y[stamina_i + 1] - stamina_y[stamina_i]) / (stamina_x[stamina_i + 1] - stamina_x[stamina_i])
			stamina_i += 1

		speed_append = int((t - speed_x[speed_i]) * speed_coeff + speed_y[speed_i])
		stamina_append = int((t - stamina_x[stamina_i]) * stamina_coeff + stamina_y[stamina_i])
		if speed_coeff >= 0 and speed_append > speed_y[speed_i + 1] or speed_coeff <= 0 and speed_append < speed_y[speed_i + 1]:
			speed_append = int(speed_y[speed_i + 1])
		if stamina_coeff >= 0 and stamina_append > stamina_y[stamina_i + 1] or stamina_coeff <= 0 and stamina_append < stamina_y[stamina_i + 1]:
			speed_append = int(speed_y[speed_i + 1])

		speed_displayed.append(str(speed_append))
		stamina_displayed.append(str(stamina_append))
	t += fps

# Creating the Displaying Window
s = 0
paused = False
def pause():
	global paused, pause_text
	if paused:
		paused = False
		pause_text.set("Pause")
	else:
		paused = True
		pause_text.set("Unpause")

def stream_refresh():
	global s
	if not paused and s < len(speed_displayed):
		speed_window.set(speed_displayed[s])
		stamina_window.set(stamina_displayed[s])
		timer_text.set(str(int(s * fps / 1000)) + "\"")
		s += 1
	stream_window.after(fps, stream_refresh)

stream_window = tk.Tk()
stream_window.title("osu!v2 - " + map_name)
stream_window.geometry("300x350")

timer_text = tk.StringVar()
timer_text.set("0.00\"")
timer = tk.Label(stream_window, textvariable=timer_text, font="Aller 16")
timer.pack()

pause_text = tk.StringVar()
pause_text.set("Pause")
pause_button = tk.Button(stream_window, textvariable=pause_text, command=pause, font="Aller 9")
pause_button.pack()


label = tk.LabelFrame(stream_window, text="Speed Value", font="Aller 18")
label.pack_propagate(0)
speed_window = tk.StringVar()
tk.Label(label, textvariable=speed_window, font="Aller 72", fg="#C00000").pack()
label.pack(fill="both", expand="yes")

label = tk.LabelFrame(stream_window, text="Stamina Value", font="Aller 18")
label.pack_propagate(0)
label.pack(fill="both", expand="yes")
stamina_window = tk.StringVar()
tk.Label(label, textvariable=stamina_window, font="Aller 72", fg="#C06000").pack()

stream_refresh()
stream_window.mainloop()
