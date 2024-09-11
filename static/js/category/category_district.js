function fetchData(categoryCode) {
    const districtId = document.getElementById("district-id").value;

    fetch(`/get_places_by_category/${selected_lang}/${districtId}/${categoryCode}/`)
        .then(response => response.json())
        .then(data => {
            updatePlaces(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updatePlaces(places) {
    const districtSpace = document.getElementById("district-space");
    districtSpace.innerHTML = '';

    places.forEach(place => {
        const spaceContainer = document.createElement('div');
        spaceContainer.id = 'space-container';
        
        const spaceBox = document.createElement('div');
        spaceBox.className = 'space-box';

        const img = document.createElement('img');
        img.src = place.review_photo || fallbackImage;
        img.alt = place.place_name;

        const details = document.createElement('div');
        details.className = 'details';

        const title = document.createElement('h3');
        title.textContent = place.place_name;

        const tag = document.createElement('p');
        tag.textContent = place.place_tag_name;

        const reviews = document.createElement('p');
        reviews.textContent = `💜 ${place.place_review_num}`;

        details.appendChild(title);
        details.appendChild(tag);
        details.appendChild(reviews);

        spaceBox.appendChild(img);
        spaceBox.appendChild(details);
        spaceContainer.appendChild(spaceBox);

        districtSpace.appendChild(spaceContainer);
    });
}

function MoveToPlacePage() {
    // URL 이동 코드
}
