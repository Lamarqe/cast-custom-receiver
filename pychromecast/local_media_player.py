import requests
from pychromecast.controllers.media import MediaController
from web_sender_types import Image, MusicTrackMediaMetadata, MediaInfo, QueueItem, QueueUpdateItemsRequest

APP_LOCAL = "D29D8DD1"


class LocalMediaPlayerController(MediaController):
  """Controller to interact with local media player app."""

  def __init__(self, forward_url):
    super().__init__()
    self.app_id = APP_LOCAL
    self.supporting_app_id = APP_LOCAL
    self.forward_url = forward_url
    with requests.post(
      'https://lamarqe.pythonanywhere.com/storeforwardurl',
      data={'localForwardURL': self.forward_url},
      headers={"Content-Type": "application/x-www-form-urlencoded"}
    ) as sidResponse:
      print(sidResponse.text)
      
  def set_MusicTrackMediaMetadata(self, title=None, artist=None, image_url=None):
    images = [] if image_url is None else [Image(image_url)]
    metadata = MusicTrackMediaMetadata()
    metadata[MusicTrackMediaMetadata.TITLE]  = title
    metadata[MusicTrackMediaMetadata.ARTIST] = artist
    metadata[MusicTrackMediaMetadata.IMAGES] = images
    mediainfo = MediaInfo(self.status.content_id, self.status.content_type)
    mediainfo[MediaInfo.METADATA] = metadata
    queueitem = QueueItem(mediainfo)
    queueitem[QueueItem.ITEMID] = 1
    queueUpdateItemsRequest = QueueUpdateItemsRequest([queueitem])

    self._send_command(queueUpdateItemsRequest)

  def quick_play(self, media_id=None, media_type="video/mp4", **kwargs):
    self.play_media(media_id, media_type, **kwargs)

