import {
    openSiteMenu,
    hideSessionTimer,
    initSessionTimer,
    startParkingTimer,
    displayError,
    displaySuccess,
    createSiteMarker,
    initSiteMenusExitButtons, closeAllSiteMenus, unsetAllMarkerIcons
} from "./google_maps.js";

const NOT_SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/parking_not_selected.svg"
const SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/parking_selected.svg"

function startParkingSession(siteId, parkingSpotType) {
    console.log(`Starting session for: ${siteId} type: ${parkingSpotType}`);

    fetch(`http://127.0.0.1:8000/station/api/site/${siteId}/session/start/${parkingSpotType}`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                displaySuccess('Session has been started');
                startParkingTimer(data.max_time_mins);
                closeAllSiteMenus();
                unsetAllMarkerIcons(NOT_SELECTED_GARAGE_IMG);
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
                unsetAllMarkerIcons(NOT_SELECTED_GARAGE_IMG);
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

function initRentButtons() {
    document.querySelectorAll('[data-rent-vehicle-btn]').forEach((button) => {
        const siteId = button.getAttribute('data-rent-vehicle-btn');
        button.addEventListener('click', () => {
            openSiteGate(siteId);
        });
    });
}

function openSiteGate(siteId) {
    fetch(`http://127.0.0.1:8000/station/api/site/${siteId}/gate/open`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                window.location.href = `http://127.0.0.1:8000/station/rent-map?site_id=${siteId}`;
            } else {
                displayError(data.message);
            }
        }).catch((error) => {
        displayError(error);
    });
}

function initMap() {
    navigator.geolocation.getCurrentPosition(initCoordinates);

    function initCoordinates(position) {
        let currentLocation = {lat: position.coords.latitude, lng: position.coords.longitude};
        const preselectedSite = document.querySelector('[data-preselected-site]');

        if (preselectedSite) {
            currentLocation = {
                lat: parseFloat(preselectedSite.getAttribute('data-preselected-site-latitude')),
                lng: parseFloat(preselectedSite.getAttribute('data-preselected-site-longitude')),
            };
        }

        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 18,
            center: currentLocation,
            mapTypeControl: false,
            streetViewControl: false
        });

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
                    if (
                        preselectedSite
                        && preselectedSite.getAttribute('data-side-id') == site.id
                    ) {
                        garageIcon = SELECTED_GARAGE_IMG;
                    }

                    createSiteMarker(site, map, garageIcon, SELECTED_GARAGE_IMG, NOT_SELECTED_GARAGE_IMG);
                });
            });

        if (preselectedSite) {
            const siteId = preselectedSite.getAttribute('data-side-id');
            openSiteMenu(siteId);
        }
    }
}

window.initMap = initMap;

window.addEventListener('load', function () {
    initSiteMenusExitButtons(NOT_SELECTED_GARAGE_IMG);
    initSiteMenusSessionButtons();
    initSessionTimer();
    initRentButtons();
});
