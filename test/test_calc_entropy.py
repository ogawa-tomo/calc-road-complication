import os
import sys
sys.path.append('./')
import geopandas as gpd
import osmnx as ox
from src.bearing import orientation_entropy
from src.calc_area_stats import get_Gu_from_polygon


def test_oriantation_entropy():

    print("")

    data_dir = './test/test_data'

    df_shp = gpd.read_file(os.path.join(data_dir, 'h27ka13114.shp'))  # 中野区
    index = 20  # 中央4丁目
    polygon = df_shp.geometry[index]

    Gu = get_Gu_from_polygon(polygon)

    # エントロピー計算
    entropy = orientation_entropy(Gu, weight='length')
    print(f'osmnx entropy with length = {entropy}')
    assert entropy == 3.126610315560262