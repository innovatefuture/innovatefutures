"use strict";
const visible = 'block';
const hidden = 'hidden';
const initial = document.getElementById("initial-list");
const results = document.getElementById("search-results");
const searchbar = document.getElementById("searchbar");
const order_by = document.getElementById("orderby");
let flipped = false;
/*
order_by.addEventListener('input', function (evt) {
    if (flipped) {
        searching(true);
    } else {
        
    }
}

searchbar.addEventListener('input', function (evt) {
    if (searchbar.value.length > 2) {
        searching(true)
    } else {
        flipped = false
        searching(false)
    }

});

function searching(displayResults: boolean) {
    if (initial != null && results != null) {
        if (!flipped) {
            if (displayResults) {
                initial.classList.value = hidden
                results.classList.value = visible
                flipped = true
            } else {
                initial.classList.value = visible
                results.classList.value = hidden
                results.innerHTML = ''
            }
        }
    }
}
*/
function buttonTagSearch(tag) {
    searchbar.value = tag;
    console.log('search');
    //searching(true)
}
function setResultCount(count) {
    let elem = document.getElementById("result-count");
    if (elem != null) {
        if (count == 1) {
            elem.innerHTML = count.toString() + " result available";
        }
        else {
            elem.innerHTML = count.toString() + " results available";
        }
    }
}
