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
    
                    document.getElementById('district-name').innerText = d.properties.name;
                })
                .on('mouseout', function(event, d) {
                    const centroid = path.centroid(d);
                    d3.select(this)
                        .classed('active', false)
                        .style('transform-origin', `${centroid[0]}px ${centroid[1]}px`);
                    document.getElementById('district-name').innerText = 'ㅤ';
                })
                .on('click', function(event, d) {
                    d3.select(this).classed('clicked', true);
                    setTimeout(() => {
                        d3.select(this).classed('clicked', false);
                    }, 500);
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
    
    const img = document.createElement('img');
    img.src = store.img;
    img.alt = store.place_name;
    
    const details = document.createElement('div');
    details.classList.add('details');
    
    const name = document.createElement('h3');
    name.textContent = store.place_name;
    name.id = 'place-name';

    const tag = document.createElement('p');
    tag.textContent = `${store.place_tag}`;
    tag.id = 'place-tag';

    const reviews = document.createElement('p');
    reviews.textContent = `리뷰 ${store.review_num}개`;
    reviews.id = 'place-reviews';
    
    details.appendChild(name);
    details.appendChild(tag);
    details.appendChild(reviews);
    
    div.appendChild(img);
    div.appendChild(details);
    
    return div;
}

async function loadAndDisplayData() {
    const csvUrl = window.district_temp_place;
    const csvText = await fetchCSV(csvUrl);
    const data = parseCSV(csvText);

    const spaceBoxes = document.querySelectorAll('#district-space #space-container');
    spaceBoxes.forEach((box, index) => {
        if (data[index]) {
            box.innerHTML = ''; // Clear existing content
            box.appendChild(createStoreItem(data[index]));
        }
    });
}

document.addEventListener('DOMContentLoaded', loadAndDisplayData);
