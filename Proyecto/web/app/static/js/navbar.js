document.addEventListener("DOMContentLoaded", function () {
    const profileSvg = document.getElementById("profile");
    const accountInfo = document.getElementById("account-info");
    const accountOptions = document.getElementById("account-options");
    const navBar = document.querySelector("nav");
    const profilePicMenu = document.getElementById('profile-pic-menu');
    const profileContainer = document.querySelector(".profile-container");
    const viewProfileLink = document.querySelector("#account-info a[href='']");
    const easeTime = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--ease-time')) * 1000;
    const hamburgerMenu = document.getElementById("hamburger-menu");
    const dropdownNavbars = document.querySelectorAll(".navbar.dropdown");
    let isDropdownVisible = false;
    
    hamburgerMenu.addEventListener("click", function () {
      dropdownNavbars.forEach(navbar => {
        navbar.classList.toggle("active");
      });
    });

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
        }, 200);
    });

    document.getElementById('profilepic').addEventListener('click', function () {
        var profilePicMenu = document.getElementById('profile-pic-menu');
        profilePicMenu.classList.toggle('visible');

        if (profilePicMenu.classList.contains('visible')) {
            loadProfileImages();
        }
    });

    document.addEventListener("click", function (e) {
        if (!profileContainer.contains(e.target) && !profilePicMenu.contains(e.target) && !(accountInfo || accountOptions).contains(e.target) && !isDropdownVisible) {
            if(profilePicMenu.classList.contains('visible')){
                profilePicMenu.classList.remove('visible');
                setTimeout(() => {
                    profileContainer.classList.remove("show-profile");
                }, easeTime);
            }else{
                profileContainer.classList.remove("show-profile");
            }
        }   
    });

    if (viewProfileLink && profileContainer) {
        viewProfileLink.addEventListener("click", function (e) {
            e.preventDefault();
            profileContainer.classList.add("show-profile");
        });
    }

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

    function updateProfilePicture(imageUrl) {
        fetch('/accounts/profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 'imageUrl': imageUrl })
        }).catch(error => console.error('Error asociando imagenes al perfil de usuario:', error));
    
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function loadProfileImages() {
        var images = document.querySelectorAll('#profile-pic-menu img[data-src]');
        images.forEach((img, index) => {
            setTimeout(() => {
                img.setAttribute('src', img.getAttribute('data-src'));
                img.removeAttribute('data-src');
                img.classList.add('loaded');
            }, 200 * index + easeTime);
    
            img.addEventListener('click', function () {
                let imageUrl = 'images/profiles/profile' + (index + 1).toString() + '.png';
                updateProfilePicture(imageUrl);
    
                const profilePic = document.getElementById('profilepic');
                if (profilePic) {
                    profilePic.classList.add('fade-out');
    
                    setTimeout(function() {
                        profilePic.src = img.src;
                        profilePic.classList.remove('fade-out');
                    }, easeTime);
                }
            });
        });
    }
});

