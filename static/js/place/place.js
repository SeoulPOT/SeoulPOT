let current_category = selected_category;
let current_dsitrict = district_obj.district_id;
let current_sortBy = selected_sortBy
let pre_sortBy = selected_sortBy
let serach_text = ""
let cardList;
let page_container;
let markers= [];
let bookmark_buttons = [];
let bookmark_markers = [];
document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('#category');
    const sorting_container = document.querySelectorAll('.sorting-btn');
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
    SetCategoryActive(current_category, categories, sorting_container);

    //소팅 버튼 구현
    SetSortingActive(current_sortBy, categories, sorting_container);

    function SetCategoryActive(category, category_container, sorting_container){
        console.log("category_container:",category_container);
        
        category_container.forEach(btn => { 
            console.log("data-value:", btn.getAttribute('data-category'));
            if(btn.getAttribute('data-category') == category )
                btn.classList.add('active'); 
            else
                btn.classList.remove('active');
        });
        
        category_container.forEach(button => {
            button.addEventListener('click', function() {
    
                if(this.getAttribute('data-category') != 'bookmark'){
                    document.querySelectorAll('.sorting-div')[0].style.visibility = 'visible'
                    page = 1;
                    category_container.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    const category = this.getAttribute('data-category');
                    current_category = category;
    
                    cardList.innerHTML = '';
                    clearMarkers(markers);
                    loadMoreObjects(page);
                }
                // 즐겨찾기
                else{
                    document.querySelectorAll('.sorting-div')[0].style.visibility  = 'hidden'
                    page = 1;
                    category_container.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    const category = this.getAttribute('data-category');
                    current_category = category;
    
                    cardList.innerHTML = '';
                    clearMarkers(markers);
                    loadBookmarkObjects();
    
                }
            });
        });
    }
    
    function SetSortingActive(sortBy, category_container, sorting_container){
        console.log("sorting_container:",sorting_container);
        
        sorting_container.forEach(btn => { 
            console.log("data-sortBy:", btn.getAttribute('data-sortBy'));
            if(btn.getAttribute('data-sortBy') == sortBy )
                btn.classList.add('active'); 
            else
                btn.classList.remove('active');
        });
    
        const search_input = document.querySelector('#search-input');

        // 키 입력 이벤트 리스너 추가
        search_input.addEventListener("keydown", function(event) {
            // "Enter" 키인지 확인
            if (event.key === "Enter") {
                event.preventDefault(); // 기본 동작 막기 (필요에 따라)
                // 실행하고 싶은 동작
                console.log("Enter key pressed!");
                // 여기서 원하는 함수를 호출하거나 동작을 수행하세요
                page = 1;
                
                current_sortBy = "-1"
                serach_text = search_input.value;
                console.log('current_sortBy:',current_sortBy);
                
                
    
                cardList.innerHTML = '';
                clearMarkers(markers);
                loadMoreObjects();
            }
        });
    
        sorting_container.forEach(button => {
            button.addEventListener('click', function() {
            
                page = 1;
                sorting_container.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                const sortBy = this.getAttribute('data-sortBy');
                current_sortBy = sortBy;
                console.log('current_sortBy:',current_sortBy);
                if(current_sortBy == "-1")
                    serach_text = search_input.value;
                else
                    serach_text = "";
    
                cardList.innerHTML = '';
                clearMarkers(markers);
                loadMoreObjects();
    
            });
        });
    
        const toggle_btn = document.querySelector('#sorting-toggle_btn');
        const button_div = document.querySelector("#sorting-button-div"); // 단일 요소 선택
        const search_div = document.querySelector("#sorting-search-div"); // 단일 요소 선택
    
        const toggle_btn_img = toggle_btn.querySelector('img'); // 버튼 내부의 이미지 요소 선택
        toggle_btn.addEventListener('click', function() {
            // button_div의 display가 'none'이면 search_div를 'none'으로 설정하고 아니라면 토글
            if (search_div.style.display === 'none' || search_div.style.display === '') {
                search_div.style.display = 'flex';
                // 리플로우를 강제하여 애니메이션이 적용되도록 함
                void search_div.offsetWidth;
                search_div.classList.add('active');
                button_div.style.display = 'none';

                toggle_btn_img.setAttribute('src', close_img);     

                pre_sortBy = current_sortBy
                
            } else {
                //닫기 버튼을 클릭
                search_div.style.display = 'none';
                search_div.classList.remove('active');
                button_div.style.display = 'block';
        
                toggle_btn_img.setAttribute('src', search_img);
            
                //검색 텍스트 삭제
                search_input.value = '';


                if(current_sortBy != pre_sortBy)
                {
                    current_sortBy = pre_sortBy;
                    cardList.innerHTML = '';
                    clearMarkers(markers);
                    loadMoreObjects();
                }
            }
        });
    }
    
});

function loadMoreObjects(page) {
    fetch(`${get_spot_by_category}?district_id=${current_dsitrict}&place_category_cd=${current_category}&sortBy=${current_sortBy}&search_text=${serach_text}&page=${page}&place_thema_cd=${place_thema_cd}`, {
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
                    card_img.classList.add('place-img'); // 클래스 추가

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
                    if(lang == 'kor'){
                        footer.innerHTML = `📝 리뷰 ${place.place_review_num}개`;
                    }
                    else{
                        footer.innerHTML = `📝 ${place.place_review_num} reviews`;
                    }

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
        console.log('remove marker : ', marker)
        console.log('remove marker id : ', marker.map.id)
        console.log('bookmark_markers: ', bookmark_markers)
        const markerIndex = bookmark_markers.findIndex(m => m === marker);
        console.log('bookmark_marker index: ', markerIndex)
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
    // console.log('find button:', button);
    // console.log('bookmark_buttons:', bookmark_buttons);
    return button;
}

function updateButtonContent(button, place) {
    // 필요한 경우 버튼의 내용을 업데이트
    // 예: 장소 이름, 주소 등 변경 가능한 정보 업데이트
}
