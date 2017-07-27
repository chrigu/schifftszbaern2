# -*- coding: utf-8 -*-
from datetime import datetime

import settings
import json
from requests import post


def cells_to_graphql(cells, forecast):

    if len(cells) == 0:
        return ""

    query = """
    mutation {
    """

    for index, cell in enumerate(cells):
        query += cell_to_graphql(cell, forecast, index)

    query += """
        }
    """

    return query


def cell_to_graphql(cell, forecast, index):

    forecast_string = "false"

    if forecast:
        forecast_string = "true"

    return """
    cell{}: createCell(
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
    """.format(index, cell.id, int(cell.size), cell.intensity['intensity'], cell.center_of_mass[0], cell.center_of_mass[1],
               forecast_string, datetime.strftime(cell.timestamp, "%Y-%m-%dT%H:%M:00.000Z"))


def save_cells(cells, forecast):

    query = cells_to_graphql(cells, forecast)
    if query != "":
        _save_graphql(query)


def _save_graphql(query):

    if query:

        data = {
            'query': query
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(settings.GRAPH_COOL_TOKEN)
        }

        response = post(settings.GRAPH_COOL_ENDPOINT, headers=headers, data=json.dumps(data))
        print(response)


def save_current(weather_data):

    if 'weatherCode' in weather_data:

        query = """
        mutation {{
          createWeatherLocation(
            intensity: {}
            weatherCode: {}
            temperature: {}
          ) {{
            id
            intensity
            weatherCode
            temperature
            createdAt
          }}
        }}
            """.format(weather_data['intensity'], weather_data['weatherCode'], weather_data['temperature'])

    else:
        query = """
        mutation {{
          createWeatherLocation(
            intensity: {}
          ) {{
            id
            intensity
            createdAt
          }}
        }}
            """.format(weather_data['intensity'])
    _save_graphql(query)
