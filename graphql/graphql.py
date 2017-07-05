# -*- coding: utf-8 -*-
from datetime import datetime

import settings
import json
from requests import post


def cells_to_graphql(cells, forecast):

    query = ""

    for cell in cells:
        query += cell_to_graphql(cell, forecast)


def cell_to_graphql(cell, forecast):

    return """
mutation {{
  createCell(
    cellId: "{}"
    size: {}
    intensity: {}
    positionX: {}
    positionY: {}
    forecast: {}
    timestamp: "{}"
  ) {{
    id
    cellId
  }}
}}
    """.format(cell.id, cell.size, cell.intensity, cell.center_of_mass[0], cell.center_of_mass[1], forecast,
               datetime.strftime(cell.timestamp, "%Y-%m-%dT%H:%M:00.000Z"))


def save_cells(cells, forecast):

    query = cells_to_graphql(cells, forecast)

    if query:

        headers = {
            'Content-Type': "application/json",
            "Accept": "application/json"
        }

        data = {
            'query': query
        }


        print(data)
        #response = post(settings.GRAPH_COOL_ENDPOINT, headers=headers, data=json.dumps(data))
        #print(response.text)

# data = """
# mutation {
#   createCell(
#     cellId: "e13aeae2c0a549008864bfff43506f7f"
#     size: 29
#     intensity: 3
#     positionX: 45
#     positionY: 48
#     forecast: false
#     timestamp: "2016-11-22T13:57:31.123Z"
#   ) {
#     id
#     cellId
#   }
# }
# """
#
# data = {
#     'query': data
# }
#
# print(data)
#
# r = post(settings.GRAPH_COOL_ENDPOINT, headers=headers, data=json.dumps(data))
# print(r.text)
