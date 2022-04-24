import {
    initSessionTimer,
    elapsedSeconds,
    startSessionTimeCounting,
    displaySuccess,
    displayError,
    createSiteMarker,
    unsetAllMarkerIcons,
    closeAllSiteMenus,
    initSiteMenusExitButtons, startSessionTimer, openSiteMenu, initStopReservationBtn, hideSessionTimer
} from "./google_maps.js";


const NOT_SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_not_selected.svg";
const SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_selected.svg";

function startSession(rentSpotId) {
    fetch(`http://127.0.0.1:8000/station/rent-spot/${rentSpotId}/session/start`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                displaySuccess('Session has been started');
                closeAllSiteMenus();
                unsetAllMarkerIcons();
                startSessionTimer()
            } else {
                displayError(data.message);
            }
        }).catch((error) => {
        displayError(error);
    });
}

function endRentSession(rentSpotId) {
    fetch(`http://127.0.0.1:8000/station/rent-spot/${rentSpotId}/session/end`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                displaySuccess('Session has been ended')
                closeAllSiteMenus();
                unsetAllMarkerIcons();
                hideSessionTimer();
            } else {
                displayError(data.message);
            }
        }).catch((error) => {
        displayError(error);
    });
}

function openRentSpotMenu(rentSpotId) {
    closeAllSiteMenus();
    unsetAllMarkerIcons();
    let rentSpotMenu = document.querySelector(`[data-rent-spot-id='${rentSpotId}']`)

    let startRentSessionBtn = document.querySelector('[data-start-rent-session-btn]');
    if (startRentSessionBtn) {
        startRentSessionBtn.addEventListener('click', () => {
            startSession(rentSpotId);
        });
    } else {
        let endRentSessionBtn = document.querySelector('[data-end-rent-session-btn]');
        endRentSessionBtn.addEventListener('click', () => {
            endRentSession(rentSpotId);
        });
    }

    rentSpotMenu.style.height = "300px";
}

function initMap() {
    navigator.geolocation.getCurrentPosition(initCoordinates);

    function initCoordinates(position) {
        let currentLocation = {lat: position.coords.latitude, lng: position.coords.longitude};
        const preselectedRentSpot = document.querySelector('[data-preselected-spot-id]');
        const preselectedSite = document.querySelector('[data-preselected-site]');

        if (preselectedRentSpot) {
            currentLocation = {
                lat: parseFloat(preselectedRentSpot.getAttribute('data-preselected-spot-latitude')),
                lng: parseFloat(preselectedRentSpot.getAttribute('data-preselected-spot-longitude')),
            };
        } else if (preselectedSite) {
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

        // The marker, positioned at Uluru
        const marker = new google.maps.Marker({
            position: currentLocation,
            map: map,
            icon: {
                scaledSize: new google.maps.Size(38, 31),
            }
        });

        fetch('http://127.0.0.1:8000/station/api/rent-sites')
            .then(response => response.json())
            .then(data => {
                data.forEach((site) => {
                    let garageIcon = NOT_SELECTED_GARAGE_IMG;
                    const preselectedRentSpotExists = preselectedRentSpot
                        && preselectedRentSpot.getAttribute('data-preselected-spot-site-id') == site.id;

                    const preselectedSiteExists = preselectedSite
                        && preselectedSite.getAttribute('data-side-id') == site.id;

                    if (preselectedRentSpotExists || preselectedSiteExists) {
                        garageIcon = SELECTED_GARAGE_IMG;
                    }

                    let marker = createSiteMarker(site, map, garageIcon);
                });
            });

        if (preselectedRentSpot) {
            let rentSpotId = preselectedRentSpot.getAttribute('data-preselected-spot-id');
            openRentSpotMenu(rentSpotId);
        }

        if (preselectedSite) {
            let siteId = preselectedSite.getAttribute('data-side-id');
            openSiteMenu(siteId);
        }

    }
}

window.initMap = initMap;

window.addEventListener('load', function () {
    initSiteMenusExitButtons();
    initVehicleReserveButtons();

    const tabs = document.querySelectorAll(".site-menu-wrapper");
    const tabButton = document.querySelectorAll(".tab-button");
    const contents = document.querySelectorAll(".content");

    tabs.forEach((e) => {
        e.onclick = (e) => {
            const id = e.target.dataset.id;
            const listType = e.target.getAttribute("data-site-list-type");
            const siteId = e.target.getAttribute("data-site-id");

            if (listType && siteId) {
                tabButton.forEach(btn => {
                    btn.classList.remove("active");
                });
                e.target.classList.add("active");

                contents.forEach(content => {
                    content.classList.remove("active");
                });

                const dataSelector = listType === 'bike' ? `bike-${siteId}` : `scooter-${siteId}`;
                const element = document.querySelectorAll(`[data-site-vehicle-list=${dataSelector}]`)[0];

                element.classList.add("active");
            }
        }
    });

    initSessionTimer();
    initStopReservationBtn(false);
});

function initVehicleReserveButtons() {
    document.querySelectorAll('[data-vehicle-reserve-id]').forEach((button) => {
        button.addEventListener('click', () => {
            reserveVehicle(button.getAttribute('data-vehicle-reserve-id'));
        })
    });
}

function reserveVehicle(spotId) {
    fetch(`http://127.0.0.1:8000/station/api/spot/${spotId}/reservation/start`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                displaySuccess('Reservation has been started');
                startSessionTimer(true);
                removeVehicleFromList(spotId);

            } else {
                displayError(data.message);
            }
        }).catch((error) => {
            displayError(error);
    });
}

function removeVehicleFromList(spotId) {
    document.querySelectorAll(`[data-rent-vehicle-row='${spotId}']`).forEach((element) => {
        element.remove();
    })
}