# Spinning head test file #

import viz, vizact, viztask

viz.setMultiSample(4)
viz.go()
viz.MainWindow.fov(60)

piazza = viz.addChild('piazza.osgb')

male = viz.addAvatar('vcc_male.cfg')
male.setPosition([0, 0, 2])
male.setEuler([-180,0,0])

head = male.getBone('Bip01 Head')
head.lock() # boneSpinTo works whether or not the bone is locked

lookLeft = vizact.boneSpinTo('Bip01 Head',mode=viz.AVATAR_LOCAL,euler=(-90,0,0),speed=60,interpolate=vizact.easeInOut)
lookRight = vizact.boneSpinTo('Bip01 Head',mode=viz.AVATAR_LOCAL,euler=(90,0,0),speed=60,interpolate=vizact.easeInOut)

def lookAround():
	global male
	while True:
		male.runAction(lookLeft)
		print "looking left"
		#yield viztask.waitTime(2)
		male.runAction(lookRight)
		print "looking right"
		#yield viztask.waitTime(2)

viztask.schedule(lookAround)
