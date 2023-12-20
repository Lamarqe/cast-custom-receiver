import time
import pychromecast
import zeroconf
from cast_finder import CastFinder
from local_media_player import LocalMediaPlayerController


castFinder = CastFinder("Nest Hub")
castFinder.doDiscovery()

chromecast = pychromecast.get_chromecast_from_cast_info(castFinder.device, zeroconf.Zeroconf())

chromecast.wait()
if (chromecast.app_id != pychromecast.IDLE_APP_ID):
  chromecast.quit_app()
  time.sleep(0.5)

controller = LocalMediaPlayerController('http://192.168.2.21:12345/local/CastReceiver/receiver.html')
chromecast.register_handler(controller)

controller.play_media('http://192.168.2.48:8000/test.mp3', 'audio/mpeg')
controller.block_until_active()

titles     = ['Mario', 'Luigi']
artists    = ['Ist super.', 'Ist besser!']
image_urls = ['https://mario.wiki.gallery/images/0/0d/SMBW_Mario_Jump.png', 'https://mario.wiki.gallery/images/7/72/MPSS_Luigi.png']

count = 0
while True:
  chromecast.wait()
  controller.set_MusicTrackMediaMetadata(
    title     = titles     [count % 2],
    artist    = artists    [count % 2],
    image_url = image_urls [count % 2])
  count += 1
  time.sleep(5.0)
