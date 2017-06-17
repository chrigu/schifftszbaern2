# -*- coding: utf-8 -*-


class DataStorage(object):

    def __init__(self, filename):
        self.filename = filename

    def _prepare_data(self, timestamp, radar_history, next_hit, rain_at_pos):

        radar_history_dicts = list(map(lambda radar_data: radar_data.to_dict(), radar_history))

        data = {
            'timestamp': timestamp,
            'radar_history': radar_history_dicts,
            'next_hit': next_hit.to_dict(),
            'rain_at_position': rain_at_pos
        }
        return data

    def save_data(self, timestamp, radar_history, next_hit, rain_at_pos):
        pass
        # #save data, convert datetime objects to strings
        # try:
        #     if last_dry:
        #         last_dry_string = datetime.strftime(last_dry, settings.DATE_FORMAT)
        #     else:
        #         last_dry_string = None
        #
        #     if last_rain:
        #         last_rain_string = datetime.strftime(last_rain, settings.DATE_FORMAT)
        #     else:
        #         last_rain_string = None
        #
        #     #save data to file
        #     save_data = {'last_update': datetime.strftime(last_update, settings.DATE_FORMAT), 'queue': queue_to_save,
        #                  'last_sample_rain': rain_now, 'last_dry': last_dry_string,
        #                 'last_rain': last_rain_string, 'next_hit': next_hit, 'intensity': intensity,
        #                  'last_sample_snow': snow, 'location_weather_data': location_weather_data,
        #                  'prediction_id': prediction_id}

        #     with open(self.filename, 'w') as outfile:
        #         json.dump(save_data, outfile, default=self.encode)
        #
        #     return True
        #
        # except Exception, e:
        #     if settings.DEBUG:
        #         print e
        #
        # return False