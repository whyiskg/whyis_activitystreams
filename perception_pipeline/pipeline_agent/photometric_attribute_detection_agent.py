from whyis.autonomic import UpdateChangeService
from whyis.namespace import NS

from whyis.plugin import Plugin
import rdflib
from flask import current_app


import json
import requests
import numpy as np
import matplotlib.pyplot as plt

from whyis.namespace import sioc_types, sioc, schema, sio, dc, prov, whyis

request_url = "http://127.0.0.1:9191/"

class PhotometricAttributeDetectionAgent(UpdateChangeService):
    activity_class = whyis.PhotometricAttributeDetection # detecting object
    def get_query(self):
        return '''SELECT DISTINCT ?resource WHERE { 
                    ?resource a %s.
                    FILTER NOT EXISTS { ?resource a %s.}
                  }''' % ( self.getInputClass().n3() , self.getOutputClass().n3() )

    def getInputClass(self):
        return schema.ImageObject

    def getOutputClass(self):
        return whyis.PhotometricAttributeDetectedImageObject

    def process(self, i, o):
        r = requests.post(
            request_url + "photometric_attributes",
            json = {
                "image_path":i.identifier
            }
        o.add(rdf.type,whyis.GeometricAttributeDetectedImageObject)
        o.add(sioc.content,r.content)
