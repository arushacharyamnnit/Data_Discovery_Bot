from elasticsearch import Elasticsearch,helpers

es = Elasticsearch([{'host':'localhost','port':'9200'}])