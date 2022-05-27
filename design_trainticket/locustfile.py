from locust import HttpUser, task, between, constant
from datetime import datetime, timedelta, date
from random import randint
import numpy as np
import logging
import sys
import time
import logging
import uuid
import json
import random
import string
from requests.adapters import HTTPAdapter

import locust.stats
book_res ={}
customer_res ={}
book_id = []
locust.stats.CONSOLE_STATS_INTERVAL_SEC = 30
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 10
locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99, 0.999, 0.9999, 1.0]

DEP_DATE = "2022-02-11"

def random_date_generator():
    temp = randint(0, 4)
    random_y = 2000 + temp * 10 + randint(0, 9)
    random_m = randint(1, 12)
    random_d = randint(1, 28)  # to have only reasonable dates
    return str(random_y) + "-" + str(random_m) + "-" + str(random_d)

def random_string_generator():
    return random.choices(string.ascii_lowercase, k=5)
class Requests:
    def create_book(self):
	for 1 in range(10):
	 title = random_string_generator()
	 author = random_string_generator()
	 self.client.post("/book", json={"title": title, "author": author})
   def get_books(self):
	x = self.client.get("/books")
	book_res = json.loads(x.text)
	for k in book_res.items():
	  if k == "_id":
		book_id.append(book_res[k]) 
   def create_customer(self):
	for 1 in range(10):
         name = random_string_generator()
	 address = random_string_generator()
	 age= randint(16,35)
	 self.client.post("/customer", json={"name": name, "age":age,"address": address}
   def create_order(self):
	for i in range(10):
	date = random_date_generator()
	self.client.post("/order", json={"customerID": customer[i]., "bookID":bookID, "initialDate"):
    def try_to_read_response_as_json(self, response):
        try:
            return response.json()
        except:
            try:
                return response.content.decode("utf-8")
            except:
                return response.content

  
    def perform_task(self, name):
        logging.debug(f"""Performing task "{name}" for user {self.request_id}...""")
        task = getattr(self, name)
        task()


class UserNoLogin(HttpUser):
    weight = 50
    wait_time = constant(1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

    @task
    def perfom_task(self):
        requests = Requests(self.client)
