import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
from functools import partial
import pyproj
from shapely.ops import transform
from lib.bearing import orientation_entropy
import networkx as nx

# 参考→https://qiita.com/HidKamiya/items/c27c9fe7d8533cfe8a73
def calc_area_from_polygon(polygon):

    def geom_to_area(geom, epsg=3410): # epsg=3410：正積図法
        project = partial( # 関数の入力を部分的に与える．
            pyproj.transform, 
            pyproj.CRS.from_epsg(4326), # WGS84      # ver 2.2.x
            pyproj.CRS.from_epsg(epsg))              # ver 2.2.x
        trans = transform(project, geom) # 座標系変換
        return trans.area # 面積を返す

    def Swap_xy(geom):
        # (x, y) -> (y, x)
        def swap_xy_coords(coords):
            for x, y in coords:
                yield (y, x)

        # if geom.type == 'Polygon':
        def swap_polygon(geom):
            ring = geom.exterior
            shell = type(ring)(list(swap_xy_coords(ring.coords)))
            holes = list(geom.interiors)
            for pos, ring in enumerate(holes):
                holes[pos] = type(ring)(list(swap_xy_coords(ring.coords)))
            return type(geom)(shell, holes)

        # if geom.type == 'MultiPolygon':
        def swap_multipolygon(geom):
            return type(geom)([swap_polygon(part) for part in geom.geoms])

        # Main
        if geom.type == 'Polygon':
            return swap_polygon(geom)
        elif geom.type == 'MultiPolygon':
            return swap_multipolygon(geom)
        else:
            raise TypeError('Unexpected geom.type:', geom.type)


    geom_swap = Swap_xy(polygon)
    area = geom_to_area(geom_swap)
    return area * 1e-6 # m2 -> km2 

def calc_entropy_from_polygon(polygon):

    Gu = get_Gu_from_polygon(polygon)

    # エントロピー計算
    return calc_entropy_from_Gu(Gu)

def calc_entropy_from_Gu(Gu):
    if Gu == 0:
        return 0
    return orientation_entropy(Gu, weight='length')


def calc_road_length_from_Gu(Gu):
    """
    Gu: lengthつきでundirectedのネットワーク
    """
    if Gu == 0:
        return 0
    return sum([data['length'] for u, v, k, data in Gu.edges(keys=True, data=True)])

def calc_total_length_from_polygon(polygon):

    Gu = get_Gu_from_polygon(polygon)

    return calc_road_length_from_Gu(Gu)

def get_Gu_from_polygon(polygon, network_type='bike', simplify=False, retain_all=True):

    # 対象地域の道路情報取得
    try:
        G = ox.graph_from_polygon(polygon, network_type=network_type, simplify=simplify, retain_all=retain_all)
    except ox._errors.EmptyOverpassResponse:
        return 0
    except nx.NetworkXPointlessConcept:
        return 0
    except ValueError:
        return 0

    # bearings情報の付加
    G = ox.add_edge_bearings(G)

    # undirectedに変換
    Gu = ox.utils_graph.get_undirected(G)

    return Gu








