// Toggle visibility of elements
function toggleVisibility(id) {
    var el = document.getElementById(id);
 
    if (el.style.visibility=="visible") {
           el.style.visibility="hidden";
    }
    else {
           el.style.visibility="visible";
    }
}

// Active visibility of elements based on checkbox
function activeVisibility(id_status, id) {
    var elStatus = document.getElementById(id_status);
    var el = document.getElementById(id);
    console.log("This is a tests", elStatus.checked);
 
    if (elStatus.checked) {
           el.style.visibility="visible";
    }
    else {
           el.style.visibility="hidden";
    }
}