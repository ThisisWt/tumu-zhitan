from flask import Flask, request, render_template, jsonify
import osmnx as ox
from geopy.geocoders import Nominatim
import geojson
import folium
import os
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__, static_folder='static')
app.config['SERVER_NAME'] = 'localhost:5002'

# 配置线程池以实现异步处理
executor = ThreadPoolExecutor(max_workers=4)


# 缓存地理编码结果
@lru_cache(maxsize=100)
def cached_geocode(building_name, city_name):
    geolocator = Nominatim(user_agent="osm_id_finder", timeout=10)
    location = geolocator.geocode(f"{building_name}, {city_name}")
    return location


# 缓存建筑物数据
@lru_cache(maxsize=100)
def cached_osm_data(lat, lon, dist=100):
    tags = {'building': True}
    gdf = ox.features_from_point((lat, lon), tags=tags, dist=dist)
    return gdf


@app.route('/')
def app3_home():
    return render_template('model.html')


@app.route('/search', methods=['POST'])
def search():
    building_name = request.form.get('building_name')
    city_name = request.form.get('city_name')
    if not building_name or not city_name:
        return jsonify({'error': 'Please enter both building name and city name.'}), 400

    try:
        location = cached_geocode(building_name, city_name)
        if not location:
            return jsonify({'error': 'Location not found.'}), 404

        future = executor.submit(fetch_building_data, building_name, location.latitude, location.longitude)
        building_data = future.result()

        if 'error' in building_data:
            return jsonify(building_data), 404

        return jsonify({
            'message': 'Map has been generated and opened.',
            'map_url': building_data['map_url']
        })

    except Exception as e:
        return jsonify({'error': f"Error fetching building data: {e}"}), 500


def fetch_building_data(building_name, lat, lon):
    try:
        gdf = cached_osm_data(lat, lon)

        possible_name_columns = ['name', 'name:zh', 'name:zh-Hans', 'name:zh-Hant']
        name_columns = [col for col in possible_name_columns if col in gdf.columns]
        if name_columns:
            filtered_gdf = gdf[
                gdf[name_columns].apply(lambda row: any(building_name in str(name) for name in row.values), axis=1)]
        else:
            filtered_gdf = gdf[gdf['name'].str.contains(building_name, na=False)]

        if filtered_gdf.empty:
            return {'error': f'No building data found for: {building_name}'}

        invalid_columns = [col for col in filtered_gdf.columns if isinstance(filtered_gdf[col].iloc[0], list)]
        filtered_gdf = filtered_gdf.drop(columns=invalid_columns)

        if not os.path.exists('static'):
            os.makedirs('static')

        save_path = os.path.join('static', 'specific_building.geojson')
        filtered_gdf.to_file(save_path, driver="GeoJSON")

        map_file = os.path.join('static', 'map.html')
        m = folium.Map(location=[lat, lon], zoom_start=15)
        with open(save_path, 'r', encoding='utf-8') as f:
            data = geojson.load(f)
            folium.GeoJson(data).add_to(m)
        m.save(map_file)

        return {'map_url': f'/{map_file}'}

    except Exception as e:
        return {'error': f"Error fetching building data: {e}"}


if __name__ == '__main__':
    app.run(debug=True)
