window.addEventListener("load", function () {

    setTimeout(function () {

        const splash = document.getElementById("splash-screen");
        const main = document.getElementById("main-content");

        if (splash && main) {

            splash.style.opacity = "0";
            splash.style.visibility = "hidden";

            setTimeout(function () {

                splash.style.display = "none";
                main.style.display = "block";

                document.body.style.overflow = "auto";

            }, 1000);
        }

    }, 4000);

});