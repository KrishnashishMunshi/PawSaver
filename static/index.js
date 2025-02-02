// Mobile menu toggle
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');
const menuIcon = document.getElementById('menu-icon');
const closeIcon = document.getElementById('close-icon');
let isOpen = false;

mobileMenuButton.addEventListener('click', () => {
    isOpen = !isOpen;
    if (isOpen) {
        mobileMenu.classList.remove('hidden');
        menuIcon.classList.add('hidden');
        closeIcon.classList.remove('hidden');
    } else {
        mobileMenu.classList.add('hidden');
        menuIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
    }
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.classList.remove('shadow-lg');
        navbar.classList.add('shadow-md');
        return;
    }

    if (currentScroll > lastScroll) {
        // Scrolling down
        navbar.classList.add('-translate-y-full');
    } else {
        // Scrolling up
        navbar.classList.remove('-translate-y-full');
        navbar.classList.add('shadow-lg');
    }

    lastScroll = currentScroll;
});

// Close mobile menu on window resize
window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
        mobileMenu.classList.add('hidden');
        menuIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
        isOpen = false;
    }
});