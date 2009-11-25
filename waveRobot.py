import sys, re, urllib, urllib2, logging
from waveapi import simplejson
from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document

reBitly = re.compile('http://bit.ly/[a-zA-Z0-9]+\s')
apiBitly = "http://api.bit.ly/%s?version=2.0.1&%s=%s&login=morimasa&apiKey=R_1f3b290d76d173c8d4bcef2dea8ecdb5"

def bitly(url):
  if reBitly.match(url) :
    info = 1
    hashUrl = url.replace("http://bity.ly/", "")
    apiUrl = apiBitly % ('info', 'shortUrl', urllib.quote(hashUrl))
  else :
    apiUrl = apiBitly % ('shorten', 'longUrl', urllib.quote(hashUrl))

  json = urllib2.urlopen(apiUrl).read()
  data = simplejson.loads(json)
  if info:
    for k,v in data['results'].iteritems():
      return data['results'][k]['longUrl']
  else:
    for k,v in data['results'].iteritems():
      return data['results'][k]['shortUrl'];

def OnParticipantsChanged(properties, context):
  added = properties['participantsAdded']
  for participant in added:
    Greet(context, participant)
 
def Greet(context, participant):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText('Welcome, ' + participant)
 
def OnRobotAdded(properties, context):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText('Hi, everybody!')
 
def OnBlipSubmitted(properties, context):
  blip = context.GetBlipById(properties['blipId'])
  doc = blip.GetDocument()
  text = doc.GetText()
  bitlied = []
  for ann in blip.annotations:
    logging.info('ann.name:'+ann.name + ' ann.value:'+ann.value)
    if ann.name == 'link/auto' and reBitly.match(ann.value):
      bitlied.append((ann.range.start, ann.range.end, ann.value))
  
  for start, end, value in bitlied:
    url = bitly(value)
    if url:
      payload = text[start:end]
      logging.info('payload:'+payload+' value:'+value+ ' link to:'+url)
      range = document.Range(start, end)
      doc.DeleteAnnotationsInRange(range, 'link/auto')
      doc.SetAnnotation(range, 'link/manual', url)
      doc.AppendText(value+' was unbit.lied ;-)')

if __name__ == '__main__':
  myRobot = robot.Robot('waveRobot',
      image_url='http://wave-robot-morimasa.appspot.com/assets/icon.png',
      version='4',
      profile_url='http://wave-robot-morimasa.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.Run()
