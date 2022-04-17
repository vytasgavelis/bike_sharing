import {createSiteMarker, unsetAllMarkerIcons, closeAllSiteMenus, initSiteMenusExitButtons} from "./google_maps.js";


function displaySuccess(message) {
    const messageContainer = document.querySelector('[data-message-container]');
    messageContainer.innerHTML = `<div class=\"bar success\">${message}</div>`;
}

function displayError(message) {
    const messageContainer = document.querySelector('[data-message-container]');
    messageContainer.innerHTML = `<div class=\"bar error\">${message}</div>\n`;
}

let elapsedSeconds = 0;

function startSessionTimeCounting(sessionTimer) {
    elapsedSeconds += 1;
    let time = elapsedSeconds;

    // Hours, minutes and seconds
    var hrs = ~~(time / 3600);
    var mins = ~~((time % 3600) / 60);
    var secs = ~~time % 60;

    // Output like "1:01" or "4:03:59" or "123:03:59"
    var ret = "";
    if (hrs > 0) {
        ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
    }
    ret += "" + mins + ":" + (secs < 10 ? "0" : "");
    ret += "" + secs;

    sessionTimer.innerHTML = ret;
}

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
                //TODO: close down the window and start showing session timer
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
        if (preselectedRentSpot) {
            currentLocation = {
                lat: parseFloat(preselectedRentSpot.getAttribute('data-preselected-spot-latitude')),
                lng: parseFloat(preselectedRentSpot.getAttribute('data-preselected-spot-longitude')),
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
                    if (
                        preselectedRentSpot
                        && preselectedRentSpot.getAttribute('data-preselected-spot-site-id') == site.id
                    ) {
                        garageIcon = SELECTED_GARAGE_IMG;
                    }

                    let marker = createSiteMarker(site, map, garageIcon);
                });
            });

        if (preselectedRentSpot) {
            let rentSpotId = preselectedRentSpot.getAttribute('data-preselected-spot-id');
            openRentSpotMenu(rentSpotId);
        }

    }
}

window.initMap = initMap;

window.addEventListener('load', function () {
    initSiteMenusExitButtons();

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

    let sessionTimer = document.querySelector('[data-session-elapsed-seconds]');
    if (sessionTimer) {
        let elapsedSecondsData = sessionTimer.getAttribute('data-session-elapsed-seconds');
        elapsedSeconds = parseInt(elapsedSecondsData);
        setInterval(function () {
            startSessionTimeCounting(sessionTimer)
        }, 1000);
    }
});