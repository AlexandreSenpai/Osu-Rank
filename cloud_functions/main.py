from os import environ
from math import floor
from datetime import datetime

from requests import get
from google.cloud import bigquery

##### Osu!Api Configuration #####
user = 'Ryuukiteru'
endpoint = 'https://osu.ppy.sh/api/'
token = environ['OSU_TOKEN']
##### Bigquery Configuration #####
bigquery_dataset = environ['DATASET']
bigquery_table = environ['TABLE']

def send_to_bigquery(arr):
  arr[1] = str(arr[1])
  client = bigquery.Client()
  dataset_id = bigquery_dataset
  table_id = bigquery_table
  table_ref = client.dataset(dataset_id).table(table_id)
  table = client.get_table(table_ref)
  rows_to_insert = [
    (arr)
  ]
  errors = client.insert_rows(table, rows_to_insert)
  assert errors == []

def format_response(res):
  bigquery_input_list = [
    datetime.now(),
    res.get('user_id'),
    res.get('username'),
    res.get('level'),
    res.get('playcount'),
    res.get('pp_rank'),
    res.get('pp_country_rank'),
    res.get('pp_raw'),
    res.get('accuracy'),
    res.get('count300'),
    res.get('count100'),
    res.get('count50')
  ]
  bigquery_correct_type = []
  for x in bigquery_input_list:
    try:
      bigquery_correct_type.append(floor(float(x)))
    except:
      bigquery_correct_type.append(x)
  send_to_bigquery(bigquery_correct_type)

def make_request(request):
    if request.method == 'POST':
        info_req = get(endpoint + 'get_user?u=' + user + '&k=' + token)
        if info_req.status_code == 200:
            format_response(info_req.json()[0])
