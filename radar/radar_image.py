import boto3
from botocore.exceptions import ClientError
import settings
from PIL import Image
from numpy import array
from io import BytesIO
from requests import get
from radar.utils import convert_to_timestring


class RadarImage(object):
    def __init__(self, crop_coords, url=None, timestamp=None, forecast=None):

        url, image_name = self._get_image_name(timestamp, forecast, url)

        if url.startswith('http'):
            response = get(url)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(image_name)

        if image.palette:
            image = image.convert(mode='RGBA')

        if settings.SAVE_TO_S3:
            self._save_to_s3(image, image_name)

        self._image_data = array(image.crop(crop_coords))
        self._image_name = image_name
        # import scipy
        # scipy.misc.imsave(image_name, self._image_data)

        self._has_alpha = self._image_data.shape[2] == 4

    def get_rgb_for_position(self, position):
        return self._image_data[position[0]][position[1]][:-1]

    # todo move to own file/class
    def _save_to_s3(self, image, image_name):
        client = boto3.client(
            's3',
            aws_access_key_id=settings.S3_ACCESS_ID,
            aws_secret_access_key=settings.S3_ACCESS_SECRET,
        )

        try:
            client.head_object(Bucket=settings.S3_BUCKET, Key=image_name)
        except ClientError as e:
            if (e.response['Error']['Code']) != 404:
                image_bytes = BytesIO()
                image.save(image_bytes, format('PNG'))

                client.put_object(Body=image_bytes.getvalue(), Bucket=settings.S3_BUCKET,
                                  Key=image_name)

    @property
    def image_data(self):
        return self._image_data

    @staticmethod
    def _get_image_name(timestamp, forecast, url):

        # use local files. Mainly for testing
        if url and url.startswith('file:'):
            image_name = url.replace('file:', '')

        else:
            timestring = convert_to_timestring(timestamp)

            if not forecast and not url:
                image_name = "PPIMERCATOR.%s.png" % (timestring)
            else:
                # this is sometimes not available from the website, so it is currently not used here
                image_name = "FCSTMERCATOR.%s.png" % (timestring)

            if not forecast and not url:
                url = "https://www.srf.ch/meteo/static/map/layer/radar/web/%s" % (image_name)

        return url, image_name
