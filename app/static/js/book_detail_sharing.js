// Check if the necessary input element exists (relevant for owner view)
if (document.getElementById('user-search-input')) {
    document.addEventListener('DOMContentLoaded', function() {
        // Get references to the necessary HTML elements
        const searchInput = document.getElementById('user-search-input');
        const resultsContainer = document.getElementById('user-search-results');
        const selectedUserIdInput = document.getElementById('selected-user-id');
        const selectedUserInfo = document.getElementById('selected-user-info');
        const shareSubmitButton = document.getElementById('share-submit-btn');
        // Read the book ID from the data attribute on the search input
        const bookId = searchInput.dataset.bookId;
        let searchTimeout; 

        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout); 
            const query = searchInput.value.trim(); 

            // Reset selection and results when input changes
            selectedUserIdInput.value = '';
            selectedUserInfo.textContent = 'No user selected.';
            shareSubmitButton.disabled = true;
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';

            // Don't search if the query is too short
            if (query.length < 1) {
                return;
            }

            // Debounce: Wait 300ms after typing stops before sending request
            searchTimeout = setTimeout(() => {
                fetch(`/users/search?q=${encodeURIComponent(query)}&book_id=${bookId}`)
                    .then(response => {
                     
                        if (!response.ok) {
                            throw new Error('Network response error');
                        }
                        return response.json(); 
                    })
                    .then(users => {
                        resultsContainer.innerHTML = ''; 
                        if (users.length > 0) {
                            // If users are found, create list items for each
                            users.forEach(user => {
                                const userItem = document.createElement('a');
                                userItem.href = '#'; 
                                userItem.classList.add('list-group-item', 'list-group-item-action');
                                userItem.textContent = user.username; 
                                userItem.dataset.userId = user.id;    
                                userItem.dataset.username = user.username;

                                
                                userItem.addEventListener('click', function(event) {
                                    event.preventDefault(); 
                                 
                                    selectedUserIdInput.value = this.dataset.userId;
                                    selectedUserInfo.textContent = `Selected: ${this.dataset.username}`;
                                    searchInput.value = this.dataset.username; 
                                    shareSubmitButton.disabled = false; 
                                    resultsContainer.innerHTML = ''; 
                                    resultsContainer.style.display = 'none'; 
                                });
                                resultsContainer.appendChild(userItem); 
                            });
                             resultsContainer.style.display = 'block'; 
                        } else {
                             // If no users found, display a message
                             resultsContainer.innerHTML = '<div class="list-group-item disabled">No matching users found.</div>';
                             resultsContainer.style.display = 'block'; 
                        }
                    })
                    .catch(error => {
                        // Handle errors during the fetch operation
                        console.error('Error searching users:', error);
                        resultsContainer.innerHTML = '<div class="list-group-item text-danger">Error searching users.</div>';
                        resultsContainer.style.display = 'block'; 
                    });
            }, 300); // 300ms delay for debounce
        });

        document.addEventListener('click', function(event) {
            // Check if the click was inside the search input or the results container
            const isClickInsideSearch = searchInput.contains(event.target) || resultsContainer.contains(event.target);
            if (!isClickInsideSearch) {
                // If click was outside, hide the results
                resultsContainer.style.display = 'none';
            }
        });

        // Add event listener for clearing the search input (e.g., clicking the 'x')
        searchInput.addEventListener('search', function() {
             if (!searchInput.value) {
                 selectedUserIdInput.value = '';
                 selectedUserInfo.textContent = 'No user selected.';
                 shareSubmitButton.disabled = true;
                 resultsContainer.innerHTML = '';
                 resultsContainer.style.display = 'none';
             }
        });
    }); 
} 