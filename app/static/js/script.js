// Simple JavaScript for future functionality
$(document).ready(function() {
    console.log('Book Tracker initialized');
    
    // Example function for future use
    function togglePrivacy() {
        // Code to toggle book privacy via AJAX
    }

        // Profile Picture Change functionality
        const fileInput = document.getElementById('profilePictureInput');
        const profileContainer = document.getElementById('profilePictureContainer');
    
        profileContainer.addEventListener('click', () => fileInput.click());
    
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                document.getElementById('profileForm').submit();
            }
        });
    
        fileInput.addEventListener('click', function () {
            this.value = '';
        });
});