import os
import json
import redis
import logging
from sartopo_python import SartopoSession
import requests

logging.basicConfig(level=logging.INFO)

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(redis_url)

def relayData(data):
    mapKey = "8G1DF"

    configFilePath = "/app/ConfigParserTestSartopo.INI"

    accountEmail = "arhsinventeam@gmail.com"

    sts2=SartopoSession(    
    "sartopo.com",  #sartopo.com
    mapKey,
    #Downloads\ConfigParserTestSartopo.INI
    #../../sts.ini
    configpath=configFilePath,
    account=accountEmail)
    #def relayDataToSartopo(data):
    
    markerID = data["markerID"]
    markerFID = data["markerFID"]
    markerName = data["markerName"]
    #heartRate, spo2, temp, verify (all are strings)

    userID = "TV9JRL"
    statusToColor = {"good" : "#0CFF00", "neutral" : "#FBFF00", "bad" : "#FF0000"}
    thresholdList = {"heartRate" : [60.0,160.0,190.0,50.0], "spo2" : [95.0, 100.0, 100.0, 90.0], "temp" : [98.0, 99.0, 101.0, 97.0]}
    statusList = {"heartRate" : "", "spo2" : "", "temp" : ""}
    statReport = ""
    for i in data:
      if i in thresholdList:
        if float(data[i]) >= thresholdList[i][0] and float(data[i]) <= thresholdList[i][1]:
          statusList[i] = "good"
        else:
          if i == "spo2":
              if float(data[i]) < thresholdList[i][3]:
                statusList[i] = "bad"
              elif float(data[i]) < thresholdList[i][1] and float(data[i]) > thresholdList[i][3] and float(data[i]) < thresholdList[i][0]:
                statusList[i] = "neutral"  
          else:
              if float(data[i]) > thresholdList[i][1]:
                if i == "heartRate":
                  if float(data[i]) <= thresholdList[i][2]:
                    statusList[i] = "neutral"
                  else:
                    statusList[i] = "bad"
                #elif i == "spo2":
                  #statusList[i] = "bad"
                  
                elif i == "temp":
                  if float(data[i]) <= thresholdList[i][2]:
                    statusList[i] = "neutral"
                  elif float(data[i]) > thresholdList[i][2]:
                    statusList[i] = "bad"
              elif float(data[i]) < thresholdList[i][0]:
                if float(data[i]) >= thresholdList[i][3]:
                  statusList[i] = "neutral"
                else:
                  statusList[i] = "bad"
      
      counters = {"good" : 0, "neutral" : 0, "bad" : 0}
      

      for i in statusList:
        if statusList[i] != "":
          counters[statusList[i]] += 1
          
      if counters["bad"] != 0:
        statReport = "bad"
      elif counters["neutral"] > counters["good"]:
        statReport = "neutral"
      else:
        statReport = "good"
      #requests.get("https://caltopo.com/api/v1/position/report/%s?id=%s&lat=%s&lng=%s" %(name, id, lat, long))
      #prfloat(statReport)
    requests.get("https://caltopo.com/api/v1/position/report/%s?id=%s&lat=%s&lng=%s" %(markerName, markerFID, data["lat"], data["lon"]))
    sts2.editFeature(id=markerID,className="LiveTrack", title=markerName, properties={'stroke-opacity': 1, 'creator': userID, 'pattern': 'M-5 5L0 -5M5 5L0 -5,20,40,T', 'stroke-width': 1, 'title': markerName, 'deviceId': 'FLEET:%s-%s' %(markerName, markerFID), 'stroke': statusToColor[statReport], 'class': 'LiveTrack', 'updated': 1713897329000}, timeout=10000)

def listen_and_execute():
    logging.info("Worker started, waiting for tasks...")
    while True:
        _, message = redis_client.blpop('task_queue')
        logging.info(message)
        data = json.loads(message.decode('utf-8'))
        if "verifyKey" in data:
          if data["verifyKey"] == "54321":
            relayData(data)
          # Remove the processed sk from the queue
        # Assuming that the task is successfully processed
        #redis_client.lrem('task_queue', 1, message)  # Remove one occurrence of message from the queue

if __name__ == '__main__':
    listen_and_execute()

'''
import os
import redis
from redis import Redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker

listen = ['high', 'default', 'low']

#redis_url = redis.from_url(os.getenv('REDIS_URL'))
#if not redis_url:
 #   raise RuntimeError("Set up Heroku Data For Redis first, \
  #  make sure its config var is named 'REDIS_URL'.")

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(redis_url)
#conn = redis.Redis(
    #host="ec2-100-26-90-46.compute-1.amazonaws.com",
    #password="p70f1a6680c12d91324454d4dd750d40d3a21cc2ae1ca71ac17bf53a9e6086003",
    #port=19610,
    #ssl=True,
    #ssl_cert_reqs=None,
    #ssl_ca_data=None)

if __name__ == '__main__':
    with Connection(redis_client):
        worker = Worker(map(Queue, listen))
        worker.work()
'''


