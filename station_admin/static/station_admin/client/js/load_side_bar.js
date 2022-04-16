function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
//  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  //document.getElementById("main").style.marginLeft= "0";
}

window.addEventListener('load', function() {
  document.getElementById("sidebar-toggle-btn").onclick = () => {
    openNav();
  }

  document.getElementById("sidebar-exit-btn").onclick = () => {
    closeNav();
  }
});