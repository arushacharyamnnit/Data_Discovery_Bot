from flask import Flask,render_template,redirect,url_for,request,jsonify,json,make_response,Response
import pandas as pd
import numpy as np
from collections import defaultdict
from pathlib import Path
import spacy
import pprint
from spacy.util import minibatch, compounding
import time
from spacy.matcher import PhraseMatcher
import elasticsearch
import sys
from elasticsearch import Elasticsearch,helpers
import json
from QueryHandler import *
from ModelLoader import *
import slack
import os
from dotenv import load_dotenv
from ElasticSearchQuery import *

from slackeventsapi import SlackEventAdapter
sys.path.insert(0, 'D:\DataDiscovery_Bot\DataDiscovery_Bot\Database\MySQL')
from database_connectivity import DataUpdate,DataUpdate_feedback,DataUpdate_comment
from db_metrics import metrics
import matplotlib.pyplot as plt
import re
import random
from flask_mysqldb import MySQL,MySQLdb
from spacy.tokens import DocBin
# nlp1 = spacy.load('../NLP model/output1/model-best')
# nlp2 = spacy.load('../NLP model/output_ocidw/model-best')
# nlp3=spacy.load('../NLP model/model-last')
# from spello.model import SpellCorrectionModel
# sp = SpellCorrectionModel(language='en')
# sp.load('../NLP model/SpellModel/model.pkl')