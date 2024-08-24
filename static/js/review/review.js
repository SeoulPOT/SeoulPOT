document.addEventListener('DOMContentLoaded', function() {
    // Naver Map integration
    var mapOptions = {
        center: new naver.maps.LatLng(place_lat, place_lon), // 장소 중심 위치
        zoom: 17
    };

    var map = new naver.maps.Map('map', mapOptions);

    var marker = new naver.maps.Marker({
        position: new naver.maps.LatLng(place_lat, place_lon), // 마커 위치
        map: map,
        icon: marker_img,
    });
});
