document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const searchInput = document.getElementById('book-search');
    const searchButton = document.getElementById('search-button');
    const searchResults = document.getElementById('search-results');
    const bookForm = document.getElementById('book-form');
    const clearFormButton = document.getElementById('clear-form');
    const coverPreview = document.getElementById('cover-preview');
    
    // Form inputs
    const titleInput = document.querySelector('#title');
    const authorInput = document.querySelector('#author');
    const openlibraryIdInput = document.querySelector('#openlibrary_id');
    const coverImageInput = document.querySelector('#cover_image');
    const statusSelect = document.querySelector('#status');
    const currentPageInput = document.querySelector('#current_page');
    const totalPagesInput = document.querySelector('#total_pages');
    const endDateInput = document.querySelector('#end_date');
    const currentPageField = document.querySelector('.current-page-field');
    const endDateField = document.querySelector('.end-date-field');
    
    // Default cover image
    const defaultCoverImage = coverPreview.src;
    
    // variable to keep track if a book is selected from api
    let selectedBookInfo = null;
    let currentPage = 1;
    const resultsPerPage = 5;
    
    // Event listeners
    searchButton.addEventListener('click', () => performSearch(true));
    searchInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch(true);
        }
    });
    clearFormButton.addEventListener('click', clearForm);
    statusSelect.addEventListener('change', updateFormVisibility);
    currentPageInput.addEventListener('input', validatePages);
    totalPagesInput.addEventListener('input', validatePages);
    
    // Apply blur validation to relevant form fields (if we click and click out)
    bookForm.querySelectorAll('input, select').forEach(field => {
        field.addEventListener('blur', function() {
            if (this.offsetParent !== null) {
                validateField(this);
            }
        });
    });
    
    // Form submission validation
    bookForm.addEventListener('submit', function(e) {
        let isValid = true;
        
        bookForm.querySelectorAll('input, select').forEach(field => {
            if (field.offsetParent !== null && field.type !== 'hidden' && !field.classList.contains('form-check-input')) {
                if (!validateField(field)) {
                    isValid = false;
                }
            }
        });
        
        if (currentPageInput.offsetParent !== null && !validatePages()) {
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
            if (selectedBookInfo) {
                restoreBookInfo();
            }
        }
    });
    
    // Search OpenLibrary API
    function performSearch(resetResults = true) {
        const searchTerm = searchInput.value.trim();
        
        if (!searchTerm) {
            showSearchError('Please enter a search term');
            return;
        }
        
        // If starting a new search, reset search results
        if (resetResults) {
            currentSearchTerm = searchTerm;
            currentPage = 1;
            searchResults.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><div class="mt-2">Searching...</div></div>';
        } else {
            // Add loading indicator at the bottom
            const loadingIndicator = document.createElement('div');
            loadingIndicator.id = 'load-more-spinner';
            loadingIndicator.innerHTML = '<div class="text-center py-2"><div class="spinner-border spinner-border-sm text-primary" role="status"></div><span class="ms-2">Loading more...</span></div>';
            searchResults.appendChild(loadingIndicator);
        }
        
        isLoading = true;
        
        const isISBN = /^[0-9]{10,13}$/.test(searchTerm);
        const apiUrl = isISBN
            ? `https://openlibrary.org/api/books?bibkeys=ISBN:${searchTerm}&format=json&jscmd=data`
            : `https://openlibrary.org/search.json?q=${encodeURIComponent(searchTerm)}&limit=${resultsPerPage}&page=${currentPage}`;
            
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                isLoading = false;
                if (isISBN) {
                    displayISBNResults(data, searchTerm);
                } else {
                    displaySearchResults(data, resetResults);
                }
            })
            .catch(error => {
                isLoading = false;
                console.error('Error searching OpenLibrary:', error);
                if (resetResults) {
                    showSearchError('Error searching OpenLibrary. Please try again or enter details manually.');
                } else {
                    // Remove the loading spinner
                    const spinner = document.getElementById('load-more-spinner');
                    if (spinner) spinner.remove();
                    
                    // Show error at the bottom
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'alert alert-warning mt-2';
                    errorDiv.textContent = 'Failed to load more results. Please try again.';
                    searchResults.appendChild(errorDiv);
                }
            });
    }
    
    // Display search results
    function displaySearchResults(data, resetResults = true) {
        // Remove loading spinner if it exists
        const spinner = document.getElementById('load-more-spinner');
        if (spinner) spinner.remove();
        
        if (!data.docs || data.docs.length === 0) {
            if (resetResults) {
                showSearchError('No books found. Please try another search term or enter details manually.');
            } else {
                const noMoreDiv = document.createElement('div');
                noMoreDiv.className = 'alert alert-info mt-2';
                noMoreDiv.textContent = 'No more results available.';
                searchResults.appendChild(noMoreDiv);
            }
            return;
        }
        
        if (resetResults) {
            searchResults.innerHTML = '<div class="list-group"></div>';
        }
        
        // Get the list-group element
        let resultsGroup = searchResults.querySelector('.list-group');
        if (!resultsGroup) {
            resultsGroup = document.createElement('div');
            resultsGroup.className = 'list-group';
            searchResults.appendChild(resultsGroup);
        }
        
        // Append new results
        data.docs.forEach(book => {
            const title = book.title || 'Unknown Title';
            const authors = book.author_name ? book.author_name.join(', ') : 'Unknown Author';
            const year = book.first_publish_year || 'Unknown Year';
            const key = book.key;
            
            const coverImg = book.cover_i
                ? `<img src="https://covers.openlibrary.org/b/id/${book.cover_i}-M.jpg" class="search-result-cover" alt="Cover">`
                : '<div class="no-cover"><i class="bi bi-book"></i></div>';
            
            const resultItem = document.createElement('a');
            resultItem.href = '#';
            resultItem.className = 'list-group-item list-group-item-action book-result';
            resultItem.setAttribute('data-key', key);
            resultItem.setAttribute('data-title', title);
            resultItem.setAttribute('data-author', authors);
            resultItem.innerHTML = `
                <div class="d-flex">
                    <div class="flex-shrink-0 me-3">${coverImg}</div>
                    <div class="flex-grow-1">
                        <h5 class="mb-1">${title}</h5>
                        <p class="mb-1">Author: ${authors}</p>
                        <small>Published: ${year}</small>
                    </div>
                </div>
            `;
            resultsGroup.appendChild(resultItem);
            
            resultItem.addEventListener('click', function(e) {
                e.preventDefault();
                fetchBookDetails(this.getAttribute('data-key'));
            });
        });
        
        
        currentPage++;
        
        // Add "Load More" button if there are more results to load
        if (data.docs.length >= resultsPerPage) {
            const loadMoreButton = document.createElement('button');
            loadMoreButton.className = 'btn btn-outline-primary w-100 mt-2';
            loadMoreButton.textContent = 'Load More Results';
            loadMoreButton.id = 'load-more-button';
            searchResults.appendChild(loadMoreButton);
            
            loadMoreButton.addEventListener('click', function() {
                this.remove(); 
                performSearch(false); 
            });
        }
    }
    
    // Display ISBN search results
    function displayISBNResults(data, isbn) {
        const key = `ISBN:${isbn}`;
        if (!data[key]) {
            showSearchError('No book found with that ISBN. Please try another search or enter details manually.');
            return;
        }
        
        const book = data[key];
        populateFormFromBook({
            title: book.title,
            authors: book.authors ? book.authors.map(a => a.name).join(', ') : 'Unknown',
            cover: book.cover ? book.cover.medium : null,
            key: key
        });
    }
    
    // Fetch detailed book info
    function fetchBookDetails(key) {
        searchResults.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><div class="mt-2">Loading book details...</div></div>';
        
        fetch(`https://openlibrary.org${key}.json`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(bookData => {
                if (bookData.authors && bookData.authors.length > 0) {
                    const authorPromises = bookData.authors.map(author => {
                        return fetch(`https://openlibrary.org${author.author.key}.json`)
                            .then(response => response.json())
                            .then(authorData => authorData.name)
                            .catch(() => 'Unknown Author');
                    });
                    
                    Promise.all(authorPromises).then(authorNames => {
                        populateFormFromBook({
                            title: bookData.title,
                            authors: authorNames.join(', '),
                            cover: bookData.covers ? `https://covers.openlibrary.org/b/id/${bookData.covers[0]}-M.jpg` : null,
                            pages: bookData.number_of_pages || 0,
                            key: key
                        });
                    });
                } else {
                    populateFormFromBook({
                        title: bookData.title,
                        authors: 'Unknown Author',
                        cover: bookData.covers ? `https://covers.openlibrary.org/b/id/${bookData.covers[0]}-M.jpg` : null,
                        pages: bookData.number_of_pages || 0,
                        key: key
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching book details:', error);
                showSearchError('Error loading book details. Please try again or enter details manually.');
            });
    }
    
    // Populate form with book data
    function populateFormFromBook(bookInfo) {
        selectedBookInfo = bookInfo;
        
        titleInput.value = bookInfo.title;
        authorInput.value = bookInfo.authors;
        openlibraryIdInput.value = bookInfo.key;
        
        if (bookInfo.pages && totalPagesInput) {
            totalPagesInput.value = bookInfo.pages;
        }
        
        if (bookInfo.cover) {
            coverImageInput.value = bookInfo.cover;
            coverPreview.src = bookInfo.cover;
        } else {
            coverImageInput.value = '';
            coverPreview.src = defaultCoverImage;
        }
        
        titleInput.readOnly = true;
        authorInput.readOnly = true;
        
        searchResults.innerHTML = `
            <div class="alert alert-success">
                <strong>"${bookInfo.title}"</strong> selected! Complete the remaining details below.
                <button type="button" class="btn-close float-end" id="clear-selection"></button>
            </div>
        `;
        
        document.getElementById('clear-selection').addEventListener('click', function() {
            clearForm();
            searchResults.innerHTML = '';
        });
        
        updateFormVisibility();
    }
    
    // Restore book info after validation failure
    function restoreBookInfo() {
        if (!selectedBookInfo) return;
        
        titleInput.readOnly = true;
        authorInput.readOnly = true;
        
        if (selectedBookInfo.cover) {
            coverPreview.src = selectedBookInfo.cover;
        }
        
        searchResults.innerHTML = `
            <div class="alert alert-success">
                <strong>"${selectedBookInfo.title}"</strong> selected! Complete the remaining details below.
                <button type="button" class="btn-close float-end" id="clear-selection"></button>
            </div>
        `;
        
        document.getElementById('clear-selection').addEventListener('click', function() {
            clearForm();
            searchResults.innerHTML = '';
        });
    }
    
    // Show search error message
    function showSearchError(message) {
        searchResults.innerHTML = `
            <div class="alert alert-warning">
                ${message}
            </div>
        `;
    }
    

// VALIDATE FORM FIELDS

    // Clear form fields and reset state
    function clearForm() {
        // Reset the form
        bookForm.reset();
        
        // Clear text inputs
        titleInput.value = '';
        authorInput.value = '';
        searchInput.value = '';
        openlibraryIdInput.value = '';
        coverImageInput.value = '';
        currentPageInput.value = '';
        totalPagesInput.value = '';
        
        // Reset date fields
        document.querySelector('#start_date').value = '';
        document.querySelector('#end_date').value = '';
        
        // Reset selects to default values
        document.querySelector('#genre').selectedIndex = 0;
        document.querySelector('#status').selectedIndex = 0;
        document.querySelector('#rating').selectedIndex = 0;
        
        // Reset checkboxes
        document.querySelector('#is_public').checked = false;
        document.querySelector('#is_favorite').checked = false;
        
        // Reset UI state
        titleInput.readOnly = false;
        authorInput.readOnly = false;
        
        coverPreview.src = defaultCoverImage;
        searchResults.innerHTML = '';
        
        selectedBookInfo = null;
        
        clearValidationErrors();
        updateFormVisibility();
    }
    
    // Clear all validation errors
    function clearValidationErrors() {
        document.querySelectorAll('.validation-error').forEach(el => el.remove());
        document.querySelectorAll('.is-invalid').forEach(field => field.classList.remove('is-invalid'));
    }
    
    function updateFormVisibility() {
        const status = statusSelect.value;

        if (status === 'Completed') {
            endDateField.style.display = 'block';
            currentPageField.style.display = 'none';
            if (totalPagesInput.value) {
                currentPageInput.value = totalPagesInput.value;
            }
            currentPageInput.disabled = true;
        } else {
            endDateField.style.display = 'none';
            currentPageField.style.display = 'block';
            endDateInput.value = '';
            currentPageInput.disabled = false;
        }
        
        const ratingField = document.querySelector('.rating-field');
        const ratingSelect = document.querySelector('#rating');

        if (ratingField && ratingSelect) {
            if (status === 'In Progress') {
                ratingField.style.display = 'none';
                ratingSelect.value = "0"; // Set to 0 for In Progress
                ratingSelect.disabled = true;
            } else {
                ratingField.style.display = 'block';
                ratingSelect.disabled = false;
                
                // If switching back to a rated status, ensure a valid rating is selected
                if (ratingSelect.value === "0") {
                    ratingSelect.value = "";
                }
            }
        }
        
        bookForm.querySelectorAll('input, select').forEach(field => {
            if (field.offsetParent === null) {
                removeValidationError(field);
            }
            
        });
    }
    
    function validatePages() {
        if (currentPageField.style.display === 'none') {
            return true;
        }

        const currentPage = parseInt(currentPageInput.value);
        const totalPages = parseInt(totalPagesInput.value);
        
        removeValidationError(currentPageInput);
        
        if (statusSelect.value !== 'Completed' && currentPageField.style.display !== 'none' && 
            (!currentPageInput.value || currentPageInput.value.trim() === '')) {
            addValidationError(currentPageInput, 'This field is required');
            return false;
        }
        
        if (isNaN(currentPage) || isNaN(totalPages)) {
            return true;
        }
        
        if (currentPage > totalPages) {
            addValidationError(currentPageInput, 'Current page cannot be greater than total pages');
            return false;
        }
        
        return true;
    }
    
    // Validate individual field
    function validateField(field) {
        removeValidationError(field);
        
        if (field.type === 'hidden' || field.type === 'checkbox' || field.readOnly || 
            field.offsetParent === null || field.disabled) {
            return true;
        }
        
        // Special handling for rating field
        if (field.id === 'rating') {
            // For In Progress, we don't need to validate the rating
            if (statusSelect.value === 'In Progress') {
                return true;
            }
            
            // For other statuses, rating is required
            if (!field.value) {
                addValidationError(field, 'Please select a rating');
                return false;
            }
        } else if (!field.value.trim()) {
            addValidationError(field, 'This field is required');
            return false;
        }
        
        return true;
    }
    
    // Add validation error to field
    function addValidationError(field, message) {
        field.classList.add('is-invalid');
        
        const existingError = field.parentNode.querySelector('.validation-error');
        if (existingError) {
            existingError.textContent = message;
            return;
        }
        
        const errorElement = document.createElement('div');
        errorElement.className = 'text-danger validation-error';
        errorElement.textContent = message;
        
        field.parentNode.insertBefore(errorElement, field.nextSibling);
    }
    
    // Remove validation error from field
    function removeValidationError(field) {
        field.classList.remove('is-invalid');
        
        const errorElement = field.parentNode.querySelector('.validation-error');
        if (errorElement) {
            errorElement.remove();
        }
    }
    
    
    updateFormVisibility();
});