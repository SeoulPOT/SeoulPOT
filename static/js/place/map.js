let map;
document.addEventListener('DOMContentLoaded', function() {
    fetch(window.geojsonUrl)  // JSON 파일의 경로
    .then(response => response.json())  // JSON 데이터를 파싱
    .then(data => {
        // 여기서 데이터를 활용한 작업 수행
        const mapElement = document.getElementById('map');

        let district;

        for (const obj of data['features']) {
            if(district_obj.district_name == obj['properties']['name']){
                district =  obj;
                break;
            }
        }
        console.log("선택 구:", district);
        //district = data['features'][7];
        var polygonPath = district['geometry']['coordinates'];
    
        let sumLat = 0; // 위도 합
        let sumLng = 0; // 경도 합
        let numCoords = 0;

        // LatLngBounds 객체 생성
        var bounds = new naver.maps.LatLngBounds();

        polygonPath[0].forEach(coord => {
            sumLng += coord[0]; // 경도 합산
            sumLat += coord[1]; // 위도 합산
            numCoords++;
            var latlng = new naver.maps.LatLng(coord[1], coord[0]);
            bounds.extend(latlng);
        });

        

        // var naver_polygonPath =district['geometry']['coordinates'][0].map(coord => {
        //     return new naver.maps.LatLng(coord[1], coord[0]); // GeoJSON은 [경도, 위도] 순이므로 [위도, 경도]로 변환
        // });
        
        let centerLng = sumLng / numCoords; // 경도 평균
        let centerLat = sumLat / numCoords; // 위도 평균

        let center = [centerLng, centerLat]; // 중심 좌표

        console.log("Center Coordinates:", center);
        console.log('district:' ,district_obj );
        

        map = new naver.maps.Map(document.getElementById('map'), {
            // center: new naver.maps.LatLng(center[1], center[0]),
            center: new naver.maps.LatLng(district_obj.district_lat, district_obj.district_lon),
  
        });
        
        map.fitBounds(bounds);
        
        

        naver.maps.Event.once(map, 'init', function(e) {
            map.data.setStyle(function(feature) {
                var mantle_properties = feature.geometryCollection[0].getRaw().mantle_properties;
                console.log("mantle_properties : ", mantle_properties);
                var styleOptions = {
                    ...mantle_properties,
                };
                if (feature.getProperty('focus')) {
                    styleOptions.fillOpacity = 0.6;
                    styleOptions.fillColor = '#D4CBF8';
                    styleOptions.strokeColor = '#D4CBF8';
                    styleOptions.strokeWeight = 2;
                    styleOptions.strokeOpacity = 1;
                }
                return styleOptions;
            });
        
            map.data.addGeoJson(district, true);
        
            map.data.addListener('click', function(e) {
                var feature = e.feature;
        
                if (feature.getProperty('focus') !== true) {
                    feature.setProperty('focus', true);
                } else {
                    feature.setProperty('focus', false);
                }
            });
        
            map.data.addListener('mouseover', function(e) {
                var feature = e.feature;
                map.data.overrideStyle(feature, {
                    fillOpacity: 1,
                    strokeWeight: 10,
                    strokeOpacity: 1
                });
            });
        
            map.data.addListener('mouseout', function(e) {
                map.data.revertStyle();
            });
        });


        

    })
    .catch(error => console.error('Error loading JSON:', error));
    
    
});

function addMarker(lat, lon, place_name, place_desc){
    var infoDiv = document.getElementById('info');
    
    // 마커를 생성하고 지도에 추가
    var marker = new naver.maps.Marker({
        position: new naver.maps.LatLng(lat, lon), // 마커의 위치 (서울)
        map: map, // 마커를 추가할 지도 객체
        icon: markerImage,
        
    });
    let infowindow = createInfoWindow( place_name, place_desc);
    
    naver.maps.Event.addListener(marker, "mouseover", function(e) {
         infowindow.open(map, marker);        
    });

    // 마우스 아웃 시 infoDiv 숨기기
    naver.maps.Event.addListener(marker, 'mouseout', function() {
        infowindow.close();
    });

    naver.maps.Event.addListener(marker, "click", function() {
        // 현재 아이콘이 기본 아이콘인지 확인하고, 클릭된 아이콘으로 변경
        // if (marker.icon === markerImage) {
        //     marker.setIcon(clicked_markerImage);
        // } else {
        //     marker.setIcon(markerImage);
        // }
    });

    return marker;
}

function createInfoWindow(place_name, place_desc)
{
    // 핀 요소
    var infoWindowElement = `
        <<div class="custom-infowindow">
                <h3>${place_name}</h3>
                <p>${place_desc}</p>
            </div>
        `;

    var infowindow = new naver.maps.InfoWindow({
        content: infoWindowElement,
    
        
        borderWidth: 0,
        disableAnchor: false,
        backgroundColor: 'white',
        anchorSize: new naver.maps.Size(20, 2), // 앵커 크기를 작게 설정
        anchorSkew: true,
        anchorColor: "white",
    
    
        pixelOffset: new naver.maps.Point(0, -10),
    });
    return infowindow;   
}

function clearMarkers(markers){
    console.log('markers : ', markers);
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    
    // 배열 비우기 (선택 사항)
    markers = [];
}