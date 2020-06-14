jQuery(document).ready(function ($) {
    $.getJSON('https://ipapi.co/json/', function (data) {

        var isCurrencyChanged = Cookies.get('isCurrencyChanged')

        var currencyvalue=Cookies.get("currencyvalue");
        if (!isCurrencyChanged) {
            console.log("if (!isCurrencyChanged) {");
            $.getJSON('https://ipapi.co/json/', function (data) {
                Cookies.set("currency", data.currency)
                if(currencyvalue==null){
                    $.getJSON("../../static/currency/currency.json", function(json) {
                        $.each(json, function(index, value) {
                            if(value[0]==data.currency){
                                Cookies.set("currencyvalue", value[1])
                            }
                        }); 
                        
                    });

                }
              
                Cookies.set("isCurrencyChanged", true)
            });
        } 

    });
});

function filterSelection(c) {
    if (c == "all") {
        $("#cars-lits .sport").fadeIn();
        $("#cars-lits .business").fadeIn();
        $("#cars-lits .full-size").fadeIn();
        $("#cars-lits .minivan").fadeIn();
        $("#cars-lits .economy").fadeIn();
    } else {
        $("#cars-lits .sport").fadeOut();
        $("#cars-lits .business").fadeOut();
        $("#cars-lits .full-size").fadeOut();
        $("#cars-lits .minivan").fadeOut();
        $("#cars-lits .economy").fadeOut();
        $("#cars-lits ." + c).fadeIn();
    }
}


function changethemoney() {
    var currency = $("#money .currency").val();
    var res = currency.split("/");
    Cookies.set("currency", res[0])
    Cookies.set("currencyvalue", res[1])
    Cookies.set("isCurrencyChanged", true)
    window.location.href = window.location.href;
}