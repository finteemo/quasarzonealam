import time
from quaasar_bot import gethotdeal, send_tgmessage
keyword_item = input("뭐 찾을까?")
while True:
    latest = gethotdeal()
    send_tgmessage(latest, keyword_item)
    time.sleep(90)
