from settings.constants import *
import os
import urllib.request
from tqdm import tqdm
import glob
import zipfile


print('小地域データをダウンロード')
for pref_num in tqdm(range(1, 48)):
    num_str = str(pref_num).zfill(2)
    url = REGION_URL_FORMER + num_str + REGION_URL_LATTER
    title = os.path.join(SHP_DIR, num_str + '.zip')
    urllib.request.urlretrieve(url, title)

print('zipファイルを展開')
files = glob.glob(os.path.join(SHP_DIR, "*.zip"))
for file in tqdm(files):
    with zipfile.ZipFile(file, "r") as f:
        f.extractall(SHP_DIR)





