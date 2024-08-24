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
                    }
                    

            
                    // 조건을 만족하는 객체가 있으면 출력
                    var foundItem = districts_list.find(function(item) {
                        return item.district_name === d.properties.name;
                    });

                    if (foundItem) {
                        img_path = staticPath+`/${foundItem.district_name}_가로.png`;
                        console.log('img_path : ', fallbackImage);
                        console.log('img_path : ', img_path);
                        document.getElementById('selected-district-desc').innerText = foundItem.district_desc;
                        document.getElementById('selected-district-img').src = img_path;
                        document.getElementById('selected-district-img').onerror = function() {
                            this.onerror = null;
                            this.src = '/static/img/default1.png';
                        };
                        
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
                        document.getElementById('none_select-info-container').style.display = 'flex';
                        document.getElementById('district-container').style.display = 'none';
                        document.getElementById('district-info-container').style.display = 'none';
                        document.getElementById('district-name').innerText = 'ㅤ';
                    }


                })
                .on('click', function(event, d) {
                    console.log('seleced_distict :', selected_obj);
                    d3.select(selected_obj).classed('clicked', false);

                    if(selected_obj == this){
                        selected_obj = undefined;
                        document.getElementById('none_select-info-container').style.display = 'none';
                        document.getElementById('district-container').style.display = 'none';
                        document.getElementById('district-info-container').style.display = 'flex';
                    }
                    else{
                        selected_obj = this;
                        is_selected = true;
                        d3.select(this).classed('clicked', true);
                        // setTimeout(() => {
                        //     d3.select(this).classed('clicked', false);
                        // }, 5);
    
                        document.getElementById('district-name').innerText = d.properties.name;
                        
                        is_selected = true;
                        document.getElementById('none_select-info-container').style.display = 'none';
                        document.getElementById('district-container').style.display = 'flex';
                        document.getElementById('district-info-container').style.display = 'none';
    
                        var foundItem = districts_list.find(function(item) {
                            return item.district_name === d.properties.name;
                        });
    
                        if (foundItem) {
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



// 데이터베이스 연동 코드로 수정 필요
async function fetchCSV(url) {
    const response = await fetch(url);
    const text = await response.text();
    return text;
}

function parseCSV(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split(',').map(header => header.trim());
    const data = lines.slice(1).map(line => {
        const values = line.split(',').map(value => value.trim());
        const row = {};
        headers.forEach((header, index) => {
            row[header] = values[index];
        });
        return row;
    });
    return data;
}

function createStoreItem(store) {
    const div = document.createElement('div');
    div.classList.add('space-box');
    console.log('store : ', store);

    const img = document.createElement('img');
    img.src = store.review_photo;
    img.alt = store.place_name;
    // 이미지 로드에 실패할 경우 대체 이미지 설정
    img.onerror = function() {
        this.onerror = null;  // 무한 반복 방지
        this.src = fallbackImage;  // 대체 이미지 경로
    };
    
    const details = document.createElement('div');
    details.classList.add('details');
    
    const name = document.createElement('h3');
    name.textContent = store.place_name;
    name.id = 'place-name';

    const tag = document.createElement('p');
    //tag.textContent = `${store.place_tag}`;
    tag.id = 'place-tag';

    const reviews = document.createElement('p');
    //reviews.textContent = `리뷰 ${store.review_num}개`;
    reviews.id = 'place-reviews';
    
    details.appendChild(name);
    details.appendChild(tag);
    details.appendChild(reviews);
    
    div.appendChild(img);
    div.appendChild(details);
    
    return div;
}

// async function loadAndDisplayData() {
//     const csvUrl = window.district_temp_place;
//     const csvText = await fetchCSV(csvUrl);
//     const data = parseCSV(csvText);

//     const spaceBoxes = document.querySelectorAll('#district-space #space-container');
//     spaceBoxes.forEach((box, index) => {
//         if (data[index]) {
//             box.innerHTML = ''; // Clear existing content
//             box.appendChild(createStoreItem(data[index]));
//         }
//     });
// }

//document.addEventListener('DOMContentLoaded', loadAndDisplayData);

///////////////////////////////////////////////////////////////////////////////////////


function fetchData(category) {
    current_category = category;

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