from lib.calc_area_stats import *
from tqdm import tqdm
import geopandas as gpd
from lib.district import District
import csv
from settings.constants import *
import os



def main():

    shp_file = 'shp_data/h27ka13.shp'  # 東京都
    # shp_file = 'shp_data/h27ka31.shp'  # 鳥取県
    # shp_file = 'test/test_data/h27ka13114.shp'  # 中野区

    output_district_data(shp_file)

def output_district_data(shp_file):

    df_shp = gpd.read_file(shp_file)

    columns = [
        'pref',
        'city',
        'district',
        'center_lat',
        'center_lon',
        'area',
        'entropy',
        'road_length',
        'road_density',
        'circuity',
        'complexity'
    ]

    file_name = os.path.splitext(os.path.basename(shp_file))[0] + '.csv'
    file_path = os.path.join(CSV_DIR, file_name)
    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, columns)
        writer.writeheader()
    print(len(df_shp))
    for row in tqdm(df_shp.itertuples()):
        d = District(
            row.PREF_NAME,
            row.CITY_NAME,
            row.S_NAME,
            row.AREA,
            row.geometry
        )
        if '区' not in d.city:
            continue
        if row.JINKO == 0:
            # 人口ゼロは無視
            continue
        if d.Gu == 0:
            # ネットワークがない
            continue

        with open(file_path, 'a') as f:
            writer = csv.DictWriter(f, columns)
            writer.writerow({
                'pref': d.pref,
                'city': d.city,
                'district': d.district,
                'center_lat': d.center_lat,
                'center_lon': d.center_lon,
                'area': d.area,
                'entropy': d.entropy,
                'road_length': d.road_length,
                'road_density': d.road_density,
                'circuity': d.circuity,
                'complexity': d.complexity
            })
        d.save_network_fig(os.path.join(PNG_DIR, f"{d.name}_network.png"))
        d.save_bearings_fig(os.path.join(PNG_DIR, f'{d.name}_bearings.png'))

if __name__ == '__main__':
    main()