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

let markers = [];

function persistMarker(marker) {
    markers.push(marker)
}


const NOT_SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_not_selected.svg";
const SELECTED_GARAGE_IMG = "/static/station_admin/client/img/svg/garage_selected.svg";


function initMap() {
    navigator.geolocation.getCurrentPosition(initCoordinates);

    function initCoordinates(position) {
        const currentLocation = {lat: position.coords.latitude, lng: position.coords.longitude};
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 18,
            center: currentLocation,
        });

        // The marker, positioned at Uluru
        const marker = new google.maps.Marker({
            position: currentLocation,
            map: map,
            icon: {
                scaledSize: new google.maps.Size(38, 31),
            }
        });

        marker.addListener('click', () => {
            console.log('it was clicked!');
        });

        fetch('http://127.0.0.1:8000/station/api/rent-sites')
            .then(response => response.json())
            .then(data => {
                data.forEach((site) => {
                    const marker = new google.maps.Marker({
                        position: {lat: site.latitude, lng: site.longitude},
                        map: map,
                        icon: {
                            url: NOT_SELECTED_GARAGE_IMG,
                            scaledSize: new google.maps.Size(60, 60),
                        }
                    });

                    persistMarker(marker);

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
                })
            });

    }
}

window.initMap = initMap;

window.addEventListener('load', function () {
    document.querySelectorAll('[data-site-bar-exit-btn]').forEach((item) => {
        let siteId = item.getAttribute('data-site-bar-exit-btn');
        item.onclick = () => {
            let siteMenu = document.querySelectorAll(`[data-side-id='${siteId}']`)[0];
            siteMenu.style.height = "0";
        }
    });
});