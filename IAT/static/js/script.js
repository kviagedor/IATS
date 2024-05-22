document.addEventListener("DOMContentLoaded", function() {
    const menuItems = document.querySelectorAll('.menu li');

    menuItems.forEach(item => {
        item.addEventListener('click', function(event) {
            // Remove the active class from all li elements
            menuItems.forEach(item => {
                item.classList.remove('active');
            });

            // Add the active class to the clicked li element
            this.classList.add('active');
        });
    });
});