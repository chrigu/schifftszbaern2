# -*- coding: utf-8 -*-
from datetime import datetime

import settings
import json
from requests import post

HEADERS = {
            'Content-Type': "application/json",
            "Accept": "application/json"
        }


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
    _save_graphql(query)


def _save_graphql(query):

    if query:

        data = {
            'query': query
        }


        print(data)
        post(settings.GRAPH_COOL_ENDPOINT, headers=HEADERS, data=json.dumps(data))

def save_current(intensity):
    query = """
    mutation {{
      createRainLocation(
        intensity: {}
      ) {{
        id
        intensity
        createdAt
      }}
    }}
        """.format(intensity)

    _save_graphql(query)
