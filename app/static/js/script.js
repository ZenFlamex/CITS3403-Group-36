function setupNotificationClickHandlers() {
    console.log('Plain JS: Setting up notification click handlers.');

    const notificationItems = document.querySelectorAll('.notification-item');
    console.log('Plain JS: Found .notification-item elements:', notificationItems.length);

    if (notificationItems.length > 0) {
        notificationItems.forEach(item => {
            item.addEventListener('click', function(event) {
                console.log('Plain JS: Click detected on item:', item);

                const notificationItem = item; 
                const notificationId = notificationItem.dataset.notificationId; 
                const targetLink = notificationItem.dataset.targetLink;     

                if (!notificationItem.classList.contains('unread')) {
                    console.log(`Notification ${notificationId} is already read. Navigating if link exists.`);
                    
                    if (!targetLink) {
                         event.preventDefault(); 
                    }
                    return; 
                }

                console.log(`Notification ${notificationId} is unread. Preventing default navigation.`);
                event.preventDefault();

                console.log(`Marking notification ${notificationId} as read via fetch...`);

                const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
                const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : null;
                const headers = {
                    'Content-Type': 'application/json' 
                };
                 if (csrfToken) {
                     headers['X-CSRFToken'] = csrfToken;
                     console.log("CSRF Token Added to fetch header.");
                 } else {
                     console.warn("CSRF Token meta tag not found!");
                 }
              
                fetch(`/notifications/${notificationId}/read`, {
                    method: 'POST',
                    headers: headers
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        console.log(`Notification ${notificationId} successfully marked as read by server. Removing item from dropdown.`);

                        const listItem = notificationItem.closest('li'); 
                        if (listItem) {
                            const nextSibling = listItem.nextElementSibling; 
                            listItem.remove(); 
                            console.log("Notification <li> item removed from DOM.");

                            if (nextSibling && nextSibling.firstElementChild && nextSibling.firstElementChild.tagName === 'HR' && nextSibling.firstElementChild.classList.contains('dropdown-divider')) {
                                nextSibling.remove();
                                console.log("Associated divider removed from DOM.");
                            }
                        } else {
                            console.warn("Could not find parent <li> to remove for notificationItem. Removing the item itself as a fallback.");
                            notificationItem.remove();
                        }
                        const badge = document.getElementById('notification-count-badge');
                        if (badge) {
                            let currentCount = parseInt(badge.textContent);
                            if (!isNaN(currentCount) && currentCount > 0) {
                                currentCount--;
                                badge.textContent = currentCount;
                                console.log("Navbar badge count updated to:", currentCount);
                                if (currentCount === 0) {
                                    badge.remove();
                                    console.log("Navbar badge removed.");
                                }
                            }
                        } else {
                            console.log("Navbar badge element (#notification-count-badge) not found.");
                        }

                        if (targetLink) {
                            console.log("Navigating to target link:", targetLink);
                            window.location.href = targetLink;
                        }
                    } else {
                        console.error(`Server responded failure for notification ${notificationId}:`, data.message || 'Unknown error');
                        if (targetLink) { window.location.href = targetLink; }
                    }
                })
                .catch(error => {
                    console.error(`Workspace Error marking notification ${notificationId} as read:`, error);
                    if (targetLink) { window.location.href = targetLink; }
                });
            });
        });
        console.log('Plain JS: Click listeners attached directly to items.');
    } else {
        console.log('Plain JS: No .notification-item elements found to attach listeners.');
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupNotificationClickHandlers);
} else {
    setupNotificationClickHandlers();
}

if (window.jQuery) {
     $(document).ready(function() {
         console.log('jQuery ready also fired.');
     });
} else {
     console.log('jQuery ($) is not defined when script runs.');
}

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
