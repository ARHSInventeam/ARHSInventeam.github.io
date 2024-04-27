from sartopo_python import SartopoSession
import time
import json
import requests
from selenium import webdriver 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
import time 
import json 
from bs4 import BeautifulSoup
import csv



mapKey = "8G1DF"

configFilePath = "Downloads/ConfigParserTestSartopo.INI"

accountEmail = "arhsinventeam@gmail.com"

url = "https://arhsinventeam.github.io."

markerData = ["874cbf7d-dd98-437c-afff-478b199401e5", "2", "backendTest","TV9JRL"]

sts2=SartopoSession(    
    "sartopo.com",  #sartopo.com
    mapKey,
    #Downloads\ConfigParserTestSartopo.INI
    #../../sts.ini
     configpath=configFilePath,
     account=accountEmail)



def relayDataToSartopo(data, markerData):
  markerID = markerData[0]
  markerFID = markerData[1]
  markerName = markerData[2]
  userID = markerData[3]
  statusToColor = {"good" : "#0CFF00", "neutral" : "#FBFF00", "bad" : "#FF0000"}
  thresholdList = {"heartRate" : [60,100,170,50], "spo2" : [95, 100, 93], "temp" : [98, 99, 100, 97]}
  statusList = {"heartRate" : "", "spo2" : "", "temp" : ""}
  statReport = ""
  for i in data:
    if i in thresholdList:
      if data[i] >= thresholdList[i][0] and data[i] <= thresholdList[i][1]:
        statusList[i] = "good"
      else:
        if data[i] > thresholdList[i][1]:
          if i == "heartRate":
            if data[i] <= thresholdList[i][2]:
              statusList[i] = "neutral"
            else:
              statusList[i] = "bad"
          elif i == "spo2":
            statusList[i] = "bad"
          elif i == "temp":
            if data[i] <= thresholdList[i][2]:
              statusList[i] = "neutral"
            elif data[i] > thresholdList[i][2]:
              statusList[i] = "bad"
        elif data[i] < thresholdList[i][0]:
          if data[i] >= thresholdList[i][3]:
            statusList[i] = "neutral"
          else:
            statusList[i] = "bad"
  
  statusListStats = [statusList[x] for x in statusList]
  print(statusListStats)
  for i in ["bad", "neutral", "good"]:
    if i in statusListStats:
      statReport = i
      break
  
  #requests.get("https://caltopo.com/api/v1/position/report/%s?id=%s&lat=%s&lng=%s" %(name, id, lat, long))
  requests.get("https://caltopo.com/api/v1/position/report/%s?id=%s&lat=%f&lng=%f" %(markerName, markerFID, data["lat"], data["lon"]))
  sts2.editFeature(id=markerID,className="LiveTrack", title=markerName, properties={'stroke-opacity': 1, 'creator': userID, 'pattern': 'M-5 5L0 -5M5 5L0 -5,20,40,T', 'stroke-width': 1, 'title': markerName, 'deviceId': 'FLEET:%s-%s' %(markerName, markerFID), 'stroke': statusToColor[statReport], 'class': 'LiveTrack', 'updated': 1713897329000}, timeout=10000)

relayDataToSartopo({"heartRate" : 100, "spo2" : 95, "temp" : 98, "lat" : 42.38052, "lon" : -72.51561}, markerData) #the heartrate, spo2, temp, lat, and long are hardcoded here


