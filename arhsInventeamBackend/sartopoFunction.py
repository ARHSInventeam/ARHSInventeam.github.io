from sartopo_python import SartopoSession
import requests
from sartopo_python import SartopoSession
import requests
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



def relayData():
  
  while True:
    
    mapKey = "8G1DF"

    configFilePath = "Downloads/ConfigParserTestSartopo.INI"

    accountEmail = "arhsinventeam@gmail.com"

    #url = "https://arhsinventeam.github.io."

    #markerData = ["874cbf7d-dd98-437c-afff-478b199401e5", "2", "backendTest","TV9JRL"]

    sts2=SartopoSession(    
        "sartopo.com",  #sartopo.com
        mapKey,
        #Downloads\ConfigParserTestSartopo.INI
        #../../sts.ini
        configpath=configFilePath,
        account=accountEmail)


    #def unpackSentData(sentData):
    sentData = {
      "heartRate" : 90,
      "temp" : 98,
      "spo2" : 97
      }  

    dataList = [i for i in sentData.split("/")]
    dataDict = {}
    for i in dataList:
      secondSplit = [v for v in i.split(":")]
      dataDict[secondSplit[0]] = secondSplit[1]
    #return dataDict
    data = dataDict
      
      
    #def relayDataToSartopo(data):
    markerID = data["markerID"]
    markerFID = data["markerFID"]
    markerName = data["markerName"]
    userID = "TV9JRL"
    statusToColor = {"good" : "#0CFF00", "neutral" : "#FBFF00", "bad" : "#FF0000"}
    thresholdList = {"heartRate" : [60,100,170,50], "spo2" : [95, 100, 93, 100], "temp" : [98, 99, 100, 97]}
    statusList = {"heartRate" : "", "spo2" : "", "temp" : ""}
    statReport = ""
    for i in data:
      if i in thresholdList:
        if int(data[i]) >= thresholdList[i][0] and int(data[i]) <= thresholdList[i][1]:
          statusList[i] = "good"
        else:
          if int(data[i]) > thresholdList[i][1]:
            if i == "heartRate":
              if int(data[i]) <= thresholdList[i][2]:
                statusList[i] = "neutral"
              else:
                statusList[i] = "bad"
            elif i == "spo2":
              statusList[i] = "bad"
              
            elif i == "temp":
              if int(data[i]) <= thresholdList[i][2]:
                statusList[i] = "neutral"
              elif int(data[i]) > thresholdList[i][2]:
                statusList[i] = "bad"
          elif int(data[i]) < thresholdList[i][0]:
            if int(data[i]) >= thresholdList[i][3]:
              statusList[i] = "neutral"
            else:
              statusList[i] = "bad"
      
      statusListStats = [statusList[x] for x in statusList]
      
      neutralStats = 0
      
      for i in ["bad", "neutral", "good"]:
        if i in statusListStats:
          if i == "neutral":
            neutralStats += 1
          statReport = i
          break
        

      if neutralStats > 2:
        statReport = "bad"
      #requests.get("https://caltopo.com/api/v1/position/report/%s?id=%s&lat=%s&lng=%s" %(name, id, lat, long))
      #print(statReport)
      requests.get("https://caltopo.com/api/v1/position/report/%s?id=%s&lat=%f&lng=%f" %(markerName, markerFID, float(data["lat"]), float(data["lon"])))
      sts2.editFeature(id=markerID,className="LiveTrack", title=markerName, properties={'stroke-opacity': 1, 'creator': userID, 'pattern': 'M-5 5L0 -5M5 5L0 -5,20,40,T', 'stroke-width': 1, 'title': markerName, 'deviceId': 'FLEET:%s-%s' %(markerName, markerFID), 'stroke': statusToColor[statReport], 'class': 'LiveTrack', 'updated': 1713897329000}, timeout=10000)

    #relayDataToSartopo({"heartRate" : 100, "spo2" : 95, "temp" : 98, "lat" : 42.38192, "lon" : -72.51581}, markerData)
    #relayDataToSartopo(unpackSentData("markerName:TEST/markerFID:1/markerID:f1339589-a23b-4bf9-bb94-91cb31bc577a/lat:42.38271/lon:-72.51457/gsr:1/temp:98/heartRate:90/spo2:95"))
