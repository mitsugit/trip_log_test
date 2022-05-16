import folium


def create_map(latitude, longitude):
    ido_keido = []
    ido_keido.append(latitude)
    ido_keido.append(longitude)

    map = folium.Map(location=ido_keido, zoom_start=15)
    folium.Marker(
        location=ido_keido,
        icon=folium.Icon(color='red', icon='star')).add_to(map)
    map = map._repr_html_()

    return map


if __name__ == '__main__':
    map = create_map(35.71688122378675, 140.22492881671042)
    print(map)