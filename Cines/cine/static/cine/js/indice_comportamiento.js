function cargarCines() {
    $.ajax({
        url: "http://localhost:8000/serializers/cinema/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            var ul = document.getElementById("cines");
            $("ul").empty()
            for (i = 0; i < data.results.length; i++) {
                var li = document.createElement("a");
                li.className = 'list-group-item';
                li.href("/cinema/"+data.results[i].pk+"/detallesCine/")
                li.appendChild(document.createTextNode(data.results[i].nombre));
                ul.appendChild(li);
            }
        },
        error: function () {
            document.getElementById("demo").innerHTML = "mal :(";
        }
    });
}
