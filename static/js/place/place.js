let current_category = selected_category;
let current_dsitrict = district_obj.district_id;
let page = 2;

document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('#category');
    const cardList = document.querySelector('.card-list');
    const baseUrl = "{% url 'main' %}";

    categories.forEach(button => {
        button.addEventListener('click', function() {
            page = 1;
            console.log(this);
            categories.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const category = this.getAttribute('data-category');
            current_category = category;
            console.log('current_category: ',current_category);
            fetch(`${get_spot_by_category}?district_id=${current_dsitrict}&place_category_cd=${current_category}&page=${page}`, {
                    method: "GET",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"  // 서버가 요청을 AJAX로 인식하게 하는 헤더
                    }
                })
                .then(response => response.json())
                .then(newShops => {
                    console.log("shops :", newShops.place_list);
                    cardList.innerHTML = '';

                    newShops.place_list.forEach(shop => {
                        addMarker(shop.place_lat, shop.place_lon);
                        let newButton = document.createElement('button');
                        newButton.className = 'card';
                        newButton.onclick = function() {
                            location.href = `${review_url}?place_id=${shop.place_id}`;
                        };

                        console.log('place img : ', shop.review_photo);
                        newButton.innerHTML = `
                            <img src="${shop.review_photo}" alt="${shop.name}" onerror="this.onerror=null; this.src='${fallbackImage}';"  >
                            <div class="card-content">
                                <h3>${shop.place_name}</h3>
                            </div>
                            <div class="card-footer">
                                <span>&hearts; ${shop.likes}</span>
                            </div>
                        `;

                        cardList.appendChild(newButton);
                    });
                })
                .catch(error => {
                    console.error('Failed to load category data:', error);
                });
        });
    });
});

// .list-container에 스크롤 이벤트 리스너 추가
document.addEventListener('DOMContentLoaded', function() {
    const listContainer = document.querySelector('#place-list-container');  // 요소 선택
    console.log(listContainer);  // 확인용 로그

    if (listContainer) {
        listContainer.addEventListener('scroll', onScroll);
    } else {
        console.error('Element with ID "place-list-container" not found');
    }

    function onScroll() {
        // list-container의 스크롤이 끝에 도달했을 때
        console.log('scroll');
        if (listContainer.scrollTop + listContainer.clientHeight >= listContainer.scrollHeight - 1) {
            console.log('End of scroll, loading more objects...');
            loadMoreObjects();
        }
    }
});


function loadMoreObjects() {
    fetch(`${get_spot_by_category}?district_id=${current_dsitrict}&place_category_cd=${current_category}&page=${page}`, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"  // 서버가 요청을 AJAX로 인식하게 하는 헤더
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data['place_list'].length > 0) {
            const buttonList = document.querySelector('.card-list');
            const currentPage = page;
            data['place_list'].forEach(function(place, index) {
                const button = document.createElement('button');
                button.className = 'card';
                button.onclick = function() {
                    window.location.href = review_url+`?place_id=${place.place_id}` ;
                };

            // 카드 요소 생성
            const card_img = document.createElement('img');
            card_img.src = ``;
            // 이미지 로드에 실패할 경우 대체 이미지 설정
            card_img.onerror = function() {
                this.onerror = null;  // 무한 반복 방지
                this.src = fallbackImage;  // 대체 이미지 경로
            };

            // 카드 내용 생성
            const cardContent = document.createElement('div');
            cardContent.className = 'card-content';

            // 제목 생성
            const title = document.createElement('h3');
            title.innerHTML = `${place.place_name}`;

            // 푸터 생성
            const footer = document.createElement('div');
            footer.className = 'card-footer';

        
            // 카드 내용에 제목과 푸터 추가
            cardContent.appendChild(title);
            cardContent.appendChild(footer);

          
            // 버튼에 카드 추가
            button.appendChild(card_img);
            button.appendChild(cardContent);

            // 버튼을 리스트에 추가
            buttonList.appendChild(button);
            });

        } else {
            listContainer.removeEventListener('scroll', onScroll);  // 더 이상 로드할 객체가 없을 때 스크롤 이벤트를 제거합니다.
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
    .finally(() => {
        page++;
    });
}