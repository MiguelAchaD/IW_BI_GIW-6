document.addEventListener("DOMContentLoaded", function () {
    const profileSvg = document.getElementById("profile");
    let isClicked = true

    profileSvg.addEventListener("click", function () {
        if (isClicked) {
            showAccountDropdown();
            isClicked = false;
        } else {
            hideAccountDropdown();
            isClicked = true;
        }
    });

    function showAccountDropdown() {
        const accountDropdowns = document.getElementsByClassName("account-dropdown-content");
        for (const accountDropdown of accountDropdowns) {
            accountDropdown.style.display = "block";
        }
    }

    function hideAccountDropdown() {
        const accountDropdowns = document.getElementsByClassName("account-dropdown-content");
        for (const accountDropdown of accountDropdowns) {
            accountDropdown.style.display = "none";
        }
    }
});