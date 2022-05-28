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

    output_district_data(shp_file)

def output_district_data(shp_file):

    df_shp = gpd.read_file(shp_file)

    columns = [
        '都道府県',
        '市町村',
        '地区',
        '中心経度',
        '中心緯度',
        '面積 (m^2)',
        '方向エントロピー',
        '道路延長 (m)',
        '道路密度 (km/km^2)',
        'circuity'
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
        if d.Gu == 0:
            # ネットワークがない
            continue

        with open(file_path, 'a') as f:
            writer = csv.DictWriter(f, columns)
            writer.writerow({
                '都道府県': d.pref,
                '市町村': d.city,
                '地区': d.district,
                '中心経度': d.center_lon,
                '中心緯度': d.center_lat,
                '面積 (m^2)': d.area,
                '方向エントロピー': d.entropy,
                '道路延長 (m)': d.road_length,
                '道路密度 (km/km^2)': d.road_density,
                'circuity': d.circuity
            })
        d.save_network_fig(os.path.join(PNG_DIR, f"{d.name}_network.png"))
        d.save_bearings_fig(os.path.join(PNG_DIR, f'{d.name}_bearings.png'))
        






    # with open(os.path.join(CSV_DIR, file_name), 'w') as f:
    #     writer = csv.DictWriter(f, columns)
    #     writer.writeheader()
    #     for d in tqdm(districts):
    #         writer.writerow({
    #             '都道府県': d.pref,
    #             '市町村': d.city,
    #             '地区': d.district,
    #             '中心経度': d.center_lon,
    #             '中心緯度': d.center_lat,
    #             '面積 (m^2)': d.area,
    #             '方向エントロピー': d.entropy,
    #             '道路延長 (m)': d.road_length,
    #             '道路密度 (km/km^2)': d.road_density,
    #             'circuity': d.circuity
    #         })
    
    # print('ネットワークとbearingsの描画')
    # for d in tqdm(districts):
    #     d.save_network_fig(os.path.join(PNG_DIR, f"{d.name}_network.png"))
    #     d.save_bearings_fig(os.path.join(PNG_DIR, f'{d.name}_bearings.png'))
    
    

if __name__ == '__main__':
    main()