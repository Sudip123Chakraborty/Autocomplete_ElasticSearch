
from flask import app,Flask
from flask_restful import Resource, Api, reqparse
import elasticsearch
from elasticsearch import Elasticsearch
import datetime
import concurrent.futures
import requests
import json


app = Flask(__name__)
api = Api(app)

#------------------------------------------------------------------------------------------------------------

NODE_NAME = 'sample'
es = Elasticsearch([{'host': '52.66.229.240', 'port': 9200}])

#------------------------------------------------------------------------------------------------------------


"""
{
	"wildcard": {
	    "item": {
	        "value": "{}*".format(self.query)
	    }
	}
}							
 {
                            "match_phrase_prefix": {
                                "from_station_name.keyword": {
                                    "query": "{}".format(self.query)
                                }
                            }
                        }

"""


class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        self.baseQuery ={
            "_source": [],
            "size": 0,
            "min_score": 0,
            "query": {
                "bool": {
                    "must": [
                        {
							"wildcard": {
							    "item": {
							        "value": "{}*".format(self.query)
							    }
							}
						}
						#,
						#{
						#	"wildcard": {
						#	    "category": {
						#	        "value": "grocery"
						#	    }
						#	}
						#}
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            },
            "aggs": {
                  "auto_complete": {
                      "terms": {
                          "field": "item",
                          
                          "order": {
                              "_count": "desc"
                          },
                          "size": 25
                      },
                      "aggs": {
                        "category": {
                          "terms": {
                            "field": "category"
                          }
                        }
                      }
                  }
              }
        }

    def get(self):
        res = es.search(index=NODE_NAME, size=0, body=self.baseQuery)
        return res


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')
