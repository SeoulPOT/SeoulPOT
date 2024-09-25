let review_container;
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
    
    review_container =  document.getElementById('review_container');
    console.log('review_container:',review_container);
});

document.addEventListener('DOMContentLoaded', function() {
    initModalEvents();
});

function SetReviews(reviews) {
    // review_container가 배열이나 HTMLCollection이라고 가정
    review_container.innerHTML = '';
    reviewsData = reviews;
    renderReviews();  // 저장된 리뷰 데이터를 렌더링
    initModalEvents();  // 페이지 렌더링 후 모달 이벤트 다시 설정
    reviews.forEach(function(review) {
            // 카드 요소 생성
            var cardElement = document.createElement('div');
            cardElement.className = 'card';
        
            // 이미지 요소 생성
            var imgElement = document.createElement('img');
            imgElement.src = review.review_photo;
            imgElement.alt = 'Review Photo';
            imgElement.onerror = function() {
                this.onerror = null;
                this.src = '/static/img/default1.png';
            };
        
            // 카드 콘텐츠 요소 생성
            var cardContentElement = document.createElement('div');
            cardContentElement.className = 'card-content';
        
            // 날짜 요소 생성
            var dateElement = document.createElement('p');
            dateElement.className = 'card-date';
            // dateElement.textContent = formatDate(review.review_date);
            cardContentElement.appendChild(dateElement);
            
            console.log(review);
            // 데일리 태그 요소 생성 (존재하는 경우)
            if (review.daily_tag_name) {
                var dailyTagElement = document.createElement('p');
                dailyTagElement.className = 'card-daily';
                dailyTagElement.textContent = '데일리 태그: ' + review.daily_tag_name;
                cardContentElement.appendChild(dailyTagElement);
            }
        
            // 위드 태그 요소 생성 (존재하는 경우)
            if (review.with_tag_name) {
                var withTagElement = document.createElement('p');
                withTagElement.className = 'card-with';
                withTagElement.textContent = '위드 태그: ' + review.with_tag_name;
                cardContentElement.appendChild(withTagElement);
            }
        
            // 리뷰 텍스트 요소 생성
            var descriptionElement = document.createElement('p');
            descriptionElement.className = 'card-description';
            descriptionElement.textContent = review.review_text;
        
            // 각 요소를 카드 콘텐츠에 추가
            
            cardContentElement.appendChild(descriptionElement);
        
            // 이미지와 카드 콘텐츠를 카드에 추가
            cardElement.appendChild(imgElement);
            cardElement.appendChild(cardContentElement);
        
            
            // 카드 요소를 리뷰 컨테이너에 추가
            review_container.appendChild(cardElement);
        
    });
}


function setSortOption(array) {
    console.log(array);
    console.log(sort_array);
    sort_array = array;
    movePage(1, array);
}

// //데이트 양식 변경 함수
// function formatDate(inputDate) {
//     const date = new Date(inputDate);  // "2024-04-19" 형식의 문자열을 Date 객체로 변환
//     const options = { month: 'short', day: 'numeric', year: 'numeric' };
//     return date.toLocaleDateString('en-US', options).replace(',', '').replace(/(\d{1,2}) /, '$1.');
// }


// 모달 열기
function openModal(imageSrc) {
    const modal = document.getElementById('modalContainer');
    const modalImage = document.getElementById('modalImage');
    modalImage.src = imageSrc;
    modal.style.display = 'flex'; // 모달창을 화면에 표시
}

// 모달 닫기
function closeModal() {
    const modal = document.getElementById('modalContainer');
    modal.style.display = 'none'; // 모달창을 숨김
}

