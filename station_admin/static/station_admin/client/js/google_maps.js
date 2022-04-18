let markers = [];
const NOT_SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_not_selected.svg";
const SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_selected.svg";
let elapsedSeconds = 0;

function persistMarker(marker) {
    markers.push(marker)
}

function closeAllSiteMenus() {
    document.querySelectorAll(`[data-side-id]`).forEach((siteMenu) => {
        siteMenu.style.height = "0";
    });
}

function unsetAllMarkerIcons() {
    markers.forEach((marker) => {
        marker.setIcon({
            url: NOT_SELECTED_GARAGE_IMG,
            scaledSize: new google.maps.Size(60, 60),
        });
    });
}

function createSiteMarker(site, map, garageIcon) {
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
        unsetAllMarkerIcons();
        let siteMenu = document.querySelectorAll(`[data-side-id='${site.id}']`)[0];
        siteMenu.style.height = "300px";

        marker.setIcon({
            url: SELECTED_GARAGE_IMG,
            scaledSize: new google.maps.Size(60, 60),
        });
    });

    persistMarker(marker);

    return marker;
}

function initSiteMenusExitButtons() {
    document.querySelectorAll('[data-site-bar-exit-btn]').forEach((item) => {
        let siteId = item.getAttribute('data-site-bar-exit-btn');
        item.onclick = () => {
            let siteMenu = document.querySelectorAll(`[data-side-id='${siteId}']`)[0];
            siteMenu.style.height = "0";
            unsetAllMarkerIcons();
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

function startSessionTimer() {
    let sessionTimer = document.querySelector('[data-session-elapsed-seconds]');
    if (sessionTimer) {
        elapsedSeconds = 0
        let sessionTimerContainer = document.getElementsByClassName('session-status-grid-container')[0];
        sessionTimerContainer.classList.remove('hidden');
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

export {
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
    displaySuccess
};