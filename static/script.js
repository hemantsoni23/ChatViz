document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.getElementById('file-input');

  fileInput.addEventListener('change', function () {
      const selectedFile = fileInput.files[0];

      if (selectedFile) {
          const formData = new FormData();
          formData.append('file', selectedFile);
          fetch('/upload', {
              method: 'POST',
              body: formData
          })
          .then(response => response.text())
          .then(data => {
              window.location.href = '/analysis';
          })
          .catch(error => {
              console.error('Error:', error);
          });
      }
  });
});

const mainNavItems = document.querySelectorAll('.nav-item');
mainNavItems.forEach((mainNavItem) => {
    const subnav = mainNavItem.querySelector('.subnav');
    mainNavItem.addEventListener('click', () => {
        subnav.classList.toggle('hidden');
    });
});

