jQuery(document).ready(function ($) {
    $.getJSON('https://ipapi.co/json/', function (data) {
        
        isCurrencyChanged=Cookies.get('isCurrencyhanged')
        if (isCurrencyChanged){
            itisLang=Cookies.get('currency')
        }else{
            
            if (!Cookies.get("allCurrencyIsReady")){
                Cookies.set("currency", data.currency)
                $.getJSON("../../static/currency/currency.json", function(json) {
                    Cookies.set("allcurrencies", json)
                    Cookies.set("allCurrencyIsReady",true)
                });
            }
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
    Cookies.set("isCurrencyhanged", true)
    window.location.href=window.location.href;
}