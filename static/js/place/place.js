let current_category = selected_category;
let current_dsitrict = district_obj.district_id;
let cardList;
let page_container;
let markers= [];
let bookmark_buttons = [];
let bookmark_markers = [];
document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('#category');
    cardList = document.querySelector('.card-list');
    page_container = document.getElementById('page_container');

    //Init cardList
    cardList.innerHTML = '';
    
    clearMarkers(markers);

    //가게 리스트 호출
    loadMoreObjects(1);

    //페이지 버튼 구현
    SetPagination(current_page, total_pages);

    //카테고리 버튼 구현
    SetCategoryActive(current_category, categories);

    categories.forEach(button => {
        button.addEventListener('click', function() {

            if(this.getAttribute('data-category') != 'bookmark'){
                page = 1;
                categories.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                const category = this.getAttribute('data-category');
                current_category = category;

                cardList.innerHTML = '';
                clearMarkers(markers);
                loadMoreObjects();
            }
            else{
                page = 1;
                categories.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                const category = this.getAttribute('data-category');
                current_category = category;

                cardList.innerHTML = '';
                clearMarkers(markers);
                loadBookmarkObjects();

            }
        });
    });
});

function loadMoreObjects(page) {
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
        SetPagination(data.current_page, data.total_pages);
        if (data['place_list'].length > 0) {
            const buttonList = document.querySelector('.card-list');
            const currentPage = page;
            data['place_list'].forEach(function(place, index) {

                let button;
                const existingButton = findExistingButton(place.place_id);
            
                if (existingButton) {
                    // 기존 버튼이 있다면 그것을 사용
                    button = existingButton;
                    // 필요하다면 버튼 내용 업데이트
                    updateButtonContent(button, place);
                }
                else{
                    const place_marker = addMarker(place);
                    markers.push(place_marker);

                    button = document.createElement('button');
                    button.className = 'card';
                    button.dataset.placeId = place.place_id;
                    button.onclick = function() {
                        window.location.href = review_url+`?place_id=${place.place_id}` ;
                    };

                    // 카드 요소 생성
                    const card_img = document.createElement('img');
                    card_img.src = place.review_photo;
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
                    
                    const category = document.createElement('div');
                    category.className = 'card-category';
                    category.innerHTML = `${place.place_tag_name}`;


                    // 푸터 생성
                    const footer = document.createElement('div');
                    footer.className = 'card-footer';
                    footer.innerHTML = `📝 리뷰 ${place.place_review_num}개`;

                    const bookmark= document.createElement('img');
                    bookmark.src = bookmark_not_check_img;
                    bookmark.width = 25;
                    bookmark.height = 25;
                    bookmark.style.cursor = 'pointer'; // 호버 시 커서를 포인터로 변경
                    bookmark.classList.add('bookmark-icon'); // 클래스 추가
                    // 클릭 이벤트 리스너 추가
                    bookmark.addEventListener('click', function(event) {
                        event.stopPropagation(); // 버블링 방지
                        toggleBookmark(place.place_id, place_marker, button,  this ); // 북마크 토글 함수 호출
                    });


                    cardContent.appendChild(title);
                    cardContent.appendChild(category);
                    cardContent.appendChild(footer);
                
                    button.appendChild(card_img);
                    button.appendChild(cardContent);
                    button.appendChild(bookmark);
                    // 버튼을 리스트에 추가
                }
                buttonList.appendChild(button);
            });

        } 
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
    .finally(() => {
        //page++;
    });
}

function loadBookmarkObjects(){
    const buttonList = document.querySelector('.card-list');

    bookmark_buttons.forEach(button => {
        console.log('button:', button);
        buttonList.appendChild(button);
    });

    SetPagination(1,1);
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
        let newButton2 = document.createElement('button');
        newButton2.className = 'page-button';
        newButton2.onclick = function() { movePage((page_group_index+1)*5+1) };
        newButton2.innerHTML = '다음 &raquo';
        page_container.appendChild(newButton2);
    }
}

function movePage(page) {
    clearMarkers(markers);
    cardList.innerHTML = '';
    loadMoreObjects(page);
}

function SetCategoryActive(category, category_container){
    console.log("category_container:",category_container);
    
    category_container.forEach(btn => { 
        console.log("data-value:", btn.getAttribute('data-category'));
        if(btn.getAttribute('data-category') == category )
            btn.classList.add('active'); 
        else
            btn.classList.remove('active');
    });
}

// 북마크 토글 함수
function toggleBookmark(placeId, marker, button, imgElement) {
    // 여기에 북마크 상태를 토글하는 로직 추가
    // 예: API 호출, 로컬 상태 변경 등
    const buttonList = document.querySelector('.card-list');
    console.log('북마크 토글:', placeId);
    console.log('button:', button);

    const currentImageName = imgElement.src.split('/').pop();
    const notCheckImageName = bookmark_not_check_img.split('/').pop();
    
    // 파일 이름 비교
    if (currentImageName === notCheckImageName) {
        imgElement.src = bookmark_img;
        changeMarker(marker, true);
        bookmark_buttons.push(button);
        bookmark_markers.push(marker);
    } else {
        imgElement.src = bookmark_not_check_img;
        changeMarker(marker, false);
        
        // bookmark_buttons 배열에서 버튼 제거
        const buttonIndex = bookmark_buttons.indexOf(button);
        if (buttonIndex > -1) {
            bookmark_buttons.splice(buttonIndex, 1);
        }
        
        // bookmark_markers 배열에서 marker 제거
        const markerIndex = bookmark_markers.findIndex(m => m.id === marker.id);
        if (markerIndex > -1) {
            bookmark_markers.splice(markerIndex, 1);
        }

        // 현재 표시된 카테고리가 '즐겨찾기'인 경우에만 카드를 삭제
        const currentCategory = document.querySelector('#category.active').dataset.category;
        if (currentCategory === 'bookmark') {
            // 카드 리스트에서 해당 버튼(카드) 제거
            buttonList.removeChild(button);
            clearMarker(marker);
        }
    }
    console.log('bookmark_buttons:', bookmark_buttons);
}

// 기존 버튼 찾기 함수
function findExistingButton(placeId) {
    button = bookmark_buttons.find(button => button.dataset.placeId == placeId);
    console.log('find button:', button);
    console.log('bookmark_buttons:', bookmark_buttons);
    return button;
}

function updateButtonContent(button, place) {
    // 필요한 경우 버튼의 내용을 업데이트
    // 예: 장소 이름, 주소 등 변경 가능한 정보 업데이트
}
