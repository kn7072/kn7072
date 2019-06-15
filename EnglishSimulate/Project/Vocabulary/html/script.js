document.addEventListener("DOMContentLoaded", function(event) {
    var switchGroups = document.getElementById('switchVisibleGroups');
    var groups = document.getElementsByClassName('groupsContainer');

    switchGroups.addEventListener( "click", function (params) {
        var hide = !this.style.hide;
        for (let index = 0; index < groups.length; index++) {
            if(hide) {
                groups[index].style.display = 'none';
                
            } else {
                groups[index].style.display = 'flex';
            }
            
        }
        this.style.hide = hide;
    })
});