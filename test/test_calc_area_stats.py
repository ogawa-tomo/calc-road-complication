import sys
sys.path.append('./')
from src.calc_area_stats import calc_area_from_polygon, calc_entropy_from_polygon, calc_total_length_from_polygon
import os
import geopandas as gpd

def test_calc_area_from_polygon():

    data_dir = './test/test_data'

    # 戸田市
    df_shp = gpd.read_file(os.path.join(data_dir, 'h27ka11224.shp')) # 戸田市
    index = 20  # 上戸田1丁目
    polygon = df_shp.geometry[index]
    assert calc_area_from_polygon(polygon) == 0.15027209676913733

    # カナダ
    # https://qiita.com/HidKamiya/items/c27c9fe7d8533cfe8a73
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    cana = world['geometry'][3] # MultiPolygon
    assert calc_area_from_polygon(cana) == 9986763.834110908

def test_calc_entropy_from_polygon():

    print("")

    data_dir = './test/test_data'

    df_shp = gpd.read_file(os.path.join(data_dir, 'h27ka13114.shp'))  # 中野区
    index = 20  # 中央4丁目
    polygon = df_shp.geometry[index]

    entropy = calc_entropy_from_polygon(polygon)

    assert entropy == 3.126610315560262

def test_calc_total_length_from_polygon():

    data_dir = './test/test_data'

    df_shp = gpd.read_file(os.path.join(data_dir, 'h27ka11224.shp')) # 戸田市
    index = 25  # 大字上戸田
    polygon = df_shp.geometry[index]

    total_length = calc_total_length_from_polygon(polygon)

    assert total_length == 1595.8020000000001









