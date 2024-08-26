let page_container;
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
    
    
    page_container = document.getElementById('page_container');
    review_container =  document.getElementById('review_container');
    console.log('review_container:',review_container);

    SetPagination(current_page, total_pages);
});

function toggleFeature() {
    var moreFeature = document.getElementById('more-feature');
    var toggleButton = document.getElementById('toggle-button');
    
    if (moreFeature.style.display === "none") {
        moreFeature.style.display = "block";
        toggleButton.textContent = "-"; // 버튼 텍스트를 "v"로 변경
    } else {
        moreFeature.style.display = "none";
        toggleButton.textContent = "+"; // 버튼 텍스트를 "^"로 변경
    }
}

function movePage(page, array) {
    fetch(`?place_id=${place_id}&page=${page}&array=${array}`, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"  // 서버가 요청을 AJAX로 인식하게 하는 헤더
        }
    })
    .then(Response => Response.json())
    .then(data => {
        console.log("nextReview: ", data);
        SetPagination(data.current_page, data.total_pages);
        SetReviews(data.reviews);   
    })
    .catch(error => {
        console.error('Failed to load review data:', error);
    });
}

function SetPagination(current_page, total_page)
{
    console.log("current_page", current_page);
    page_container.innerHTML = '';

    current_page -= 1;
    page_group_index = Math.floor(current_page / 5);
    page_group_page_index = current_page % 5 ; 
    total_group_index = Math.floor(total_page / 5);
    total_group_page_index = total_page % 5 ; 

    if(page_group_index != 0){
        let newButton1 = document.createElement('button');
        newButton1.className = 'page-button';
        newButton1.onclick = function() { movePage((page_group_index-1)*5+1) };
        newButton1.innerHTML = '&laquo; 이전';
        page_container.appendChild(newButton1);

        // let newButton2 = document.createElement('button');
        // newButton2.className = 'page-button';
        // newButton2.onclick = function() { movePage(current_page-1) };
        // newButton2.innerHTML = '이전';
        // page_container.appendChild(newButton2);
    }

    for (let i = 1; i <= 5 && ((page_group_index)*5+i) <= total_page; i++) {
        let newButton1 = document.createElement('button');
        newButton1.className = 'page-button';
        newButton1.onclick = function() { movePage((page_group_index)*5+i) };
        newButton1.innerHTML = `${(page_group_index)*5+i}`;
        
        console.log(`${current_page} ${i-1} ${page_group_page_index}`);
        if( i-1 == page_group_page_index ){
            newButton1.classList.add('active');
        }
        
        page_container.appendChild(newButton1);
        
    }

    if(page_group_index != total_group_index){
        // let newButton1 = document.createElement('button');
        // newButton1.className = 'page-button';
        // newButton1.onclick = function() { movePage(current_page+1) };
        // newButton1.innerHTML = '다음';
        // page_container.appendChild(newButton1);

        let newButton2 = document.createElement('button');
        newButton2.className = 'page-button';
        newButton2.onclick = function() { movePage((page_group_index+1)*5+1) };
        newButton2.innerHTML = '다음 &raquo';
        page_container.appendChild(newButton2);
    }
}

function SetReviews(reviews) {
    // review_container가 배열이나 HTMLCollection이라고 가정
    review_container.innerHTML = '';

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
            dateElement.textContent = review.review_date;
        
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
            cardContentElement.appendChild(dateElement);
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
