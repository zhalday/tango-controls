function triggerRtdSearch() {
    const event = new CustomEvent("readthedocs-search-show");
    document.dispatchEvent(event);
    // Explicitly set text color to black to ensure it is visible in dark mode
    document.querySelector("readthedocs-search").shadowRoot.querySelector("div form input").style.color="black";
    // Default the 'Include subproject' checkbox to true
    document.querySelector("readthedocs-search").shadowRoot.querySelector("div ul li input").checked=true
}

document.addEventListener("DOMContentLoaded", function(event) {
    const original_search = document.querySelector("button.btn.search-button-field.search-button__button.pst-js-only");
    var new_search = original_search.cloneNode(true);
    original_search.parentNode.replaceChild(new_search, original_search);
    new_search.addEventListener("click", (e) => {
        triggerRtdSearch();
    });

    document.addEventListener('keydown', (e) => {
        // Check if we are using a mac
        var useCommandKey = navigator.platform.indexOf("Mac") === 0 || navigator.platform === "iPhone";
        var metaKeyUsed = useCommandKey ? e.metaKey && !e.ctrlKey : !e.metaKey && e.ctrlKey;
        if (metaKeyUsed && e.key === "k" && !e.shiftKey && !e.altKey) {
            if (document.contains(document.getElementById("pst-search-dialog"))) {
                // Suppress the pydata default search bar
                document.getElementById("pst-search-dialog").style.visibility="hidden";
                document.getElementById("pst-search-dialog").close();
            }
            triggerRtdSearch();
        }
    });
});
