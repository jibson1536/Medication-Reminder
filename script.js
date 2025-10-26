// Highlight the active navigation link automatically
document.addEventListener('DOMContentLoaded', () => {
    // Get the current page file name (e.g. "userflow.html")
    const currentPage = window.location.pathname.split('/').pop();
  
    // Get all navbar links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  
    navLinks.forEach(link => {
      const linkPage = link.getAttribute('href');
  
      // Check if the current link matches the page name
      if (linkPage === currentPage || (linkPage === 'index.html' && currentPage === '')) {
        // Remove active class from all links first
        navLinks.forEach(l => l.classList.remove('active', 'text-white', 'bg-dark', 'rounded-pill'));
  
        // Add active styling to the current link
        link.classList.add('active', 'text-white', 'bg-dark', 'rounded-pill');
      }
    });
  });
  