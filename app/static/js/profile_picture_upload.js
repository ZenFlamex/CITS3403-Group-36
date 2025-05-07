    // Profile Picture Change functionality
    const fileInput = document.getElementById('profilePictureInput');
    const profileForm = document.getElementById('profileForm');
    const resetForm = document.getElementById('resetForm');
    const profileContainer = document.getElementById('profilePictureContainer');
  
    const modal = document.getElementById('profileOptionModal');
    const uploadBtn = document.getElementById('uploadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const closeModal = document.getElementById('closeModal');
  
    profileContainer.addEventListener('click', () => {
      modal.style.display = 'flex';
    });
  
    uploadBtn.addEventListener('click', () => {
      modal.style.display = 'none';
      fileInput.value = ''; // Reset so same file can be uploaded again
      fileInput.click();
    });
  
    resetBtn.addEventListener('click', () => {
      modal.style.display = 'none';
      resetForm.submit();
    });
  
    closeModal.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        profileForm.submit();
      }
    });