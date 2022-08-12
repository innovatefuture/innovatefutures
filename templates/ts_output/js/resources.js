"use strict";
var visible = 'block';
var hidden = 'hidden';
var initial = document.getElementById("initial");
var results = document.getElementById("results");
var searchbar = document.getElementById("searchbar");
var flipped = false;
searchbar.addEventListener('input', function (evt) {
    if (searchbar.value.length > 2) {
        searching(true);
    }
    else {
        flipped = false;
        searching(false);
    }
});
function searching(displayResults) {
    if (initial != null && results != null) {
        if (!flipped) {
            if (displayResults) {
                initial.classList.value = hidden;
                results.classList.value = visible;
                flipped = true;
            }
            else {
                initial.classList.value = visible;
                results.classList.value = hidden;
                results.innerHTML = '';
            }
        }
    }
}
