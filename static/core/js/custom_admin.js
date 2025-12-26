(function () {
    'use strict';
    
    console.log('🔧 Responsive Sidebar Fix Loading...');

    const MOBILE_BREAKPOINT = 1024;
    const SIDEBAR_WIDTH = '280px';
    
    let state = {
        initialized: false,
        isOpen: false,
        elements: {
            sidebar: null,
            overlay: null,
            toggleBtn: null
        }
    };

    // Check if we should use mobile mode
    function isMobileMode() {
        return window.innerWidth <= MOBILE_BREAKPOINT;
    }

    // Clean up everything for desktop mode
    function cleanupForDesktop() {
        console.log('🖥️ Switching to desktop mode');
        
        if (state.elements.overlay) {
            state.elements.overlay.remove();
        }
        
        if (state.elements.sidebar) {
            state.elements.sidebar.removeAttribute('style');
        }
        
        document.body.style.overflow = '';
        document.body.classList.remove('sidebar-open');
        
        state = {
            initialized: false,
            isOpen: false,
            elements: { sidebar: null, overlay: null, toggleBtn: null }
        };
    }

    // Close the sidebar
    function closeSidebar() {
        if (!state.elements.sidebar || !state.isOpen) return;
        
        state.elements.sidebar.style.transform = 'translateX(-100%)';
        state.elements.overlay.style.opacity = '0';
        
        setTimeout(() => {
            if (state.elements.overlay) {
                state.elements.overlay.style.display = 'none';
            }
            document.body.style.overflow = '';
            document.body.classList.remove('sidebar-open');
        }, 300);
        
        state.isOpen = false;
        console.log('✖️ Sidebar closed');
    }

    // Open the sidebar
    function openSidebar() {
        if (!state.elements.sidebar || state.isOpen) return;
        
        state.elements.overlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
        document.body.classList.add('sidebar-open');
        
        // Force reflow for animation
        state.elements.overlay.offsetHeight;
        
        state.elements.overlay.style.opacity = '1';
        state.elements.sidebar.style.transform = 'translateX(0)';
        
        state.isOpen = true;
        console.log('✓ Sidebar opened');
    }

    // Toggle sidebar
    function toggleSidebar(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        if (state.isOpen) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }

    // Initialize mobile sidebar
    function initMobileSidebar() {
        if (state.initialized) return;

        // Find elements
        const sidebar = document.querySelector('.main-sidebar');
        const toggleBtn = document.querySelector('[data-widget="pushmenu"]');

        if (!sidebar || !toggleBtn) {
            console.warn('⏳ Sidebar elements not found, retrying...');
            setTimeout(initMobileSidebar, 300);
            return;
        }

        console.log('📱 Initializing mobile sidebar');

        // Store elements
        state.elements.sidebar = sidebar;
        state.elements.toggleBtn = toggleBtn;

        // Reset sidebar classes
        sidebar.className = 'main-sidebar';
        sidebar.removeAttribute('data-widget');

        // Style the sidebar for mobile
        sidebar.style.cssText = `
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: ${SIDEBAR_WIDTH} !important;
            height: 100vh !important;
            height: 100dvh !important;
            z-index: 1000000 !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            display: block !important;
            transform: translateX(-100%) !important;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 2px 0 8px rgba(0,0,0,0.15) !important;
            -webkit-overflow-scrolling: touch !important;
        `;

        // Create overlay if it doesn't exist
        if (!state.elements.overlay) {
            const overlay = document.createElement('div');
            overlay.id = 'mobile-sidebar-overlay';
            overlay.style.cssText = `
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.6);
                z-index: 999999;
                opacity: 0;
                transition: opacity 0.3s ease;
                -webkit-tap-highlight-color: transparent;
            `;
            document.body.appendChild(overlay);
            state.elements.overlay = overlay;

            // Close on overlay click
            overlay.addEventListener('click', closeSidebar);
        }

        // Replace toggle button to remove old event listeners
        const newToggleBtn = toggleBtn.cloneNode(true);
        toggleBtn.parentNode.replaceChild(newToggleBtn, toggleBtn);
        state.elements.toggleBtn = newToggleBtn;
        
        newToggleBtn.addEventListener('click', toggleSidebar);

        // Close sidebar when clicking links
        sidebar.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                if (state.isOpen) {
                    setTimeout(closeSidebar, 150);
                }
            });
        });

        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && state.isOpen && isMobileMode()) {
                closeSidebar();
            }
        });

        state.initialized = true;
        console.log('✅ Mobile sidebar initialized');
    }

    // Main check function
    function checkMode() {
        if (isMobileMode()) {
            if (!state.initialized) {
                initMobileSidebar();
            }
        } else {
            if (state.initialized) {
                cleanupForDesktop();
            }
        }
    }

    // Debounced resize handler
    let resizeTimeout;
    function handleResize() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const wasMobile = state.initialized;
            const isMobile = isMobileMode();
            
            if (wasMobile !== isMobile) {
                checkMode();
            }
        }, 250);
    }

    // Initialize
    function init() {
        if (isMobileMode()) {
            setTimeout(checkMode, 500);
        }
        
        window.addEventListener('resize', handleResize);
        window.addEventListener('orientationchange', () => {
            setTimeout(checkMode, 300);
        });
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => setTimeout(init, 200));
    } else {
        setTimeout(init, 200);
    }

    console.log('✅ Sidebar fix loaded');
})();