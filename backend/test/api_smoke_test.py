import json
import time
from urllib.request import urlopen

URL = 'http://localhost:8000/'

for _ in range(10):
    try:
        with urlopen(URL) as resp:
            data = json.load(resp)
            assert 'message' in data
            assert '課題管理API' in data['message']
            print('API responded:', data)
            break
    except Exception as e:
        print('Waiting for API...', e)
        time.sleep(3)
else:
    raise SystemExit('API did not start in time')
