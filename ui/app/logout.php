<html>
    <head>
    <script>
        sessionStorage.clear();

        console.log(document.cookie);
        if (document.cookie === ""){
            location.reload();
            window.location.replace("./index.php");
        }
        else{
            var cookies = document.cookie.split(";");

            for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i];
                    var eqPos = cookie.indexOf("=");
                    var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
                    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
                }
            location.reload();
        }
    </script>
    <body>

           

    </body>