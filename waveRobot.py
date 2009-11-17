from waveapi import events
from waveapi import model
from waveapi import robot
 
def OnParticipantsChanged(properties, context):
  added = properties['participantsAdded']
  for participant in added:
    Greet(context, participant)
 
def OnRobotAdded(properties, context):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText('Hi, everybody!')
 
def OnBlipCreated(properties, context):
  blip = context.GetBlipById(properties['blipId'])
  blip.GetDocument().AppendText(':-)')
 
def Greet(context, participant):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText('Welcome, ' + participant)
 
if __name__ == '__main__':
  myRobot = robot.Robot('waveRobot',
      image_url='http://wave-robot-morimasa.appspot.com/assets/icon.png',
      version='1',
      profile_url='http://wave-robot-morimasa.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipCreated)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.Run()
