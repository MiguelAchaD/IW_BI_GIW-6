document.addEventListener("DOMContentLoaded", function () {
    const profileSvg = document.getElementById("profile");
    const accountDropdowns = document.getElementsByClassName("account-dropdown-content");
    let isClicked = false;
    let isMouseIn = false;

    profileSvg.addEventListener("click", function () {
        if (!isClicked) {
            showAccountDropdown();
            isClicked = true;
        } else {
            hideAccountDropdown();
            isClicked = false;
        }
    });

    profileSvg.addEventListener("blur", function () {
        if(!isMouseIn){
            hideAccountDropdown();
            isClicked = false;
        }
    });

    for (const accountDropdown of accountDropdowns) {
        accountDropdown.addEventListener("mouseenter", function () {
            isMouseIn = true;
        });

        accountDropdown.addEventListener("mouseleave", function () {
            isMouseIn = false;
        });
    }

    function showAccountDropdown() {
        for (const accountDropdown of accountDropdowns) {
            accountDropdown.style.display = "block";
        }
    }

    function hideAccountDropdown() {
        for (const accountDropdown of accountDropdowns) {
            accountDropdown.style.display = "none";
        }
    }
});
