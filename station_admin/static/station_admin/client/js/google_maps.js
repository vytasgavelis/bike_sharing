let markers = [];
const NOT_SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_not_selected.svg";
const SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_selected.svg";

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



export {
    createSiteMarker,
    unsetAllMarkerIcons,
    closeAllSiteMenus,
    NOT_SELECTED_GARAGE_IMG,
    SELECTED_GARAGE_IMG,
    initSiteMenusExitButtons
};