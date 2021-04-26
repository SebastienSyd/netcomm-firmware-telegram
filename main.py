import requests
import json
import datetime
import logging


logging.basicConfig(filename='output.log', level=logging.DEBUG, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')

def filter_firware(j):
  ''' Filters json result to only get the firmware '''
  try:
    x = j['Item']['Resources']
  except KeyError:
    pass

  result = []
  for i in x:
    if i["TypeCode"] == "Firmware":
      result = i

  return result

def get_latest_firmware(j):
  ''' Only gets the latest released firmware '''
  latest_date = datetime.datetime(1970, 1, 1)
  latest_firmware = None
  for i in j:
    date_time_str = i["ReleaseDate"]
    date_time_obj = datetime.datetime.strptime(date_time_str, '%d/%m/%Y')

    if date_time_obj > latest_date:
      latest_firmware = i
      latest_date = date_time_obj
  
  return latest_firmware

def main():
  url = "https://support.netcommwireless.com/api/ProductModels/NF18MESH"
  res = requests.get(url)
  res.raise_for_status()

  res_json = res.json()

  firmwares = filter_firware(j=res_json)
  logging.info("Retrieved %d firmware", len(firmwares["Resources"]) )
  logging.debug("%s", json.dumps(firmwares["Resources"], indent=2) )

  latest_firmware = get_latest_firmware(j=firmwares["Resources"])
  logging.info("Latest firmware is from %s", latest_firmware["ReleaseDate"])

if __name__ == '__main__':
  main()