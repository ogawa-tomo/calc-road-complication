from lib.calc_area_stats import *
from lib.bearing import orientation_entropy

class District(object):

    def __init__(self, pref, city, district, area, polygon) -> None:
        self.__pref = pref
        self.__city = city
        self.__district = district
        self.__area = area
        # self.__polygon = polygon
        self.__polygon = polygon.buffer(-0.0001)  # バッファをとる
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
        self.__Gu = get_Gu_from_polygon(self.polygon)
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




    
    
    

    
        
        
