from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import time

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def scrape_title(url):
    youtube = build('youtube','v3', developerKey="AIzaSyA2m8CGKeNOE4OaPdgDQYZdlyCt-uasSFQ") 


    video_request=youtube.videos().list(
    part='snippet,statistics, contentDetails',
    id=video_id(url)
)
  
    video_response = video_request.execute()
    title = video_response['items'][0]['snippet']['title']
    duration= video_response['items'][0]['contentDetails']['duration']
    duration= time.strftime('%H:%M:%S', time.gmtime(convert_YouTube_duration_to_seconds(duration)))
    thumbnail= video_response['items'][0]['snippet']['thumbnails']['default']['url']
    return title, duration, thumbnail


def convert_YouTube_duration_to_seconds(duration):
   day_time = duration.split('T')
   day_duration = day_time[0].replace('P', '')
   day_list = day_duration.split('D')
   if len(day_list) == 2:
      day = int(day_list[0]) * 60 * 60 * 24
      day_list = day_list[1]
   else:
      day = 0
      day_list = day_list[0]
   hour_list = day_time[1].split('H')
   if len(hour_list) == 2:
      hour = int(hour_list[0]) * 60 * 60
      hour_list = hour_list[1]
   else:
      hour = 0
      hour_list = hour_list[0]
   minute_list = hour_list.split('M')
   if len(minute_list) == 2:
      minute = int(minute_list[0]) * 60
      minute_list = minute_list[1]
   else:
      minute = 0
      minute_list = minute_list[0]
   second_list = minute_list.split('S')
   if len(second_list) == 2:
      second = int(second_list[0])
   else:
      second = 0
   return day + hour + minute + second

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)