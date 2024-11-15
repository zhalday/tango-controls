document.addEventListener("DOMContentLoaded", function(event) {
const original_search = document.querySelector("button.btn.search-button-field.search-button__button.pst-js-only");
var new_search = original_search.cloneNode(true);
original_search.parentNode.replaceChild(new_search, original_search);
new_search.addEventListener("click", (e) => {
        const event = new CustomEvent("readthedocs-search-show");
        document.dispatchEvent(event);
    });
});

