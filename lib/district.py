from time import sleep
from webbrowser import BaseBrowser
from lib.calc_area_stats import *
from lib.bearing import orientation_entropy
import folium
from tqdm import tqdm
import re
from shapely.ops import unary_union


class DistrictsManager(object):

    def __init__(self, df_shp) -> None:
        self.__districts = self.__make_districts(df_shp)
    
    @staticmethod
    def __make_districts(df_shp):

        districts = list()
        for row in tqdm(df_shp.itertuples()):
            d = District(
                row.PREF_NAME,
                row.CITY_NAME,
                re.split('１|２|３|４|５|６|７|８|９|０', row.S_NAME)[0],  # '○丁目'の前の部分
                row.AREA,
                row.geometry
            )
            if len(districts) == 0:
                districts.append(d)
                continue
            prev_district = districts[-1]
            if prev_district.name == d.name:
                # ○丁目の前までの名前が直前と一致していたら、合体する
                new_district = District(
                    d.pref,
                    d.city,
                    d.district,
                    d.area + prev_district.area,
                    unary_union([d.polygon, prev_district.polygon])
                )
                districts[-1] = new_district
            else:
                districts.append(d)
            
        return districts
    
    @property
    def districts(self):
        return self.__districts







class District(object):

    def __init__(self, pref, city, district, area, polygon) -> None:

        self.__BUFFER = 0.0001  # バッファをとる量

        self.__pref = pref
        self.__city = city
        self.__district = district
        self.__area = area
        self.__polygon = polygon
        # self.__polygon = polygon.buffer(-self.__buffer)  # バッファをとる
        self.__Gu = None  # bearings情報のついったundirectedなネットワーク
        self.__entropy = None
        self.__road_length = None
        self.__centroid = None
        self.__circuity = None
        self.__complexity = None
    
    @property
    def pref(self):
        return self.__get_name_avoid_none(self.__pref)
    
    @property
    def city(self):
        return self.__get_name_avoid_none(self.__city)
    
    @property
    def district(self):
        return self.__get_name_avoid_none(self.__district)
    
    @staticmethod
    def __get_name_avoid_none(name):
        if name is None:
            return ''
        return name
    
    @property
    def name(self):
        return self.pref + self.city + self.district
    
    @property
    def area(self):
        return self.__area
    
    @property
    def polygon(self):
        return self.__polygon
    
    @property
    def Gu(self):
        if self.__Gu is not None:
            return self.__Gu
        self.__Gu = get_Gu_from_polygon(self.polygon.buffer(-self.__BUFFER))  # バッファをとる
        return self.__Gu
    
    @property
    def entropy(self):
        if self.__entropy is not None:
            return self.__entropy
        self.__entropy = calc_entropy_from_Gu(self.Gu)
        return self.__entropy
    
    @property
    def road_length(self):
        if self.__road_length is not None:
            return self.__road_length
        self.__road_length = calc_road_length_from_Gu(self.Gu)
        return self.__road_length
    
    @property
    def road_density(self):
        # 1平方kmあたりの道路延長（km）
        return (self.road_length / 10**3) / (self.area / 10**6)
    
    @property
    def centroid(self):
        if self.__centroid is not None:
            return self.__centroid
        self.__centroid = self.polygon.centroid
        return self.__centroid
    
    @property
    def center_lon(self):
        return self.centroid.x
    
    @property
    def center_lat(self):
        return self.centroid.y
    
    @property
    def circuity(self):
        if self.__circuity is not None:
            return self.__circuity
        if self.Gu == 0:
            return 0
        self.__circuity = ox.stats.circuity_avg(self.Gu)
        return self.__circuity
    
    @property
    def complexity(self):
        return self.road_density * self.entropy

    def save_network_fig(self, filepath):
        if self.Gu == 0:
            return
        opts = {"node_size": 5, "bgcolor": "white", "node_color": "blue", "edge_color": "blue"}
        ox.plot_graph(self.Gu, show=False, save=True, filepath=filepath, **opts)
        plt.clf()
        plt.close()
    
    def save_bearings_fig(self, filepath):
        if self.Gu == 0:
            return
        fig, ax = ox.bearing.plot_orientation(self.Gu, area=False, weight='length')
        plt.savefig(filepath)
        plt.clf()
        plt.close()
    
    def save_map_html(self, filepath):
        try:
            fmap = folium.Map(location=[self.center_lat, self.center_lon], zoom_start=16, control_scale=True)
        except IndexError:
            return
        def add_polygon_to_map(polygon):
            folium.Polygon(
                locations=Swap_xy(polygon).exterior.coords,
                color='red',
                fill=True,
                fill_opacity=0.1
            ).add_to(fmap)

        if self.polygon.type == 'Polygon':
            add_polygon_to_map(self.polygon)
        elif self.polygon.type == 'MultiPolygon':
            for p in self.polygon.geoms:
                add_polygon_to_map(p)
        else:
            raise TypeError('Unexpected geom.type:', self.polygon.type)
        fmap.save(filepath)
