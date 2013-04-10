# A quick script to show the different avatars for the classroom study
# to make sure they look different enough, press r to flip the view

import viz
import vizact

viz.setMultiSample(4)
viz.fov(60)
viz.go()

male_avatars = []
male_avatars.append(viz.addAvatar('male1.cfg'))
male_avatars.append(viz.addAvatar('male2.cfg'))
male_avatars.append(viz.addAvatar('male3.cfg'))
male_avatars.append(viz.addAvatar('male4.cfg'))
male_avatars.append(viz.addAvatar('male5.cfg'))
male_avatars.append(viz.addAvatar('male6.cfg'))
male_avatars.append(viz.addAvatar('male7.cfg'))
male_avatars.append(viz.addAvatar('male8.cfg'))
male_avatars.append(viz.addAvatar('male9.cfg'))
male_avatars.append(viz.addAvatar('male10.cfg'))
male_avatars.append(viz.addAvatar('male11.cfg'))
male_avatars.append(viz.addAvatar('male12.cfg'))
male_avatars.append(viz.addAvatar('male13.cfg'))
male_avatars.append(viz.addAvatar('male14.cfg'))
male_avatars.append(viz.addAvatar('male15.cfg'))
male_avatars.append(viz.addAvatar('male16.cfg'))
male_avatars.append(viz.addAvatar('male17.cfg'))
male_avatars.append(viz.addAvatar('male18.cfg'))
male_avatars.append(viz.addAvatar('male19.cfg'))
male_avatars.append(viz.addAvatar('male20.cfg'))

female_avatars = []
#female_avatars.append(viz.addAvatar('female1.cfg'))
#female_avatars.append(viz.addAvatar('female2.cfg'))
#female_avatars.append(viz.addAvatar('female3.cfg'))
#female_avatars.append(viz.addAvatar('female4.cfg'))
#female_avatars.append(viz.addAvatar('female5.cfg'))
#female_avatars.append(viz.addAvatar('female6.cfg'))
#female_avatars.append(viz.addAvatar('female7.cfg'))
#female_avatars.append(viz.addAvatar('female8.cfg'))
#female_avatars.append(viz.addAvatar('female9.cfg'))
#female_avatars.append(viz.addAvatar('female10.cfg'))
#female_avatars.append(viz.addAvatar('female11.cfg'))
#female_avatars.append(viz.addAvatar('female12.cfg'))
#female_avatars.append(viz.addAvatar('female13.cfg'))
#female_avatars.append(viz.addAvatar('female14.cfg'))
#female_avatars.append(viz.addAvatar('female15.cfg'))
#female_avatars.append(viz.addAvatar('female16.cfg'))
#female_avatars.append(viz.addAvatar('female17.cfg'))
#female_avatars.append(viz.addAvatar('female18.cfg'))
#female_avatars.append(viz.addAvatar('female19.cfg'))
#female_avatars.append(viz.addAvatar('female20.cfg'))

# display male avatars
num_avatars = len(male_avatars)
x = -.5 * num_avatars
z = 3 + num_avatars * .5

for avatar in male_avatars:
	avatar.setPosition([x, 0, z]);
	avatar.setEuler(-180,0,0)
	avatar.state(1)
	x += 1

# display female avatars
num_avatars = len(female_avatars)
x = .5 * num_avatars
z = -3 + num_avatars * -.5
for avatar in female_avatars:
	avatar.setPosition([x, 0, z]);
	avatar.state(1)
	x -= 1

# The below code allows you to set the reverse the mainview. In order to do
# so, I create a wrapper around the euler value, euler_t. Using the array
# wrapper, the function can edit the array and maintain the value, whereas
# integers are mutable and the change wouldn't persist.
euler_t = [0]
def flip_view(euler_t):
	euler = euler_t[0]
	if (euler == 0):
		euler = 180
	else:
		euler = 0
	viz.MainView.setEuler([euler,0,0])
	euler_t[0] = euler
vizact.onkeydown('r', flip_view, euler_t)
