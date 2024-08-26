let current_category = selected_category;
let current_dsitrict = district_obj.district_id;
let cardList;
let page_container;
let markers= [];
// let page = 2;

document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('#category');
    cardList = document.querySelector('.card-list');
    page_container = document.getElementById('page_container');

    //Init
    cardList.innerHTML = '';
    
    clearMarkers(markers);
    loadMoreObjects(1);
    SetPagination(current_page, total_pages);
    SetCategoryActive(current_category);

    categories.forEach(button => {
        button.addEventListener('click', function() {
            page = 1;
            categories.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const category = this.getAttribute('data-category');
            current_category = category;

            cardList.innerHTML = '';
            clearMarkers(markers);
            loadMoreObjects();


            // console.log('current_category: ',current_category);
            // fetch(`${get_spot_by_category}?district_id=${current_dsitrict}&place_category_cd=${current_category}&page=${page}`, {
            //         method: "GET",
            //         headers: {
            //             "X-Requested-With": "XMLHttpRequest"  // 서버가 요청을 AJAX로 인식하게 하는 헤더
            //         }
            //     })
            //     .then(response => response.json())
            //     .then(data => {
            //         console.log("data :", data);
            //         cardList.innerHTML = '';
            //         SetPagination(data.current_page, data.total_pages);

            //         newShops = data.place_list;

            //         newShops.place_list.forEach(shop => {
            //             markers.push(addMarker(shop.place_lat, shop.place_lon));
            //             let newButton = document.createElement('button');
            //             newButton.className = 'card';
            //             newButton.onclick = function() {
            //                 location.href = `${review_url}?place_id=${shop.place_id}`;
            //             };

            //             console.log('place img : ', shop.review_photo);
            //             newButton.innerHTML = `
            //                 <img src="${shop.review_photo}" alt="${shop.name}" onerror="this.onerror=null; this.src='${fallbackImage}';"  >
            //                 <div class="card-content">
            //                     <h3>${shop.place_name}</h3>
            //                 </div>
            //                 <div class="card-footer">
            //                     <span>&hearts; ${shop.likes}</span>
            //                 </div>
            //             `;

            //             cardList.appendChild(newButton);
            //         });
            //     })
            //     .catch(error => {
            //         console.error('Failed to load category data:', error);
            //     });
        });
    });
});

// .list-container에 스크롤 이벤트 리스너 추가
// document.addEventListener('DOMContentLoaded', function() {
//     const listContainer = document.querySelector('#place-list-container');  // 요소 선택
//     console.log(listContainer);  // 확인용 로그

//     if (listContainer) {
//         listContainer.addEventListener('scroll', onScroll);
//     } else {
//         console.error('Element with ID "place-list-container" not found');
//     }

//     function onScroll() {
//         // list-container의 스크롤이 끝에 도달했을 때
//         console.log('scroll');
//         if (listContainer.scrollTop + listContainer.clientHeight >= listContainer.scrollHeight - 1) {
//             console.log('End of scroll, loading more objects...');
//             loadMoreObjects();
//         }
//     }
// });


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
                markers.push(addMarker(place.place_lat, place.place_lon));

                const button = document.createElement('button');
                button.className = 'card';
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

        } 
        // else {
        //     listContainer.removeEventListener('scroll', onScroll);  // 더 이상 로드할 객체가 없을 때 스크롤 이벤트를 제거합니다.
        // }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
    .finally(() => {
        //page++;
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

function movePage(page) {
    clearMarkers(markers);
    cardList.innerHTML = '';
    loadMoreObjects(page);
}

function SetCategoryActive(category, category_container){
    // category_container.forEach(btn => { 
    //     if(btn.getAttribute('data-value') == category )
    //         btn.classList.add('active'); 
    //     else
    //         btn.classList.remove('active');
    // });
}