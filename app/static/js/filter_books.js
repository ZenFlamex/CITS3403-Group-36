// JavaScript function to filter books based on the selected filter value
function filterBooks() {

    const filterValue = document.getElementById("book-filter-dropdown").value;

    const titleElement = document.querySelector('h1');
    titleElement.classList.add('hidden'); // fade out
    
    setTimeout(() => {
      titleElement.textContent = filterValue === '1' ? 'Favourite Books' : 'My Books';
      titleElement.classList.remove('hidden');
    }, 50);

    // Update the URL with the current filter
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('favourites', filterValue); 

    // Reload the page with the new URL to apply the filter
    window.location.href = currentUrl.toString();
}

// Function to update the active state of view mode buttons and dropdown filter when the page loads
function updateViewMode() {
    const urlParams = new URLSearchParams(window.location.search);
    const viewMode = urlParams.get('view') || 'card';
    const favourites = urlParams.get('favourites') || '0';  

    // Set the filter dropdown to the correct favourites value
    document.getElementById("book-filter-dropdown").value = favourites;

    // Update the page title based on the favourites filter
    const titleElement = document.querySelector('h1');
    titleElement.textContent = favourites === '1' ? 'Favourite Books' : 'My Books';
}

// Call the update function on page load to set the correct state
window.onload = function() {
    updateViewMode();
};
