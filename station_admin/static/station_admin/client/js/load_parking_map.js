import {
    hideSessionTimer,
    initSessionTimer,
    startSessionTimer,
    displayError,
    displaySuccess,
    createSiteMarker,
    NOT_SELECTED_GARAGE_IMG,
    SELECTED_GARAGE_IMG,
    initSiteMenusExitButtons, closeAllSiteMenus, unsetAllMarkerIcons
} from "./google_maps.js";

function startParkingSession(siteId, parkingSpotType) {
    console.log(`Starting session for: ${siteId} type: ${parkingSpotType}`);

    fetch(`http://127.0.0.1:8000/station/api/site/${siteId}/session/start/${parkingSpotType}`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                displaySuccess('Session has been started');
                //TODO: close down the window and start showing session timer
                startSessionTimer();
                closeAllSiteMenus();
                unsetAllMarkerIcons();
            } else {
                displayError(data.message);
            }
        }).catch((error) => {
        displayError(error);
    });
}

function endParkingSession(siteId) {
    fetch(`http://127.0.0.1:8000/station/api/site/${siteId}/session/end`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                displaySuccess('Session has been ended');
                //TODO: close down the window and start showing session timer
                hideSessionTimer();
                closeAllSiteMenus();
                unsetAllMarkerIcons();
            } else {
                displayError(data.message);
            }
        }).catch((error) => {
        displayError(error);
    });
}

function initSiteMenusSessionButtons() {
    let startSessionBtns = document.querySelectorAll('[data-start-parking-session-btn]');
    startSessionBtns.forEach((button) => {
        const siteId = button.getAttribute('data-start-parking-session-btn');
        const parkingSpotType = button.getAttribute('data-start-parking-session-btn-type');
        button.addEventListener('click', () => {
            startParkingSession(siteId, parkingSpotType)
        });
    });

    let endSessionBtns = document.querySelectorAll('[data-end-parking-session-btn]');
    endSessionBtns.forEach((button) => {
        const siteId = button.getAttribute('data-end-parking-session-btn');
        button.addEventListener('click', () => {
            endParkingSession(siteId);
        })
    })
}

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
    initSiteMenusSessionButtons();
    initSessionTimer();
});
