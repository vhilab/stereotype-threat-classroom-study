import viz, vizinput, viztask, time, vizact, random, math
from time import clock

############################ editable global variables
NUM_AVATARS = 18 # set to 18 for female only (cond 5.) for high framerates
				 # set to 18 for mixed (cond 3.) for high framerates
				 # set to 18 for male only (cond. 1) for high framerates
ROOM = "PPT2" # set to "PPT1" or "PPT2" -> this affects the tracking module used
AMBISONIC = False # set to True if running in PPT1
DATA = True # set to True if running (IMPORTANT)
FADE_RATE = 1 # set to 1 if running; TODO: take it out entirely when room is finalized
DATA_PRIORITY = 1 # this sets the priority of the data output -- make this variable higher if you notice any freezes

############################ global variables
AA = 4
ROOM_SCALE = [1.56, 1.56, 1.56]
# SEAT_POS describes where an avatar should be set to be seated, starting at seat index 0;
# NOTE: SEAT_POS describes the seat number which will not correspond to the avatar number if you
# have empty seats
SEAT_POS = ([-2.5, .329, 2.6], [-2.5, .329, 1.7], [-2.5, .329, 1], [-2.5, .329, .3],
			[-2.5, .329, -.5], [-2.5, .329, -1.3], [-2.5, .329, -2.05], [-2.5, .329, -2.8],
			[-1.5, .329, -3.7], [0.0, .329, -3.7], [0.8, .329, -3.7], [1.6, .329, -3.7],
			[2.5, .329, -2.8], [2.5, .329, -2.05], [2.5, .329, -1.3], [2.5, .329, -.5],
			[2.5, .329, .3], [2.5, .329, 1], [2.5, .329, 1.7], [2.5, .329, 2.6])
AVATAR_STATE = (3,4,13,15,11,12,13,14,3,12,4,8,17,9,14,11,8,4,17,10)
FADE_IN_AVATARS = (11,4,2,14,17,7) # index into avatars array to fade in avatars
FADE_IN_DELAY = (24,17,6,12,14,15)
FADE_OUT_AVATARS = (14,5,6,10,2,17,13,7,8,15,11,12,4,3,1,0,9,16) # indexes to fade out
FADE_OUT_DELAY = (20,9,3,3,5,10,5,5,7,8,4,7,10,2,4,1,1,6)
TRANSITION_SETS = ((6, 13, 11, 7, 0), (9, 2, 14, 10), (8, 4, 15), (16, 3), (12, 5), (1, 17))
TEACHER_POS = [-2.650106191635132, .6, 5.995359420776367]
TEACHER_STATE = (1,2,3,6,7,3,6,1) # animation numbers to circulate through for the teacher
STARTING_POS = [-0.75, 1.5, -4.0] # starting position for MainView
AUDIO_FILE = "resources/lectureaudio%d.wav"
NUM_AUDIO_FILES = 13
DURATIONS = (56.1922903, 44.2107937, 46.8114286, 53.5916554, 54.4275737, 56.0994105, 55.1706123, 57.9570069, 44.582313, 54.6133334, 54.1489343, 57.2139683, 4.4162812)
CLASSROOM_FILE = "resources/classroom.dae"
MALE_AVATAR_FILE = "avatars/male%d.cfg"
FEMALE_AVATAR_FILE = "avatars/female%d.cfg"
TEACHER_AVATAR_FILE = "avatars/teacher.cfg"
HEAD_MOTIONS_FILE = "head_motions/headEulerTest%d.txt"
HEAD_BEG_MOTIONS_FILE = "head_motions/headBegEulerTest%d.txt"
NOD_FILE = "head_motions/headNod.txt"
SLIDES_FILE = "resources/Slide%d.JPG"
TEACHER_TIMINGS_FILE = "resources/teacher_timings.txt"
SLIDES_TIMINGS_FILE = "resources/michelle_input.txt"
RECORD_TIMINGS = False
NUM_SLIDES = 136
NUM_CONDITIONS = 5
NUM_SEATS = 20
H_BEG = 0; H_TRANS = 1; H_LEC = 2 # sets what head animation to use
M = 0; F = 1; EMPTY = 2 # denotes seating for conditions
CONDITIONS = (  (M, M, M, M, M, EMPTY, M, M, M, M, M, M, M, EMPTY, M, M, M, M, M, M),
				(M, M, M, M, F, EMPTY, M, M, M, M, F, M, M, EMPTY, F, M, M, M, M, F),
				(M, F, M, M, F, EMPTY, F, M, F, M, F, M, M, EMPTY, F, M, F, M, F, F),
				(F, F, F, F, M, EMPTY, F, F, F, F, M, F, F, EMPTY, M, F, F, F, F, M),
				(F, F, F, F, F, EMPTY, F, F, F, F, F, F, F, EMPTY, F, F, F, F, F, F) )
CONDITION_PROMPT = "What condition would you like to use?\n1 (Default) = 0% female\n\
2 = 22.2% female\n3 = 50% female\n4 = 77.78% female\n5 = 100% female"

############################ Condition setup
condition = int(vizinput.choose(CONDITION_PROMPT, [str(i + 1) for i in range(NUM_CONDITIONS)]))
seating = CONDITIONS[condition]
if RECORD_TIMINGS:
	SLIDES_TIMINGS_FILE = viz.input("Enter a timing file name")
	SLIDES_TIMINGS_FILE += ".txt"
else:
	with open(SLIDES_TIMINGS_FILE) as f:
		str_array = f.read().split()
		slide_timings = (float(i) for i in str_array)

with open(TEACHER_TIMINGS_FILE) as f:
	str_array = f.read().split()
	teacher_timings = (float(i) for i in str_array)

SUBJECT_PROMPT = "Please enter the subject's name or number:"
subject_id = vizinput.input(SUBJECT_PROMPT)

############################ vizard and lab setup
def configureSound():
	#Good adjustment for reverb and room
	vizsonic.setReverb(6.0, 0.2, 0.5, 0.9, 0)
	#Define virtual roomsize
	vizsonic.setSimulatedRoomRadius(5,3)
	#Turn shaker on
	vizsonic.setShaker(1.0)
	#Make speakers stationary
	viz.setOption('sound3d.useViewRotation', 0)
	#Turn on/off sound debugging
	viz.setDebugSound3D(False)
if AMBISONIC:
	import vizsonic
	configureSound()

viz.vsync(viz.ON)
viz.setOption('viz.antialias', str(AA))
viz.go(viz.PROMPT)
tracking = viz.get(viz.TRACKER)
Tracking = None
if (tracking):
	if ROOM == "PPT1":
		from labTracker import *
		startPosition = [0, .25, -3.7]
		Tracking = labTracker()
		Tracking.setPosition(startPosition)
	else:
		from labtracker2 import *
		startPosition = [0, .25, -3.7]
		Tracking = labTracker()
		Tracking.setPosition(startPosition)

############################ maintain state
# this class will maintain state. this technique is used to replace the use
# of the global keyword when changing variables across functions
class ClassroomState:
	teacher_state_index = 0
	gesture = 4
	gesture_on = False
	lecture_finished = False

############################ preload actions
state = ClassroomState()
room = viz.addChild(CLASSROOM_FILE)
room.emissive([1,1,1])
room.setScale(ROOM_SCALE)

teacher = viz.add(TEACHER_AVATAR_FILE)
teacher.setPosition(TEACHER_POS)
teacher.setEuler(170,0,0)
teacher.state(2)
teacher.emissive([1,1,1])
teacher.setScale(1.25,1.25,1.25)
viz.MainView.getHeadLight().disable()

beg_euler = []
for i in range(NUM_AVATARS):
	data = []
	try :
		file_handle = open(HEAD_BEG_MOTIONS_FILE % (i+1))
	except IOError:
		continue
	for line in file_handle:
		line = line.replace('[','').replace(']','')
		line = line.split(',')
		floatArr = []
		if i < 8:
			floatArr.append(float(line[0]) - 70)
		elif i > 11:
			floatArr.append(float(line[0]) + 70)
		else:
			floatArr.append(-float(line[0]))
		floatArr.append(float(line[1]))
		floatArr.append(float(line[2]))
		data.append(floatArr)
	file_handle.close()
	beg_euler.append(data)

euler = []
for i in range(NUM_AVATARS):
	data = []
	try :
		file_handle = open(HEAD_MOTIONS_FILE % (i+1))
	except IOError:
		continue
	for line in file_handle:
		line = line.replace('[','').replace(']','')
		line = line.split(',')
		floatArr = []
		if i < 8 or i > 11:
			floatArr.append(-.6*float(line[0]))
		else:
			floatArr.append(-float(line[0]))
		floatArr.append(float(line[1]))
		floatArr.append(float(line[2]))
		data.append(floatArr)
	file_handle.close()
	euler.append(data)
	# print len(data)

# avatars_i is incremented for each avatar added. some global variables are set up for seats and some
# are set up for the avatar. This is due to a last minute change from 20 avatars, i.e., in sync with the
# number of seats, to 18 avatars, i.e., out of sync with the number of seats. Some seats do not
# contain avatars
avatars_i = 0
avatars = []
heads = []
heads_state = [] # uses H_BEG, H_TRANS, H_LEC to alter the head appropriately
# the below variables provide some offset in the animations based on running
# the simulation and viewing which avatars motions look similar
primaryConflicts = [8,10,13,15,16,18]
secondaryConflicts = [1,8,4,19,6]
for seat_i in range(NUM_SEATS):
	if avatars_i >= NUM_AVATARS: break
	if seating[seat_i] is not EMPTY:
		new_avatar = viz.addAvatar((MALE_AVATAR_FILE if seating[seat_i] == M else FEMALE_AVATAR_FILE) % (avatars_i+1))
		avatars.append(new_avatar)
		heads_state.append(H_BEG)
		new_avatar.setPosition(SEAT_POS[seat_i])
		new_avatar.setEuler(90,0,0)
		if avatars_i in FADE_IN_AVATARS: new_avatar.visible(viz.OFF)
		if seat_i > 7:
			new_avatar.setEuler(0,0,0)
		if seat_i > 11:
			new_avatar.setEuler(-90,0,0)
		if i not in primaryConflicts and i not in secondaryConflicts:
			new_avatar.execute(1, freeze=True)
			new_avatar.setAnimationSpeed(1,1000)
		else:
			new_avatar.execute(1, freeze=True)
			new_avatar.setAnimationSpeed(1,1000)
		new_avatar.emissive([1,1,1])
		new_avatar_head = new_avatar.getBone('Bip01 Head')
		heads.append(new_avatar_head)
		new_avatar_head.lock()
		avatars_i += 1

background_screen = viz.addTexQuad()
background_screen.setScale(2.65, 2.65)
background_screen.setPosition([2.13, 2.47, 6.75])
scaled_slides = [viz.addTexture(SLIDES_FILE % (slideNum + 1)) for slideNum in range(NUM_SLIDES)]
screen = viz.addTexQuad()
screen.setScale(2.6, 1.95)
screen.setPosition([2.13, 2.47, 6.74])
currSlide = scaled_slides.pop(0)
screen.texture(currSlide)
scaled_slides.append(currSlide) # for looping

def getSound(soundfile, object):
	'''a wrapper to setup the soundobject to play a sound.
	the returned object should be sent back to playSound.\
	this function returns a sound object.'''
	sound = object.playsound(soundfile)
	sound.stop()
	return sound

lecture_sounds = []
for audioNum in range(NUM_AUDIO_FILES):
	soundfile = AUDIO_FILE % (audioNum + 1)
	lecture_sounds.append(getSound(soundfile, teacher))
	
nodEuler = [] # an array of euler coordinates for the nodding head motion, see nodAvatar()
try :
	file_handle = open(NOD_FILE)
	for line in file_handle:
		line = line.replace('[','').replace(']','')
		line = line.split(',')
		floatArr = []
		if i < 8 or i > 11:
			floatArr.append(-.6*float(line[0]))
		else:
			floatArr.append(-float(line[0]))
		floatArr.append(float(line[1]))
		floatArr.append(float(line[2]))
		nodEuler.append(floatArr)
	file_handle.close()
except IOError:
	pass


############################ runtime actions
times = [0 for i in range(len(euler))]
def faceView():
	for i in range(len(avatars)):
		if (heads_state[i] != H_TRANS):
			if (heads_state[i] == H_BEG):
				heads_array = beg_euler
			else:
				heads_array = euler
			if times[i] < len(heads_array[i]):
				heads[i].setEuler((heads_array[i])[times[i]], viz.AVATAR_LOCAL)
				times[i] += 1
			else:
				times[i] = 0
		else:
			times[i] = 0
			heads[i].setEuler(heads[i].getEuler()) # must be absolute because getEuler returns absolute coordinates

def teacherGesture():
	if not state.lecture_finished:
		state.gesture_on = True
		if state.gesture is 4:
			state.gesture = 5
		else:
			state.gesture = 4
		teacher.state(state.gesture)
		yield viztask.waitTime(10)
		teacher.state(1)
		state.gesture_on = False

def recordTime():
	timeDiff = clock()
	with open(SLIDES_TIMINGS_FILE, "a") as timeFile:
		timeFile.write(str(timeDiff) + '\n')


def advanceSlide():
	'''advances a slide'''
	currSlide = scaled_slides.pop(0)
	screen.texture(currSlide)
	scaled_slides.append(currSlide) # for looping
	if RECORD_TIMINGS:
		recordTime()

def playLecture():
	for timing in teacher_timings:
		vizact.ontimer2(timing, 0, viztask.schedule, teacherGesture())
	if RECORD_TIMINGS:
		clock()
	else:
		for timing in slide_timings:
			vizact.ontimer2(timing, 0, advanceSlide)
	teacher.state(1)
	count = 0 # used to access the DURATIONS list
	for lecture_sound in lecture_sounds:
		lecture_sound.play()
		yield viztask.waitTime(DURATIONS[count])
		lecture_sound.stop()
		count += 1
	print "lecture finished"
	state.lecture_finished = True
	teacher.state(2)
	fadeOut = vizact.fadeTo(0, time=1)
	for i in range(len(FADE_OUT_AVATARS)):
		if FADE_OUT_AVATARS[i] < len(avatars):
			yield viztask.waitTime(FADE_OUT_DELAY[i]/FADE_RATE)
			avatars[FADE_OUT_AVATARS[i]].addAction(fadeOut)
	outputData.write('\nFinished Fading Out Avatars\n')
	outputData.write('-------------------------------------------------\n')
	print "study finished"

def popInAvatars():
	print 'fading in'
	for i in range(len(FADE_IN_AVATARS)):
		if FADE_IN_AVATARS[i] < len(avatars):
			yield viztask.waitTime(FADE_IN_DELAY[i]/FADE_RATE)
			avatars[FADE_IN_AVATARS[i]].visible(viz.ON)
	outputData.write('\nFinished Loading Avatars\n')
	outputData.write('-------------------------------------------------\n')

def transitionAvatars():
	print 'transitioning'
	yield viztask.waitTime(1)
	for a_set in TRANSITION_SETS:
		maxAngularDifference = 0 # used to set the waiting time for each transition set, or a_set
		for i in a_set:
			if i < len(avatars):
				heads_state[i] = H_TRANS
				angle = euler[i][0]
				look = vizact.boneSpinTo('Bip01 Head',mode=viz.AVATAR_LOCAL,euler=angle,speed=60)
				avatars[i].runAction(look)
				angularDifference = getAngularDifference(heads[i].getEuler(viz.AVATAR_LOCAL), angle)
				if (angularDifference > maxAngularDifference): maxAngularDifference = angularDifference
		yield viztask.waitTime(maxAngularDifference/60) # the maxAngularDifference sets the time we wait here
		for i in a_set:
			if i < len(avatars):
				heads_state[i] = H_LEC
	outputData.write('\nFinished Transitioning Avatars to Lecture State\n')
	outputData.write('-------------------------------------------------\n')


##### Data Output Setup
outputData = open('output_data/' + subject_id + '_orientation_data.txt', 'a')
outputData.write('Orientation Data for Subject ' + subject_id + '\n')
outputData.write('-------------------------------------------------\n')

def getData():
	head_euler = str(viz.MainView.getEuler())
	head_pos = str(Tracking.getPosition())
	left_hand_pos = str(Tracking.getMarkerPosition(2))
	right_hand_pos = str(Tracking.getMarkerPosition(3))
	outputData.write(head_euler + ',' + head_pos + ',' \
			+ left_hand_pos + ',' + right_hand_pos + '\n')

if DATA:
	vizact.onupdate(DATA_PRIORITY, getData)

def writeTransition(string):
	outputData.write(string)

##### Run Script Logic
def control():
	yield viztask.waitKeyDown(' ')
	viztask.schedule(popInAvatars())
	yield viztask.waitKeyDown(' ')
	viztask.schedule(transitionAvatars())
	viztask.schedule(playLecture())

vizact.onupdate(0, faceView)

viztask.schedule(control())

### This section sets up the code to force an avatar to nod. It is based off the same code as
# transitionAvatars() with modifications to force a custom nod animation that fits into the running scene cleanly.
def nodAvatar(avatarNum):
	avatarNum -= 1
	if (avatarNum < len(avatars)):
		heads_state[avatarNum] = H_TRANS
		angle = nodEuler[0]
		look = vizact.boneSpinTo('Bip01 Head',mode=viz.AVATAR_LOCAL,euler=angle,speed=100)
		angularDifference = getAngularDifference(heads[avatarNum].getEuler(viz.AVATAR_LOCAL), angle)
		avatars[avatarNum].runAction(look)
		yield viztask.waitTime(angularDifference/100)
		for angle in nodEuler:
			heads[avatarNum].setEuler(angle, viz.AVATAR_LOCAL)
			yield viztask.waitTime(.008) # sets speed of head nod; make lower to speed up head nod
		angle = euler[avatarNum][0]
		look = vizact.boneSpinTo('Bip01 Head',mode=viz.AVATAR_LOCAL,euler=angle,speed=100)
		angularDifference = getAngularDifference(heads[avatarNum].getEuler(viz.AVATAR_LOCAL), angle)
		avatars[avatarNum].runAction(look)
		yield viztask.waitTime(angularDifference/100)
		heads_state[avatarNum] = H_LEC

# uses law of cosines to get the angluar difference between two angles in an x,y,z coordinate system
# usage: figuring out how long to wait given that the avatars can start an animation when their heads
# are at different eulers, see nodAvatar():
def getAngularDifference(angle1, angle2):
	a = math.sqrt(math.pow(angle1[0],2) + math.pow(angle1[1],2) + math.pow(angle1[2],2))
	b = math.sqrt(math.pow(angle2[0],2) + math.pow(angle2[1],2) + math.pow(angle2[2],2))
	c = math.sqrt(math.pow(angle1[0]-angle2[0],2) + math.pow(angle1[1]-angle2[1],2) + math.pow(angle1[2]-angle2[2],2))
	angle = math.degrees(math.acos((math.pow(a,2) + math.pow(b,2) - math.pow(c,2))/(2*a*b)))
	return angle


def registerCallback1(): yield viztask.waitKeyDown('1'); viztask.schedule(nodAvatar(1))
def registerCallback2(): yield viztask.waitKeyDown('2'); viztask.schedule(nodAvatar(2))
def registerCallback3(): yield viztask.waitKeyDown('3'); viztask.schedule(nodAvatar(3))
def registerCallback4(): yield viztask.waitKeyDown('4'); viztask.schedule(nodAvatar(4))
def registerCallback5(): yield viztask.waitKeyDown('5'); viztask.schedule(nodAvatar(5))
def registerCallback6(): yield viztask.waitKeyDown('6'); viztask.schedule(nodAvatar(6))
def registerCallback7(): yield viztask.waitKeyDown('7'); viztask.schedule(nodAvatar(7))
def registerCallback8(): yield viztask.waitKeyDown('8'); viztask.schedule(nodAvatar(8))
def registerCallback9(): yield viztask.waitKeyDown('9'); viztask.schedule(nodAvatar(9))
def registerCallback10(): yield viztask.waitKeyDown('q'); viztask.schedule(nodAvatar(10))
def registerCallback11(): yield viztask.waitKeyDown('w'); viztask.schedule(nodAvatar(11))
def registerCallback12(): yield viztask.waitKeyDown('e'); viztask.schedule(nodAvatar(12))
def registerCallback13(): yield viztask.waitKeyDown('r'); viztask.schedule(nodAvatar(13))
def registerCallback14(): yield viztask.waitKeyDown('t'); viztask.schedule(nodAvatar(14))
def registerCallback15(): yield viztask.waitKeyDown('y'); viztask.schedule(nodAvatar(15))
def registerCallback16(): yield viztask.waitKeyDown('u'); viztask.schedule(nodAvatar(16))
def registerCallback17(): yield viztask.waitKeyDown('i'); viztask.schedule(nodAvatar(17))
def registerCallback18(): yield viztask.waitKeyDown('o'); viztask.schedule(nodAvatar(18))

for i in range(1, len(avatars) + 1): viztask.schedule(eval("registerCallback" + str(i)))
