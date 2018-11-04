from statistics import mean, median
from math import exp

__name__ = "osu!v2 - An osu! alternative system by Fukiyel (W.I.P.)"
__doc__ = """
osu!v2 is a concept meant to surpass osu!'s current system.
'System' include Star Rating, PP calculation, Mods options & effects, Scoring, etc.

It is a W.I.P., and I'm currently working on Star Rating calculation.
It will be separated into different aspects like Speed and Stamina, which are respectively in version v5 and v8.
- Speed measures difficulty to click really fast during a short time.
- Stamina measures difficulty to click fast during a long time.

FT, or FastTime is a new mod that increases a map's speed (N.B. not talking about Speed difficulty) by 25%.
It is a between of No-mod and DT.


Functions :
	osu_map() -> Returns the entire string of a map's file
	objects() -> Returns the objects of a map and separate their parameters
	active_objects() -> Filter only clickable objects
	timestamps() -> Returns timestamps of objects
	periods() -> Turns timestamps into periods

	ht() -> Divide periods by .75
	ft() -> Divide periods by 1.25
	dt() -> Divide periods by 1.5

	raw_speed() -> Corresponding raw speed values of entered periods
	speed_blocks() -> Makes blocks of raw speed values
	speed_weighting() -> Weights speed blocks depending of their length
	speed() -> Takes active timestamps and returns weighted speed blocks
	global_speed() -> Turns speed values into a unique one

	absolute_stamina() -> Returns stamina changes of entered periods
	relative_stamina() -> Applies stamina changes to periods
	stamina() -> Takes active timestamps and returns their relative stamina
	global_stamina() -> Turns stamina values into a unique one
"""


def osu_map(path: str, folder: str, map_name: str) -> str:
	"""
	This function takes the path, folder, and map name of an osu!'s map file.
	In result, returns a long string with the full content of the file.

	:param path: Path to where folders of your maps are located.
	:param folder: Name of the folder that contains wanted map.
	:param map_name: Name of the map's file.
	:type path: <str>
	:type folder: <str>
	:type map_name: <str>
	:return: A string contening map's file content.
	:rtype: <str>

	:Example:

	>>> from v2 import *
	>>> map = osu_map("C:/Users/Péridot/AppData/Local/osu!/Songs", "3756 Peter Lambert - osu! tutorial", "Peter Lambert - osu! tutorial (peppy) [Gameplay basics]")
	>>> print(map[:100] + "...etc")
	osu file format v5

	[General]
	AudioFilename: tutorial.ogg
	AudioLeadIn: 0
	PreviewTime: -1
	Countdown: ...etc
	>>>

	.. seealso:: objects()
	"""
	osu_map = open(path + "/" + folder + "/" + map_name + ".osu", "r", encoding="utf8").read()
	return osu_map
def objects(osu_map: str) -> list:
	"""
	This function takes in entry the string of at least a part of an osu!'s map.
	It returns its objects via a list, and each object is itself a list of its parameters.
	Parameters are x and y coordinates, timestamp, type, hitsound and extras.

	:param osu_map: osu!'s map file.
	:type osu_map: <str>
	:return: A list of objects. Each object is a list of its parameters.
	:rtype: <list> of <list> of <str>

	:Example:

	>>> from v2 import *
	>>> objects = objects("......\n\n[HitObjects]\n65,21,1120,9,6,0:0:0:0:\n72,52,1188,1,8,0:0:0:0:\n80,85,1256,1,8,0:0:0:0:\n88,118,1324,1,8,0:0:0:0:\n96,151,1392,1,8,0:0:0:0:")
	>>> print(objects) # The 'map' used is truncated because of its enormous length
	[['65', '21', '1120', '9', '6', '0:0:0:0:'], ['72', '52', '1188', '1', '8', '0:0:0:0:'], ['80', '85', '1256', '1', '8', '0:0:0:0:'], ['88', '118', '1324', '1', '8', '0:0:0:0:'], ['96', '151', '1392', '1', '8', '0:0:0:0:']]
	>>>

	.. seealso:: active(), periods(), osu_map()
	"""
	objects = osu_map.split("[HitObjects]\n")[1].split("\n")
	objects = [o.split(',') for o in objects] # Separating objects into their parameters

	if "" in objects[-1][0]: # Sometimes last object can be empty
		objects.pop()

	return objects
def active_objects(objects: list) -> list:
	"""
	This function takes a list of objects in entry and returns only active ones.
	Inactive objects are spinners. Active means circle or slider(head).

	:param objects: List of objects.
	:type objects: <list> of <list> of <str>
	:return: All active objects among entered ones.
	:rtype: <list> of <list> of <str>

	:Example:

	>>> from v2 import *
	>>> active_objects = active([['65', '21', '1120', '8', '6', '0:0:0:0:'], ['72', '52', '1188', '1', '8', '0:0:0:0:'], ['80', '85', '1256', '1', '8', '0:0:0:0:']]))
	>>> print(active_objects)
	[['72', '52', '1188', '1', '8', '0:0:0:0:'], ['80', '85', '1256', '1', '8', '0:0:0:0:']]
	>>>

	.. note:: An object is a spinner when the bit 3 (+8 or not) of type value (object[3]) is 1.
	.. seealso:: objects(), timestamps()
	"""
	return [o for o in objects if not (int(o[3]) & (1 << 3))] # Checking if bit for 8 is True or False
def timestamps(objects: list, HT=False, FT=False, DT=False) -> list:
	"""
	This function takes a list of objects in entry and returns their timestamps.
	Timestamps are the exact moment an object should be interacted with in milliseconds.
	They correspond to obj[2].
	HT, FT, and DT parameters correspond if True to ht(timestamps()), ft(timestamps()) and dt(timestamps()).
	Although ht(), ft() and dt() are meant for periods, they also work for timestamps.
	To avoid confusion, it's advised for modding timestamps to pass by parameters of this function and not by mod functions.

	:param objects: List of objects.
	:param HT: Is HalfTime mod on ?
	:param FT: Is FastTime mod on ?
	:param DT: Is DoubleTime mod on ?
	:type objects: <list> of <list> of <str>
	:type HT: <bool>
	:type FT: <bool>
	:type DT: <bool>
	:return: Timestamps of all enetered objects.
	:rtype: <list> of <float>

	:Example:

	>>> from v2 import *
	>>> timestamps = timestamps([['72', '52', '1188', '1', '8', '0:0:0:0:'], ['80', '85', '1256', '1', '8', '0:0:0:0:'], ['88', '118', '1324', '1', '8', '0:0:0:0:'], ['96', '151', '1392', '1', '8', '0:0:0:0:']])
	>>> print(timestamps)
	[1188, 1256, 1324, 1392]
	>>> timestamps = timestamps([['72', '52', '1188', '1', '8', '0:0:0:0:'], ['80', '85', '1256', '1', '8', '0:0:0:0:'], ['88', '118', '1324', '1', '8', '0:0:0:0:'], ['96', '151', '1392', '1', '8', '0:0:0:0:']], DT=True)
	>>> print(timestamps)
	[792.0, 837.3333333333334, 882.6666666666666, 928.0]
	>>>

	.. warning:: HalfTime doesn't double timestamps, neither does DoubleTime halves them.
	.. warning:: Parameters HT, FT, and DT are uppercased to avoid being misinterpreted as the eponym lowercased functions.
	.. seealso:: ht(), ft(), dt(), objects(), periods()
	"""
	timestamps = []

	for i in range(len(objects)):
		timestamps.append(int(objects[i][2]))

	if HT:
		timestamps = ht(timestamps)
	if FT:
		timestamps = ft(timestamps)
	if DT:
		timestamps = dt(timestamps)

	return timestamps
def periods(timestamps: list) -> list:
	"""
	This function takes a list of timestamps of an osu! map's objects, and returns periods each consecutive timestamps.
	Remember that timestamps have 1 more value than their periods.

	:param timestamps: List of timestamps.
	:type timestamps: <list> of <float>
	:return: List of periods between each consecutive timestamps.
	:rtype: <list> of <float>

	:Example:

	>>> from v2 import *
	>>> periods = periods([1500, 1900, 1950, 2123, 2610])
	>>> print(periods)
	[400, 50, 173, 487]
	>>>

	.. seealso:: timestamps(), ht(), ft(), dt()
	"""
	periods = []

	for i in range(len(timestamps) - 1):
		periods.append(timestamps[i + 1] - timestamps[i])

	return periods

# Mods
def ht(periods: list) -> list:
	"""
	This function takes a list of periods to return its simulated equivalent with HT mod.
	HT means HalfTime, but this term is inexact because the speed isn't halved.

	:param periods: List of periods of an osu! map.
	:type periods: <list> of <float>
	:return: The entered list but each period is divided by 0.75.
	:rtype: <list> of <float>

	:Example:

	>>> from v2 import *
	>>> ht_periods = ht([200, 100, 500, 50, 50])
	>>> print(ht_periods)
	[266.6666666666667, 133.33333333333334, 666.6666666666666, 66.66666666666667, 66.66666666666667]

	.. note:: HT mod is equivalent to dividing periods by 0.75, not by 0.5.
	.. seealso:: periods(), ft(), dt()
	"""
	return [p / .75 for p in periods]
def ft(periods: list) -> list:
	"""
	This function takes a list of periods to return its simulated equivalent with FT mod.
	FT means FastTime, a new concept of mod by Fukiyel.

	:param periods: List of periods of an osu! map.
	:type periods: <list> of <float>
	:return: The entered list but each period is divided by 1.25.
	:rtype: <list> of <float>

	:Example:

	>>> from v2 import *
	>>> ft_periods = ft([200, 100, 500, 50, 50])
	>>> print(ft_periods)
	[160.0, 80.0, 400.0, 40.0, 40.0]

	.. seealso:: periods(), ht(), dt()
	"""
	return [p / 1.25 for p in periods]
def dt(periods: list) -> list:
	"""
	This function takes a list of periods to return its simulated equivalent with DT mod.
	DT means DoubleTime, but this term is inexact because the speed isn't doubled.

	:param periods: List of periods of an osu! map.
	:type periods: <list> of <float>
	:return: The entered list but each period is divided by 1.5.
	:rtype: <list> of <float>

	:Example:

	>>> from v2 import *
	>>> dt_periods = dt([200, 100, 500, 50, 50])
	>>> print(dt_periods)
	[133.33333333333334, 66.66666666666667, 333.3333333333333, 33.333333333333336, 33.333333333333336]

	.. note:: DT mod is equivalent to dividing periods by 1.5, not by 2.
	.. seealso:: periods(), ht(), ft()
	"""
	return [p / 1.5 for p in periods]

# Speed*
def raw_speed(active_periods: list) -> list:
	"""
	This function takes active periods and returns a list of corresponding raw speed values.
	"Speed" is a system by Fukiyel which tries to make concrete values of a map's clicking-speed difficulty.
	Raw speed is a part of its calculation, and simply associates a period to a value.
	The more the period is short, the more the value will be high.

	:param active_periods: Periods between clicking objects.
	:type active_periods: <list> of <float>
	:return: List of corresponding raw speed values.
	:rtype: <list> of <float>

	:Example:

	>>> from v2 import *
	>>> raw_values = raw_speed([200, 100, 500, 50, 50])
	>>> print(raw_values)
	[15.625, 125, 1, 1000, 1000]
	>>>

	.. note:: Raw speed values are only a step for calculating speed difficulty.
	.. warning:: Only active periods should be used, make sure spinners aren't took in account.
	.. seealso:: speed_blocks(), speed_weighting(), speed(), global_speed()
	"""
	return [(1000 / p) ** 3 / 8 for p in active_periods]
def speed_blocks(raw_speed: list, timestamps=None, margin=.1) -> dict:
	"""
	This function takes raw speed values and make blocks of them if their values are similar.
	"Speed" is a system by Fukiyel which tries to make concrete values of a map's clicking-speed difficulty.
	Raw speed is a part of its calculation, and so are Speed Blocks.
	A certain margin (by default 10%) is set for a next value to be in the same block as its predecessor.
	Blocks are returned in a dict form, with block ordinals or timestamps as keys and list of raw values as values.

	:param raw_speed: List of raw speed values.
	:param timestamps: Timestamps of all raw speed values.
	:param margin: Margin, by default 0.1, set to be determining if yes or not a value will be a part of the previous value's block.
	:type raw_speed: <list> of <float>
	:type timestamps: <list> of <float>
	:type margin: <float>
	:return: List of corresponding raw speed values.
	:rtype: <dict> of <float>:<list> of <float>

	:Example:

	>>> from v2 import *
	>>> blocks = speed_blocks([15.625, 125, 1, 1000, 1000])
	>>> print(blocks)
	{0: [15.625], 1: [125], 2: [1], 3: [1000, 1000]}
	>>> timestamped_blocks = speed_blocks([15.625, 125, 1, 1000, 1000], timestamps=[3280, 3480, 3580, 4080, 4130, 4180])
	>>> print(timestamped_blocks)
	{3280: [15.625], 3480: [125], 3580: [1], 4080: [1000, 1000]}
	>>>

	.. note:: You probably shoudn't use another margin.
	.. warning:: If entered, timestamps must be as long + 1 or at least as long as raw_speed !
	.. seealso:: raw_speed(), speed_weighting(), speed(), global_speed()
	"""
	if not timestamps: # timestamps define keys, so by default keys will be 0, 1, 2... etc
		timestamps = range(len(raw_speed))

	t, b = 0, timestamps[0]
	blocks = {b: [raw_speed[0]]} # The first block should always contain the first value

	for i in range(1, len(raw_speed)):
		t += 1
		if abs(raw_speed[i] - raw_speed[i - 1]) <= raw_speed[i - 1] * margin: # Checking if next value is in the margin
			blocks[b].append(raw_speed[i])
		else: # Skip to next block
			b = timestamps[t]
			blocks[b] = [raw_speed[i]]

	return blocks
def speed_weighting(speed_blocks: dict) -> dict:
	"""
	This function takes speed blocks and weight them to turn their list values into unique values.
	"Speed" is a system by Fukiyel which tries to make concrete values of a map's clicking-speed difficulty.
	Speed weigthing is a part of the speed difficulty calculation, such as Speed blocks and others.
	The weighting depends mainly on the length of the blocks.

	:param speed_blocks: Dict of list of raw speed values, grouped by similarity.
	:type speed_blocks: <dict> of <float>:<list> of <float>
	:return: The same dict but the values became one weighted value by key.
	:rtype: <dict> of <float>:<float>

	:Example:

	>>> from v2 import *
	>>> weighted_blocks = speed_weighting({3280: [15.625], 3480: [125], 3580: [1], 4080: [1000, 1000]})
	>>> print(weighted_blocks)
	{3280: 0.05756624842868733, 3480: 0.46052998742949863, 3580: 0.003684239899435989, 4080: 5.486298899450404}
	>>>

	.. seealso:: raw_speed(), speed_blocks(), speed(), global_speed()
	"""
	weighted_blocks = {}

	for b in speed_blocks:
		weighted_blocks[b] = mean(speed_blocks[b]) / (exp(-.4 * len(speed_blocks[b]) + 6) + 1) # To know more, search for "sigmoïd functions"

	return 	weighted_blocks
def speed(active_timestamps: list) -> dict:
	"""
	This function takes timestamps bewteen active objects of an osu! map, and returns a dict of some of these timestamps and their corresponding speed values.
	"Speed" is a system by Fukiyel which tries to make concrete values of a map's clicking-speed difficulty.
	This function is a shortcut for many specifical speed functions, to get directly to the almost final result.
	To resume algorithm, the more objects are close in timing and the more they consecutively are, the more speed values will be high.

	:param active_timestamps: Timestamps of active map's objects
	:type active_timestamps: <list> of <float>
	:return: Dict of some active timestamps and their corresponding speed values
	:rtype: <dict> of <float>:<list> of <float>

	:Example:

	>>> from v2 import *
	>>> speed = speed([1188, 1256, 1324, 1392, 1410, 1440])
	>>> print(speed)
	{1188: 3.2449667786516225, 1392: 78.96604722728028, 1410: 17.056666201092543}
	>>>

	.. note:: Only a fraction of timestamps become keys.
	.. warning:: Only active timestamps should be used, make sure spinners aren't took in account.
	.. seealso:: raw_speed(), speed_blocks(), speed_weighting() global_speed()
	"""
	return speed_weighting(speed_blocks(raw_speed(periods(active_timestamps)), timestamps=active_timestamps))
def global_speed(speed: dict) -> float:
	"""
	This function takes speed difficulty values of an osu! map, and returns a global value.
	This global value summarize the speed difficulty of all of the map in one floating number.

	:param speed: Dict of key timestamps and their speed difficulty values of an osu! map.
	:type speed: <dict> of <float>:<list> of <float>
	:return: Global unique value for the map's speed difficulty.
	:rtype: <float>

	:Example:

	>>> from v2 import *
	>>> global_speed = global_speed({1188: 3.2449667786516225, 1392: 78.96604722728028, 1410: 17.056666201092543})
	>>> print(global_speed)
	118.44907084092043
	>>>

	.. seealso:: raw_speed(), speed_blocks(), speed_weighting(), speed()
	"""
	values = list(speed.values())
	end_data = sorted(values)[round(.9 * len(values) - 1):]

	return max(values) + median(end_data) / 2

# Stamina*
def absolute_stamina(active_periods: list) -> list:
	"""
	This function takes active periods of an osu! map, and returns a list of corresponding absolute stamina values.
	"Stamina" is a system by Fukiyel which tries to make concrete values of a map's clicking-stamina difficulty.
	Absolute stamina is a part of Stamina calculation. It tells how stamina is supposed to vary at each object.
	The more the period is short, the more the variation will approach +15.

	:param active_periods: Periods between a map's active timestamps.
	:type active_periods: <list> of <float>
	:return: List of absolute stamina values.
	:rtype: <list> of <float>

	:Example:

	>>> from v2 import *
	>>> absolute_values = absolute_stamina([200, 100, 500, 50, 50])
	>>> print(absolute_values)
	[-6.2132034355964265, 0.0, -18.541019662496844, 4.393398282201787, 4.393398282201787]
	>>>

	.. note:: Formula changes if the period is shorter/longer than 500 milliseconds.
	.. warning:: Only active periods should be used, make sure spinners aren't took in account.
	.. seealso:: relative_stamina(), stamina(), global_stamina()
	"""
	absolute_stamina = []

	for i in range(len(active_periods)):
		if active_periods[i] <= 500:
			absolute_stamina.append(15 - (2.25 * active_periods[i]) ** .5)
		else:
			absolute_stamina.append(15 - (2.25 * active_periods[i]) ** .5 - (active_periods[i] - 500) ** 2 / 1e5)

	return absolute_stamina
def relative_stamina(active_periods: list, timestamps=None) -> dict:
	"""
	This function takes active periods of an osu! map, and eventually the timestamps of each period's beginning.
	It returns a dict of these timestamps (or values' ordinals by default) and their relative stamina values.
	"Stamina" is a system by Fukiyel which tries to make concrete values of a map's clicking-stamina difficulty.
	Each value depends of the previous one. The more the period is short the more it will augment.

	:param active_periods: Periods bewteen a map's active objects
	:param timestamps: Timestamps corresponding to the beginning of each period
	:type active_periods: <list> of <float>
	:type timestamps: <list> of <float>
	:return: List of stamina values depending on periods
	:rtype: <dict> of <float>:<float>

	:Example:

	>>> from v2 import *
	>>> stamina = relative_stamina([200, 100, 500, 50, 50])
	>>> print(stamina)
	{0: 0, 1: 0, 2: 0, 3: 4.393398282201787, 4: 8.786796564403573}
	>>> timestamped_stamina = relative_stamina([200, 100, 500, 50, 50])
	>>> print(relative_stamina([200, 100, 500, 50, 50], timestamps=[3280, 3480, 3580, 4080, 4130, 4180]))
	{3280: 0, 3480: 0, 3580: 0, 4080: 4.393398282201787, 4130: 8.786796564403573}
	>>>

	.. note:: To stamina to stagnate, periods must be 100 ms long (10 notes / second).
	.. warning:: Only active periods should be used, make sure spinners aren't took in account.
	.. warning:: If entered, timestamps must be as long + 1 or at least as long as active_periods !
	.. seealso:: absolute_stamina(), stamina(), global_stamina()
	"""
	if not timestamps: # timestamps define keys, so by default keys will be 0, 1, 2... etc
		timestamps = range(len(active_periods))

	values = [0] + active_periods
	variation = absolute_stamina(active_periods)
	relative_stamina = {timestamps[0]: 0} # First value is set to 0

	for i in range(1, len(values)):
		if values[i - 1] + variation[i - 1] > 0:
			values[i] = values[i - 1] + variation[i - 1]
		else:
			values[i] = 0
		relative_stamina[timestamps[i - 1]] = values[i]

	return relative_stamina
def stamina(active_timestamps: list) -> dict:
	"""
	This function takes active timestamps of an osu! map, and returns a dict of them and their corresponding stamina values.
	"Stamina" is a system by Fukiyel which tries to make concrete values of a map's clicking-stamina difficulty.
	Each value depends of the previous one. The more the period is short the more it will augment.
	This function allows to skip the use of relative_stamina(), absolute_stamina(), and periods().

	:param active_timestamps: Timestamps of a map's active objects.
	:type active_timestamps: <list> of <float>
	:return: List of corresponding stamina values.
	:rtype: <dict> of <float>:<float>

	:Example:

	>>> from v2 import *
	>>> stamina = stamina([3280, 3480, 3580, 4080, 4130, 4180])
	>>> print(stamina)
	{3280: 0, 3480: 0, 3580: 0, 4080: 4.393398282201787, 4130: 8.786796564403573}
	>>>

	.. note:: To stamina to stagnate, periods must be 100 ms long (10 notes / second).
	.. warning:: Only active periods should be used, make sure spinners aren't took in account.
	.. seealso:: absolute_stamina(), relative_stamina(), global_stamina()
	"""
	return relative_stamina(periods(active_timestamps), timestamps=active_timestamps)
def global_stamina(stamina: dict) -> float:
	"""
	This function takes a dict whose values are stamina difficulty values, and returns a global one.
	That global value summarize the stamina difficulty of all of the map in one floating number.

	:param stamina: Dict with stamina difficulty values of an osu! map as values.
	:type stamina: <dict> of <float>:<float>
	:return: Global unique value for the map's stamina difficulty.
	:rtype: <float>

	:Example:

	>>> from v2 import *
	>>> global_stamina = global_stamina({3280: 0, 3480: 0, 3580: 0, 4080: 4.393398282201787, 4130: 8.786796564403573})
	>>> print(global_stamina)
	10.104816049064109
	>>>

	.. seealso:: absolute_stamina(), relative_stamina(), stamina()
	"""
	values = list(stamina.values())
	return max(values) + mean(values) / 2
