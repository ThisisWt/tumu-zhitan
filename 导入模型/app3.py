from flask import Flask, request, render_template, jsonify
import osmnx as ox
from geopy.geocoders import Nominatim
import geojson
import folium
import os

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5002'

@app.route('/')
def app3_home():
    return render_template('model.html')


@app.route('/search', methods=['POST'])
def search():
    building_name = request.form.get('building_name')
    city_name = request.form.get('city_name')
    if not building_name or not city_name:
        return jsonify({'error': 'Please enter both building name and city name.'}), 400

    # 使用地理编码找到建筑物的大致位置
    geolocator = Nominatim(user_agent="osm_id_finder", timeout=10)
    try:
        location = geolocator.geocode(f"{building_name}, {city_name}")
    except Exception as e:
        return jsonify({'error': f"Geocoding error: {e}"}), 500

    if not location:
        return jsonify({'error': 'Location not found.'}), 404

    try:
        # 下载建筑物所在区域的数据
        tags = {'building': True}
        gdf = ox.features_from_point((location.latitude, location.longitude), tags=tags, dist=100)

        # 尝试过滤特定建筑物，使用部分匹配
        possible_name_columns = ['name', 'name:zh', 'name:zh-Hans', 'name:zh-Hant']
        name_columns = [col for col in possible_name_columns if col in gdf.columns]
        if name_columns:
            filtered_gdf = gdf[
                gdf[name_columns].apply(lambda row: any(building_name in str(name) for name in row.values), axis=1)]
        else:
            filtered_gdf = gdf[gdf['name'].str.contains(building_name, na=False)]

        if filtered_gdf.empty:
            return jsonify({'error': f'No building data found for: {building_name}'}), 404

        # 删除包含无效数据类型的列
        invalid_columns = [col for col in filtered_gdf.columns if isinstance(filtered_gdf[col].iloc[0], list)]
        filtered_gdf = filtered_gdf.drop(columns=invalid_columns)

        # 保存为 GeoJSON 文件
        save_path = os.path.join('static', 'specific_building.geojson')
        filtered_gdf.to_file(save_path, driver="GeoJSON")

        # 创建地图并保存为HTML文件
        map_file = os.path.join('static', 'map.html')
        m = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)
        with open(save_path, 'r', encoding='utf-8') as f:
            data = geojson.load(f)
            folium.GeoJson(data).add_to(m)
        m.save(map_file)

        return jsonify({'message': 'Map has been generated and opened.', 'map_url': f'/{map_file}'})

    except Exception as e:
        return jsonify({'error': f"Error fetching building data: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)