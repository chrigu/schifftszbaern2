import settings
from radar import get_radar_data

def collect_data():
    get_radar_data((settings.X_LOCATION, settings.Y_LOCATION))


if __name__ == '__main__':
    collect_data()
