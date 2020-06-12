function  filterSelection(c){
    if(c=="all"){
        $("#cars-lits .sport").fadeIn();
        $("#cars-lits .business").fadeIn();
        $("#cars-lits .full-size").fadeIn();
        $("#cars-lits .minivan").fadeIn();
        $("#cars-lits .economy").fadeIn();
    }else{
    $("#cars-lits .sport").fadeOut();
    $("#cars-lits .business").fadeOut();
    $("#cars-lits .full-size").fadeOut();
    $("#cars-lits .minivan").fadeOut();
    $("#cars-lits .economy").fadeOut();
    $("#cars-lits ."+c).fadeIn();

    }
}