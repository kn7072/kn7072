document.addEventListener("DOMContentLoaded", function(event) {
    var switchGroups = document.getElementById('switchVisibleGroups');
    var groups = document.getElementsByClassName('groupsContainer');

    switchGroups.addEventListener( "click", () => {
        for (let index = 0; index < groups.length; index++) {
            if (groups[index].classList.contains("hide")) {
                groups[index].classList.remove("hide");
            } else {
                groups[index].classList.add("hide");
            }
            
        }
    });
});