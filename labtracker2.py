###############################
# Tracker for use in PPT2!    #
# Oliver Castaneda 2011       #
###############################
#
#Set the DEFAULT_OFFSET, DEFAULT_EULER, and DEFAULT_SCALE to match
#your world if the origin of your world does not
#correspond to the PPT tracking system origin.
#
# Using the tracking system:
#	from labTracker import *
#   Tracking = labTracker()
# 	Tracking.setPosition(myCurrentPosition)
#
##################################################

import nvis
import viz
import vizact

DEFAULT_OFFSET = [0,0,0]
DEFAULT_EULER = [0,0,0]
DEFAULT_SCALE = [1.5,1,1.5]
PPT_HOSTNAME = '171.64.32.54'

class labTracker(object):
	def __init__(self):
		viz.mouse.setVisible(viz.OFF)
		#Activate NVIS HMD
		#nvis.nvisorSX111()
		nvis.nvisorSX60()
		viz.cursor(viz.OFF)
		isense = viz.add('intersense.dle')
		headTracker = isense.addTracker(port=1)
		vizact.onkeydown('r',headTracker.resetHeading)
		vrpn = viz.add('vrpn7.dle')
		view = viz.MainView
		
		self.markers = []
		
		headMarker = vrpn.addTracker('PPT0@' + PPT_HOSTNAME, 0)
		headMarker.setScale(DEFAULT_SCALE)
		self.markers.append(headMarker)
		self.markers.append( vrpn.addTracker('PPT0@' + PPT_HOSTNAME, 1) )
		self.markers.append( vrpn.addTracker('PPT0@' + PPT_HOSTNAME, 2) )
		
		filter = viz.add("filter.dle")
		headMarker_filter = filter.average(headMarker, samples = 7)
		headPPT = viz.mergeLinkable(headMarker_filter,headTracker)
		headPos = viz.link(headPPT, view, priority = 0)
		headPos.setOffset(DEFAULT_OFFSET)
		headPos.setScale(DEFAULT_SCALE)
		self.posLink = headPos
		self.headMarker = headMarker
		
	#get position in world (absolute) coordinates of 0 marker (head marker)
	def getPosition(self):
		trk = self.headMarker.getPosition()
		off = self.posLink.getOffset()
		return [trk[0]+off[0], trk[1]+off[1], trk[2]+off[2]]
	#get position of any marker 1,2,3...
	def getMarkerPosition(self, markerID):
		trk = self.markers[markerID-1].getPosition()
		off = self.posLink.getOffset()
		return [trk[0]+off[0], trk[1]+off[1], trk[2]+off[2]]
		
	#set absolute location
	def setPosition(self, pos):
		trk = self.headMarker.getPosition()
		self.posLink.setOffset([pos[0]-trk[0], pos[1]-trk[1], pos[2]-trk[2]])
	#set the ground height to absolute y
	def setGround(self, y):
		off = self.posLink.getOffset()
		off[1] = y
		self.posLink.setOffset(off)
	def getGround(self):
		off = self.posLink.getOffset()
		return off[1]
	def reset(self):
		self.posLink.setOffset(DEFAULT_OFFSET)	
		
