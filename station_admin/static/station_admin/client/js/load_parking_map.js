import {createSiteMarker, NOT_SELECTED_GARAGE_IMG, SELECTED_GARAGE_IMG, initSiteMenusExitButtons} from "./google_maps.js";

function initMap() {
    navigator.geolocation.getCurrentPosition(initCoordinates);

    function initCoordinates(position) {
        let currentLocation = {lat: position.coords.latitude, lng: position.coords.longitude};
        // const preselectedRentSpot = document.querySelector('[data-preselected-spot-id]');
        // if (preselectedRentSpot) {
        //     currentLocation = {
        //         lat: parseFloat(preselectedRentSpot.getAttribute('data-preselected-spot-latitude')),
        //         lng: parseFloat(preselectedRentSpot.getAttribute('data-preselected-spot-longitude')),
        //     };
        // }

        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 18,
            center: currentLocation,
            mapTypeControl: false,
            streetViewControl: false
        });

        // The marker, positioned at Uluru
        const marker = new google.maps.Marker({
            position: currentLocation,
            map: map,
            icon: {
                scaledSize: new google.maps.Size(38, 31),
            }
        });

        fetch('http://127.0.0.1:8000/station/api/parking-sites')
            .then(response => response.json())
            .then(data => {
                data.forEach((site) => {
                    let garageIcon = NOT_SELECTED_GARAGE_IMG;
                    // if (
                    //     preselectedRentSpot
                    //     && preselectedRentSpot.getAttribute('data-preselected-spot-site-id') == site.id
                    // ) {
                    //     garageIcon = SELECTED_GARAGE_IMG;
                    // }


                    createSiteMarker(site, map, garageIcon);
                });
            });

    }
}

window.initMap = initMap;

window.addEventListener('load', function () {
    initSiteMenusExitButtons();
});
