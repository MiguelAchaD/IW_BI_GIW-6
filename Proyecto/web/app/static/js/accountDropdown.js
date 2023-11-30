document.addEventListener("DOMContentLoaded", function () {
    const profileSvg = document.getElementById("profile");
    const accountInfo = document.getElementById("account-info");
    const accountOptions = document.getElementById("account-options");
    const navBar = document.querySelector("nav");
    let isDropdownVisible = false;

    profileSvg.addEventListener("click", function () {
        toggleAccountDropdown(!isDropdownVisible);
        isDropdownVisible = !isDropdownVisible;
    });

    profileSvg.addEventListener("blur", function () {
        setTimeout(() => {
            if (isDropdownVisible) {
                toggleAccountDropdown(!isDropdownVisible);
                isDropdownVisible = !isDropdownVisible;
            }
        }, 100);
    });

    function toggleAccountDropdown(show) {
        const visibility = show ? "visible" : "hidden";
        const height = show ? (accountInfo ? "160px" : "120px") : "0";
        const borderColor = show ? "white" : "transparent";

        setDropdownStyles(visibility, height, borderColor);
    }

    function setDropdownStyles(visibility, height, borderColor) {
        if (accountInfo) accountInfo.style.height = height;
        if (accountOptions) accountOptions.style.height = height;

        navBar.style.borderBottom = `1px solid ${borderColor}`;
        if (accountInfo || accountOptions) {
            const dropdown = accountInfo || accountOptions;
            dropdown.style.visibility = visibility;
            dropdown.style.borderLeft = `1px solid ${borderColor}`;
            dropdown.style.borderRight = `1px solid ${borderColor}`;
            dropdown.style.borderBottom = `1px solid ${borderColor}`;
        }
    }
    
    const viewProfileLink = document.querySelector("#account-info a[href='']");
    const profileContainer = document.querySelector(".profile-container");

    if (viewProfileLink && profileContainer) {
        viewProfileLink.addEventListener("click", function (e) {
            e.preventDefault();
            profileContainer.classList.add("show-profile");
        });
    }

    document.addEventListener("click", function (e) {
        if (!profileContainer.contains(e.target) && !(accountInfo || accountOptions).contains(e.target) && !isDropdownVisible) {
            profileContainer.classList.remove("show-profile");
        }
    });
});
