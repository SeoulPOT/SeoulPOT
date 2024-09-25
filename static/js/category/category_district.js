let is_selected = false;
let selected_obj;
let current_district;
let current_category;


document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    function updateMap() {
        const width = document.getElementById('map').clientWidth;
        const height = document.getElementById('map').clientHeight;

        document.documentElement.style.setProperty('--map-width', `${width}px`);
        document.documentElement.style.setProperty('--map-height', `${height}px`);

        let scale;
        if (window.innerWidth <= 600) {
            scale = 40000;
        } else if (window.innerWidth <= 1200) {
            scale = 70000;
        } else {
            scale = 80000;
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
            svg.attr('width', width).attr('height', height);
        }

        d3.json(window.geojsonUrl).then(function(geojsonData) {
            console.log("Loaded GeoJSON Data: ", geojsonData);
            const paths = svg.selectAll('path')
                .data(geojsonData.features, d => d.id);

            paths.enter().append('path')
                .attr('d', path)
                .attr('class', 'district')
                .attr('fill', function (d) {
                    // 각 구역에 따른 색상을 place_count 값에 따라 설정
                    const foundItem = districts_list.find(item => item.district_name.trim().toLowerCase() === d.properties.name.trim().toLowerCase());
                    
                    console.log("Districts list:", districts_list);
            
                    console.log("Matching district:", d.properties.name, "Found Item:", foundItem);
                    
                    if (foundItem) {
                        const place_count = foundItem.place_count || 0;
                        const max_count = Math.max(...districts_list.map(item => item.place_count || 0)); // 최대값 동적 계산
                        const min_lightness = 30; // 최소 밝기
                        const max_lightness = 90; // 최대 밝기
                        const lightness = max_lightness - (place_count / max_count) * (max_lightness - min_lightness);
            
                        console.log(`District: ${d.properties.name}, Place Count: ${place_count}, Lightness: ${lightness}`);
                        
                        return `hsl(258, 50%, ${lightness}%)`;  // HSL 색상 사용
                    } else {
                        console.log(`District ${d.properties.name} not found, applying default color.`);
                        return '#f7fcf5';  // 기본 색상 (장소가 없을 때)
                    }
                })
                .on('mouseover', function(event, d) {
                    const centroid = path.centroid(d);

                    d3.select(this).raise()
                        .classed('active', true)
                        .style('transform-origin', `${centroid[0]}px ${centroid[1]}px`);

                    if (!selected_obj) {
                        document.getElementById('district-name').innerText = d.properties.name;
                        // document.getElementById('none_select-info-container').style.display = 'none';
                        document.getElementById('district-container').style.display = 'none';
                        // document.getElementById('district-info-container').style.display = 'flex';
                    }

                    var foundItem = districts_list.find(function(item) {
                        return item.district_name === d.properties.name;
                    });

                    if (foundItem) {
                        const img_path = `${staticPath}/${foundItem.district_name}.png`;
                        // document.getElementById('selected-district-img').src = img_path;
                        // document.getElementById('selected-district-img').onerror = function() {
                        //     this.onerror = null;
                        //     this.src = '/static/img/default1.png';
                        // };
                    }
                })
                .on('mouseout', function(event, d) {
                    const centroid = path.centroid(d);
                    d3.select(this).classed('active', false)
                        .style('transform-origin', `${centroid[0]}px ${centroid[1]}px`);

                    if (!selected_obj) {
                        // document.getElementById('none_select-info-container').style.display = 'flex';
                        document.getElementById('district-container').style.display = 'none';
                        // document.getElementById('district-info-container').style.display = 'none';
                        document.getElementById('district-name').innerText = '';
                    }
                })
                .on('click', function(event, d) {
                    console.log('Selected district:', selected_obj);
                    d3.select(selected_obj).classed('clicked', false);

                    if (selected_obj === this) {
                        selected_obj = undefined;
                        document.getElementById('district-name').innerText = '';
                        // document.getElementById('none_select-info-container').style.display = 'none';
                        document.getElementById('district-container').style.display = 'none';
                        // document.getElementById('district-info-container').style.display = 'flex';
                    } else {
                        selected_obj = this;
                        is_selected = true;
                        d3.select(this).classed('clicked', true);

                        document.getElementById('district-name').innerText = d.properties.name;
                        // document.getElementById('none_select-info-container').style.display = 'none';
                        document.getElementById('district-container').style.display = 'flex';
                        // document.getElementById('district-info-container').style.display = 'none';

                        var foundItem = districts_list.find(function(item) {
                            console.log('Checking district_name:', item.district_name.trim().toLowerCase(), 'with GeoJSON name:', d.properties.name.trim().toLowerCase());
                            return item.district_name.trim().toLowerCase() === d.properties.name.trim().toLowerCase();
                        });
                        
                        if (foundItem) {
                            console.log('Found district:', foundItem.district_name, ', ID:', foundItem.district_id);
                            current_district = foundItem.district_id;
                            console.log('Found district:', foundItem.district_name, ', ID:', current_district);
                            
                            // category가 없는 경우 기본값 설정
                            category_code = current_category ? current_category : categories_list[0].code;
                            
                            console.log('Before fetch: current_district = ', current_district, 'current_category = ', current_category);
                            
                            // current_district가 설정되었는지 다시 확인
                            if (!current_district) {
                                console.error("District ID is not set correctly.");
                                return;
                            }
                        
                            // fetch 실행
                            fetchData(category_code);
                        } else {
                            console.error('District not found in districts_list for GeoJSON name:', d.properties.name);
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

// 데이터 fetch 함수
function fetchData(category) {
    current_category = category;
    
    category_container = document.querySelectorAll('#district-category > button');
    category_container.forEach(btn => { 
        console.log('btn : ' , btn);
        console.log('data-value:', btn.getAttribute('data-value'));
        if(btn.getAttribute('data-value') == current_category)
            btn.classList.add('active');
        else
            btn.classList.remove('active');
    });
    
    console.log('Before fetch: current_district = ', current_district, 'current_category = ', current_category);

    // // District ID가 없는 경우 처리
    // if (!current_district) {
    //     console.error("District ID is not set correctly.");
    //     return;
    // }

    console.log('selected_lang:', selected_lang);
    console.log('place_tag_cd:', place_tag_cd);
    console.log('current_district:', current_district);
    console.log('current_category:', current_category);


    console.log('Fetch URL:', `/${selected_lang}/${place_tag_cd}/${current_district}/${current_category}/`);
    fetch(`/category/${selected_lang}/${place_tag_cd}/${current_district}/${current_category}/`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    
    .then(response => {
        console.log("Raw Response: ", response);  // 추가
        return response.json();
    })
    .then(data => {
        console.log("Parsed Data: ", data);
        console.log("data : ", data.data);
        DisplayData(data.data);
    })
    .catch(error => console.log("Fetch Error:", error));
}


function DisplayData(data) {
    const spaceBoxes = document.querySelectorAll('#district-space #space-container');
    ResetData();

    console.log("Data to display:", data); 
    if (data.length > 0) {
        spaceBoxes.forEach((box, index) => {
            if (data[index]) {
                box.innerHTML = '';
                console.log("Appending item to box:", data[index]); 
                box.appendChild(createStoreItem(data[index]));
            }
        });
    } else {
        ResetData();
    }
}

function ResetData() {
    const spaceBoxes = document.querySelectorAll('#district-space #space-container');
    spaceBoxes.forEach(box => {
        box.innerHTML = '';
    });
}

function createStoreItem(store) {
    const div = document.createElement('div');
    div.classList.add('space-box');

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
    name.textContent = store.place_name;
    const tag = document.createElement('p');
    tag.textContent = store.place_tag_name;
    const reviews = document.createElement('p');
    reviews.textContent = `📝 리뷰 ${store.place_review_num}개`;

    details.appendChild(name);
    details.appendChild(tag);
    details.appendChild(reviews);

    div.appendChild(img);
    div.appendChild(details);

    div.onclick = function() {
        window.location.href = `/review?place_id=${store.place_id}`;
    };

    return div;
}

function MoveToPlacePage() {
    window.location.href = `${place_page_url}?district_id=${current_district}&place_category_cd=${current_category}`;
}
