$(document).ready(function () {
    $.getJSON("/list", function (result) {
        var optionH = $("#optionH");
        var optionA = $("#optionA");
        //don't forget error handling!
        $.each(result, function (item, value) {
            optionH.append($("<option />").val(value).text(value));
            optionA.append($("<option />").val(value).text(value));
        });
    });
});



$("#predict-button").click(function (event) {

    H = $("#optionH").val()
    A = $("#optionA").val()

    $.get("/pred?H=" + H + "&A=" + A, function (response) {


        response.p = Math.round(response.p*10)/10

        if(response.p<0){
            response.hVence = 1
            response.aVence = 0
            response.empate = 0
            response.resultado = response.H + " Vence"
            response.Hcolor = "mediumaquamarine"
        }

        if(response.p>0){
            response.hVence = 0
            response.aVence = 1
            response.empate = 0
            response.resultado = response.A + " Vence"
            response.Acolor = "mediumaquamarine"


        }

        if(response.p==0){
            response.hVence = 0
            response.aVence = 0
            response.empate = 1
            response.resultado = "Empate"
            response.Hcolor = "mediumaquamarine"
            response.Acolor = "mediumaquamarine"
        }

        response.p = Math.abs(response.p)

        $("#template").tmpl(response).appendTo("#table-predictions")

    })

})