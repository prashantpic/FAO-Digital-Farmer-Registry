odoo.define('dfr_farmer_portal.portal_accessibility', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.DFRAccessibility = publicWidget.Widget.extend({
    selector: 'body', // Apply globally or to a more specific portal root element

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this._enhanceKeyboardNavigation();
        this._setupAriaLiveRegions(); // Ensure regions are ready
        // Call other accessibility enhancements here
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    _enhanceKeyboardNavigation: function () {
        // Implement "skip to main content" link functionality
        const skipLink = this.el.querySelector('.skip-to-main');
        const mainContent = this.el.querySelector('[role="main"]');

        if (skipLink && mainContent) {
            skipLink.addEventListener('click', function (event) {
                event.preventDefault();
                mainContent.setAttribute('tabindex', '-1'); // Make it focusable programmatically
                mainContent.focus();
                // Optional: Remove tabindex after focus if it's not normally focusable
                // mainContent.addEventListener('blur', () => mainContent.removeAttribute('tabindex'), { once: true });
            });
        }

        // Focus management for dynamic content (e.g., modals, revealed sections)
        // This is more of a pattern. Specific focus calls should be made from the JS
        // that shows/hides content. E.g., after an error message appears, focus it.
        // Example:
        // document.addEventListener('dfr-content-shown', function(event) {
        //     const target = event.detail.elementToShow;
        //     if (target) {
        //         const firstFocusable = target.querySelector('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        //         if (firstFocusable) {
        //             firstFocusable.focus();
        //         } else {
        //             target.setAttribute('tabindex', '-1');
        //             target.focus();
        //         }
        //     }
        // });
    },

    _setupAriaLiveRegions: function() {
        // This function could ensure necessary ARIA live regions exist in the DOM if not
        // hardcoded in templates, or simply serve as a reminder for their importance.
        // Example: If a global status message region is needed:
        // if (!document.getElementById('global-aria-live-status')) {
        //     const liveRegion = document.createElement('div');
        //     liveRegion.id = 'global-aria-live-status';
        //     liveRegion.className = 'sr-only'; // Visually hidden but read by screen readers
        //     liveRegion.setAttribute('aria-live', 'polite');
        //     liveRegion.setAttribute('aria-atomic', 'true');
        //     document.body.appendChild(liveRegion);
        // }
    },
    
    /**
     * Updates the content of a specified ARIA live region for screen reader announcements.
     * @param {string} regionId The ID of the ARIA live region element.
     * @param {string} message The message to announce.
     * @param {string} [politeness='polite'] The politeness setting ('polite' or 'assertive').
     */
    manageAriaLiveRegions: function (regionId, message, politeness = 'polite') {
        const liveRegion = document.getElementById(regionId);
        if (liveRegion) {
            // Ensure the region has the correct politeness setting if it's dynamic
            // liveRegion.setAttribute('aria-live', politeness); 
            liveRegion.textContent = message;

            // For 'assertive' or when immediate feedback is critical, sometimes a trick
            // is needed to ensure it's re-announced if message is the same.
            // if (politeness === 'assertive') {
            //    const originalContent = liveRegion.textContent;
            //    liveRegion.textContent = '';
            //    setTimeout(() => { liveRegion.textContent = originalContent; }, 50);
            // }
        } else {
            console.warn(`ARIA live region with ID '${regionId}' not found.`);
        }
    }
});

// Expose manageAriaLiveRegions globally or via a service if needed by other widgets
// For simplicity, other widgets can dispatch custom events that this widget listens to,
// or get an instance of this widget.
// Example of how another widget might call it:
// odoo.addons.dfr_farmer_portal.portal_accessibility.manageAriaLiveRegions('form-error-region', 'Invalid input.');

return {
    DFRAccessibility: publicWidget.registry.DFRAccessibility,
    // If you need to expose manageAriaLiveRegions for other modules:
    // manageAriaLiveRegions: publicWidget.registry.DFRAccessibility.prototype.manageAriaLiveRegions 
};

});

// Initialize accessibility features on document ready
// This ensures that even if no specific '.dfr-accessibility-widget' element is targeted,
// the global enhancements like skip links can be set up.
// However, the standard Odoo widget way is preferred.
// If your selector is 'body', it will auto-instantiate.

// Helper function to be called from other JS modules if they don't have access to the widget instance
// window.dfrAnnounceToSR = function(regionId, message, politeness) {
//     const accessibilityWidget = odoo.__DEBUG__.services['web.public_root_widget'].getChildren().find(
//         child => child instanceof odoo.dfr_farmer_portal.portal_accessibility.DFRAccessibility
//     );
//     if (accessibilityWidget) {
//         accessibilityWidget.manageAriaLiveRegions(regionId, message, politeness);
//     } else {
//         // Fallback or create on the fly if really needed, but less ideal
//         const liveRegion = document.getElementById(regionId);
//         if (liveRegion) liveRegion.textContent = message;
//     }
// };