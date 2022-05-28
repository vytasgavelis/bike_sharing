let markers = [];
const NOT_SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_not_selected.svg";
const SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_selected.svg";
let elapsedSeconds = 0;
const NO_PARKING_SPOTS_IMG = "/static/station_admin/client/img/svg/parking_no_spots.svg"
const NO_RENT_SPOTS_IMG = "/static/station_admin/client/img/svg/no_rent_spots.svg"
const SELECTED_PARKING_MARKER_IMG = "/static/station_admin/client/img/svg/parking_selected.svg"
const PARKING_TYPE = 'parking';
const RENTING_TYPE = 'renting';
function persistMarker(marker) {
    markers.push(marker)
}

function closeAllSiteMenus() {
    document.querySelectorAll(`[data-side-id]`).forEach((siteMenu) => {
        siteMenu.style.height = "0";
    });
}

function openSiteMenu(siteId) {
    let siteMenu = document.querySelectorAll(`[data-side-id='${siteId}']`)[0];
    siteMenu.style.height = "300px";
}

function unsetAllMarkerIcons(garageImg = NOT_SELECTED_GARAGE_IMG) {
    markers.forEach((marker) => {
        let noSpotsImg = marker.type === PARKING_TYPE ? NO_PARKING_SPOTS_IMG : NO_RENT_SPOTS_IMG;

        marker.marker.setIcon({
            url: marker.hasOpenSpots ? garageImg : noSpotsImg,
            scaledSize: new google.maps.Size(60, 60),
        });
    });
}

function markMarkerAsOpen(siteId) {
    markers.forEach((marker) => {
        if (marker.siteId == siteId) {
            let img = marker.type === PARKING_TYPE ? SELECTED_PARKING_MARKER_IMG : SELECTED_GARAGE_IMG;
            marker.marker.setIcon({
                url: img,
                scaledSize: new google.maps.Size(60, 60)
            });
        }
    })
}

function createSiteMarker(
    site, map, garageIcon, selectedGarageImg = SELECTED_GARAGE_IMG, notSelectedGarageImg = NOT_SELECTED_GARAGE_IMG, noSiteSpotsImg = NO_PARKING_SPOTS_IMG, type='parking'
) {
    const marker = new google.maps.Marker({
        position: {lat: site.latitude, lng: site.longitude},
        map: map,
        icon: {
            url: garageIcon,
            scaledSize: new google.maps.Size(60, 60),
        }
    });

    marker.addListener('click', () => {
        closeAllSiteMenus();
        unsetAllMarkerIcons(notSelectedGarageImg);
        openSiteMenu(site.id)
        marker.setIcon({
            url: selectedGarageImg,
            scaledSize: new google.maps.Size(60, 60)
        });
    });

    persistMarker({'marker': marker, 'hasOpenSpots': site.hasOpenSpots, 'type': type, 'siteId': site.id});

    return marker;
}

function initSiteMenusExitButtons(notSelectedGarageImg = NOT_SELECTED_GARAGE_IMG) {
    document.querySelectorAll('[data-site-bar-exit-btn]').forEach((item) => {
        let siteId = item.getAttribute('data-site-bar-exit-btn');
        item.onclick = () => {
            let siteMenu = document.querySelectorAll(`[data-side-id='${siteId}']`)[0];
            siteMenu.style.height = "0";
            unsetAllMarkerIcons(notSelectedGarageImg);
        }
    });
}

function displaySuccess(message) {
    const messageContainer = document.querySelector('[data-message-container]');
    messageContainer.innerHTML = `<div class=\"bar success\">${message}</div>`;
}

function displayError(message) {
    const messageContainer = document.querySelector('[data-message-container]');
    messageContainer.innerHTML = `<div class=\"bar error\">${message}</div>\n`;
}

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

function initSessionTimer() {
    let sessionTimer = document.querySelector('[data-session-elapsed-seconds]');
    if (sessionTimer) {
        let elapsedSecondsData = sessionTimer.getAttribute('data-session-elapsed-seconds');
        elapsedSeconds = parseInt(elapsedSecondsData);

        setInterval(function () {
            startSessionTimeCounting(sessionTimer)
        }, 1000);
    }
}

function startSessionTimer(showStopReservationBtn = false) {
    let sessionTimer = document.querySelector('[data-session-elapsed-seconds]');
    if (sessionTimer) {
        elapsedSeconds = parseInt(sessionTimer.getAttribute('data-session-elapsed-seconds'))
        let sessionTimerContainer = document.getElementsByClassName('session-status-grid-container')[0];
        sessionTimerContainer.classList.remove('hidden');

        if (showStopReservationBtn) {
            initStopReservationBtn();
        }
    }
}

function startParkingTimer(max_time_mins) {
    let sessionTimer = document.querySelector('[data-session-elapsed-seconds]');
    if (sessionTimer) {
        elapsedSeconds = parseInt(sessionTimer.getAttribute('data-session-elapsed-seconds'))
        let sessionTimerContainer = document.getElementsByClassName('session-status-grid-container')[0];
        sessionTimerContainer.classList.remove('hidden');
        let parkingLabel = sessionTimerContainer.getElementsByClassName('session-status-parking-label')[0];
        parkingLabel.innerHTML = max_time_mins && max_time_mins > 0 ? `Parking is active. Max time: ${max_time_mins} mins.` : "Parking is active.";
    }
}

function initStopReservationBtn(shouldUnhide = true) {
    let elements = document.getElementsByClassName('session-status-cancel-btn');
    if (elements.length > 0) {
        let stopReservationBtn = elements[0]
        if (shouldUnhide) {
            stopReservationBtn.classList.remove('hidden');
        }
        stopReservationBtn.addEventListener('click', () => {
            stopReservation();
        })
    }
}

function hideSessionTimer() {
    let sessionTimer = document.querySelector('[data-session-elapsed-seconds]');
    if (sessionTimer) {
        elapsedSeconds = 0
        let sessionTimerContainer = document.getElementsByClassName('session-status-grid-container')[0];
        sessionTimerContainer.classList.add('hidden');
    }
}

function stopReservation() {
    fetch(`http://127.0.0.1:8000/station/api/reservation/end`, {
        method: 'POST',
        headers: {'X-CSRFToken': window.CSRF_TOKEN},
    }).then(response => response.json())
        .then(data => {
            if (data.success == true) {
                displaySuccess('Reservation has been ended');
                hideSessionTimer();
            } else {
                displayError(data.message);
            }
        }).catch((error) => {
        displayError(error);
    });


}

function showSiteImgModal() {
    let modal = document.getElementById('site-image-modal');
    modal.style.display = 'block';
}

function initSiteImage() {
    document.querySelectorAll('.site-image').forEach((element) => {
        element.addEventListener('click', () => {
            showSiteImgModal()
        })
    })

    document.getElementById('close-site-image').addEventListener('click', () => {
        document.getElementById('site-image-modal').style.display = 'none'
    })
}

export {
    openSiteMenu,
    hideSessionTimer,
    initSessionTimer,
    startSessionTimer,
    elapsedSeconds,
    startSessionTimeCounting,
    createSiteMarker,
    unsetAllMarkerIcons,
    closeAllSiteMenus,
    NOT_SELECTED_GARAGE_IMG,
    SELECTED_GARAGE_IMG,
    initSiteMenusExitButtons,
    displayError,
    displaySuccess,
    initStopReservationBtn,
    startParkingTimer,
    markMarkerAsOpen,
    initSiteImage
};