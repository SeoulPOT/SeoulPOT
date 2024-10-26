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

document.addEventListener('DOMContentLoaded', function() {
    // 모달 열기 버튼
    const openAdModalBtn = document.getElementById('openAdModalBtn');
    // 모달 요소
    const adModal = document.getElementById('adModal');
    // 모달 닫기 버튼
    const closeAdModalBtn = document.getElementById('closeAdModalBtn');

    // 모달 열기
    openAdModalBtn.onclick = function() {
        adModal.style.display = 'block';
    }

    // 모달 닫기
    closeAdModalBtn.onclick = function() {
        adModal.style.display = 'none';
    }

    // 모달 영역 밖을 클릭하면 닫기
    window.onclick = function(event) {
        if (event.target == adModal) {
            adModal.style.display = 'none';
        }
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // 모달 열기 버튼
    const opensentModalBtn = document.getElementById('opensentModalBtn');
    // 모달 요소
    const sentModal = document.getElementById('sentModal');
    // 모달 닫기 버튼
    const closesentModalBtn = document.getElementById('closesentModalBtn');

    // 모달 열기
    opensentModalBtn.onclick = function() {
        sentModal.style.display = 'block';
    }

    // 모달 닫기
    closesentModalBtn.onclick = function() {
        sentModal.style.display = 'none';
    }

    // 모달 영역 밖을 클릭하면 닫기
    window.onclick = function(event) {
        if (event.target == sentModal) {
            sentModal.style.display = 'none';
        }
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const aiReviewElement = document.getElementById('openaiModalBtn');
    const originalText = aiReviewElement.textContent;
    // 모달 열기 버튼
    const openaiModalBtn = document.getElementById('openaiModalBtn');
    // 모달 요소
    const aiModal = document.getElementById('aiModal');
    // 모달 상태 확인
    let isModalOpen = false;

    // 텍스트가 15자 이상일 때 자르고 ... 추가
    if (originalText.length > 15) {
        aiReviewElement.textContent = originalText.substring(0, 15) + '...';
    }

    // 모달 열기
    openaiModalBtn.onclick = function() {
        if (isModalOpen) {
            // 모달이 이미 열려 있는 경우 닫기
            aiModal.style.display = 'none';
            document.body.style.overflow = 'auto'; // 모달 닫힐 때 스크롤 다시 활성화
            isModalOpen = false;
        } 
        else {
            // 모달이 닫혀 있는 경우 열기
            aiModal.style.display = 'block';
            document.body.style.overflow = 'hidden'; // 모달 열릴 때 스크롤 방지
            // openaiModalBtn 요소 바로 아래에 모달 위치 지정
            const rect = openaiModalBtn.getBoundingClientRect();
            aiModal.style.top = `${rect.bottom + window.scrollY + 35}px`;
            aiModal.style.left = `${rect.left + window.scrollX + 95}px`;
            isModalOpen = true;
        }
        }


    // 모달 영역 밖을 클릭하면 닫기
    window.onclick = function(event) {
        if (event.target == aiModal) {
            aiModal.style.display = 'none';
        }
    }
    
});