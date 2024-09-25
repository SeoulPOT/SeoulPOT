let is_selected = false;
let selected_obj;
let current_district;
let current_category;
document.addEventListener('DOMContentLoaded', function() {
    function updateMap() {
        const width = document.getElementById('map').clientWidth;
        const height = document.getElementById('map').clientHeight;

        document.documentElement.style.setProperty('--map-width', `${width}px`);
        document.documentElement.style.setProperty('--map-height', `${height}px`);

        if (window.innerWidth <= 600){
            scale = 40000
        }
        else if (window.innerWidth <= 1200){
            scale = 70000
        }
        else {
            scale = 80000
        }

        const seoul_center = [126.978, 37.566];

        const projection = d3.geoMercator()
            .center(seoul_center)
            .scale(scale)
            .translate([width / 2, height / 2]);

        const path = d3.geoPath().projection(projection);

        let svg = d3.select('#map').select('svg');
        if (svg.empty()) {
            svg = d3.select('#map').append('svg')
                .attr('width', width)
                .attr('height', height);
        } else {
            svg.attr('width', width)
                .attr('height', height);
        }

        d3.json(window.geojsonUrl).then(function(geojsonData) {
            const paths = svg.selectAll('path')
                .data(geojsonData.features, d => d.id); 

                paths.enter().append('path')
                .attr('d', path)
                .attr('class', 'district')
                .on('mouseover', function(event, d) {
                    const centroid = path.centroid(d);
    
                    d3.select(this).raise()
                        .classed('active', true)
                        .style('transform-origin', `${centroid[0]}px ${centroid[1]}px`);
    
                        
                    if(selected_obj == undefined){
                        document.getElementById('district-name').innerText = d.properties.name;                    
                        document.getElementById('none_select-info-container').style.display = 'none';
                        document.getElementById('district-container').style.display = 'none';
                        document.getElementById('district-info-container').style.display = 'flex';
                        document.getElementById('district-comming-soon').style.display = 'none';
                    }
                    
                    // 조건을 만족하는 객체가 있으면 출력
                    var foundItem = districts_list.find(function(item) {
                        return item.district_name_kor === d.properties.name;
                    });

                    if (foundItem) {

                        if(selected_obj == undefined){
                            if (selected_lang == 'kor'){
                                document.getElementById('district-name').innerText = foundItem.district_name_kor;      
                            }
                            else{
                                document.getElementById('district-name').innerText = foundItem.district_name;      
                            }
                        }


                        img_path = staticPath+`/${foundItem.district_name_kor}.png`;
                        console.log('img_path : ', fallbackImage);
                        console.log('img_path : ', img_path);

                        let splitArray = foundItem.district_desc.split('|');

                        document.getElementById('selected-district-desc').innerText = splitArray[0];
                        document.getElementById('selected-district-img').src = img_path;
                        document.getElementById('selected-district-img').onerror = function() {
                            this.onerror = null;
                            this.src = '/static/img/default1.png';
                        };
                        subway_container = document.getElementById('seleceted-district-subway');
                        createDistrictDiv(subway_container, splitArray[1])
                        
                    } else {
                        console.log(`name이 ${d.properties.name} 같은 객체를 찾을 수 없습니다.`);
                    }

                })
                .on('mouseout', function(event, d) {
                    const centroid = path.centroid(d);
                    d3.select(this)
                        .classed('active', false)
                        .style('transform-origin', `${centroid[0]}px ${centroid[1]}px`);
                    
                    if(selected_obj == undefined){
                        document.getElementById('none_select-info-container').style.display = 'none'; // flex
                        document.getElementById('district-container').style.display = 'none';
                        document.getElementById('district-info-container').style.display = 'flex'; // none
                        document.getElementById('district-comming-soon').style.display = 'none';
                        document.getElementById('district-name').innerText = 'ㅤ';
                    }


                })
                .on('click', function(event, d) {
                    console.log('seleced_distict :', selected_obj);
                    d3.select(selected_obj).classed('clicked', false);

                    if(selected_obj == this){
                        selected_obj = undefined;
                        document.getElementById('none_select-info-container').style.display = 'none';
                        document.getElementById('district-container').style.display = 'none';           //가게 리스트 출력
                        document.getElementById('district-info-container').style.display = 'flex';
                        document.getElementById('district-comming-soon').style.display = 'none';
                    }
                    else{
                        selected_obj = this;
                        is_selected = true;
                        console.log('selected_obj',selected_obj);
                        d3.select(this).classed('clicked', true);
    
                        document.getElementById('district-name').innerText = d.properties.name;
                        
                        is_selected = true;
                        if(['강남구', '마포구', '중구', '용산구', '종로구'].includes(d.properties.name)){
                            document.getElementById('none_select-info-container').style.display = 'none';
                            document.getElementById('district-container').style.display = 'flex';
                            document.getElementById('district-info-container').style.display = 'none';
                            document.getElementById('district-comming-soon').style.display = 'none';
                        }
                        else{
                            document.getElementById('none_select-info-container').style.display = 'none';
                            document.getElementById('district-container').style.display = 'none';
                            document.getElementById('district-info-container').style.display = 'none';
                            document.getElementById('district-comming-soon').style.display = 'flex';
                        }
                        var foundItem = districts_list.find(function(item) {
                            return item.district_name_kor === d.properties.name;
                        });
    
                        if (foundItem) {

                            if (selected_lang == 'kor'){
                                document.getElementById('district-name').innerText = foundItem.district_name_kor;      
                            }
                            else{
                                document.getElementById('district-name').innerText = foundItem.district_name;      
                            }
                            
                            console.log('click district : ', foundItem);
                            current_district = foundItem.district_id;
                            category_code = current_category ? current_category : categories_list[0].code;
                            
                            fetchData(category_code);
                        }
                    }
                });

            paths.attr('d', path)
                .exit().remove();
        }).catch(function(error) {
            console.error('Error loading GeoJSON:', error);
        });
    }

    updateMap();

    window.addEventListener('resize', updateMap);
});


function createDistrictDiv(subway_container, place_info) {
    // subway_container 초기화
    subway_container.innerHTML = '';

    places = place_info.split('\\');

    for(let place of places){

        let place_info = place.split('-');
        

        // <div id="seleceted-district-subway-img-container"></div>
        const div = document.createElement('div');
        div.classList.add('seleceted-district-subway-img-container');
    
        // <img id="seleceted-district-subway-marker" src="{% static 'img/marker_img.png' %}" alt="marker"></img>
        const img_marker = document.createElement('img');
        img_marker.src = `/static/img/spot.png`;
        img_marker.alt = `마커 이미지`;
        img_marker.id = 'seleceted-district-subway-marker';       
        
        const img_marker_text = document.createElement('span');
        img_marker_text.textContent = place_info[0];
        img_marker_text.classList.add('seleceted-district-subway-marker-text');

        div.appendChild(img_marker);
        div.appendChild(img_marker_text);

        // <img id="seleceted-district-subway-img" src="{% static 'img/subway/서울대입구.png' %}" alt="subway"></img>
        console.log('place_info : ', place_info);
        let subway_info = place_info[1].split(',');
        console.log('subway_info : ', subway_info);
        for(let subway of subway_info){
            const img_subway = document.createElement('img');
            img_subway.src = `/static/img/subway/${subway}.png`;
            img_subway.alt = `${subway} 이미지`;
            img_subway.id = 'seleceted-district-subway-img';
            div.appendChild(img_subway);
        }

        subway_container.appendChild(div);
    }
}

function createStoreItem(store) {
    const div = document.createElement('div');
    div.classList.add('space-box');
    console.log('store : ', store);

    const img = document.createElement('img');
    img.src = store.review_photo;
    img.alt = store.place_name;

    img.onerror = function() {
        this.onerror = null;
        this.src = fallbackImage;
    };
    
    const details = document.createElement('div');
    details.classList.add('details');
    
    const name = document.createElement('h3');
    name.textContent = `${store.place_name}`;
    name.id = 'place-name';

    const tag = document.createElement('p');
    
    tag.textContent = `${store.place_tag_name}`;
    tag.id = 'place-tag';

    const reviews = document.createElement('p');
    if (selected_lang == 'kor'){
        reviews.textContent = `📝 리뷰 ${store.place_review_num}개`;
    }
    else{
        reviews.textContent = `📝 ${store.place_review_num} reviews`;
    }
    reviews.id = 'place-reviews';
    
    details.appendChild(name);
    details.appendChild(tag);
    details.appendChild(reviews);
    
    div.appendChild(img);
    div.appendChild(details);

    div.onclick = function() {
        window.location.href = `/review/${selected_lang}?place_id=${store.place_id}`;
    };
    
    return div;
}

///////////////////////////////////////////////////////////////////////////////////////


function fetchData(category) {
    current_category = category;

    category_container = document.querySelectorAll('#district-category > button');
    category_container.forEach(btn => { 
        console.log('btn : ' , btn);
        console.log('data-value:', btn.getAttribute('data-value'));
        if(btn.getAttribute('data-value') == current_category )
            btn.classList.add('active'); 
        else
            btn.classList.remove('active');
    });
            
    console.log('current_district : ', current_district);
    console.log('current_category : ', current_category);   
    path = `${current_district}/${current_category}`;
    console.log('path : ', path);
    
    fetch(`${current_district}/${current_category}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("data : " , data.data);
        DisplayData(data.data);
    })
    .catch(error => console.log(error));
}

function DisplayData(data) {
    const spaceBoxes = document.querySelectorAll('#district-space #space-container');
    ResetData();
    if(data.length>0){
        
        spaceBoxes.forEach((box, index) => {
            if (data[index]) {
                box.innerHTML = ''; // Clear existing content
                box.appendChild(createStoreItem(data[index]));
            }
        });
    }
    else{
        ResetData();
    }
}

function ResetData()
{
    const spaceBoxes = document.querySelectorAll('#district-space #space-container');
    
    spaceBoxes.forEach((box, index) => {
        console.log(box);
      
        box.innerHTML = ''; // Clear existing content
    });

}

function MoveToPlacePage()
{
    window.location.href = place_page_url+`?district_id=${current_district}&place_category_cd=${current_category}` ;
}