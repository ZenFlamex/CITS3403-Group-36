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