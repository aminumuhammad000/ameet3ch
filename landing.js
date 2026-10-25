/**
 * Amee Technology - Core Landing Pages Client Script
 * Handles Mobile Navigation Drawer, Netlify Form Submissions,
 * Analytics Telemetry (GA4), and Smooth Link Scrolling.
 */

// ── Mobile Navigation Toggle ──
function toggleNav() {
    const drawer = document.getElementById('mobileNavDrawer');
    if (drawer) {
        drawer.classList.toggle('open');
    }
}

// ── Google Analytics Telemetry Helper ──
function trackEvent(eventName, params = {}) {
    if (typeof window.gtag === 'function') {
        window.gtag('event', eventName, params);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // ── 1. Telemetry on WhatsApp Links ──
    document.querySelectorAll('a[href*="wa.me"]').forEach(el => {
        el.addEventListener('click', () => {
            trackEvent('whatsapp_click', {
                channel: 'WhatsApp',
                source_page: window.location.pathname,
                link_text: el.textContent.trim()
            });
        });
    });

    // ── 2. Telemetry on Direct Phone Call Links ──
    document.querySelectorAll('a[href^="tel:"]').forEach(el => {
        el.addEventListener('click', () => {
            trackEvent('phone_click', {
                channel: 'Direct Phone',
                source_page: window.location.pathname,
                phone_number: el.getAttribute('href')
            });
        });
    });

    // ── 3. Netlify Lead Enquiry Form Submission ──
    const enquiryForm = document.querySelector('.lead-form-element');
    if (enquiryForm) {
        let formStarted = false;

        // Track when user first interacts with the form
        enquiryForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('focus', () => {
                if (!formStarted) {
                    formStarted = true;
                    trackEvent('contact_form_start', {
                        form_name: enquiryForm.getAttribute('name') || 'lead_enquiry_form',
                        source_page: window.location.pathname
                    });
                }
            }, { once: true });
        });

        enquiryForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = enquiryForm.querySelector('button[type="submit"]');
            const statusAlert = enquiryForm.parentElement.querySelector('.form-status-alert');
            const originalBtnHTML = submitBtn.innerHTML;

            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting...';

            if (statusAlert) {
                statusAlert.style.display = 'none';
                statusAlert.className = 'form-status-alert';
                statusAlert.textContent = '';
            }

            try {
                const formData = new FormData(enquiryForm);
                const response = await fetch('/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams(formData).toString()
                });

                if (response.ok || response.status === 200 || response.status === 204) {
                    submitBtn.innerHTML = '<i class="fa-solid fa-check"></i> Request Received!';
                    submitBtn.style.backgroundColor = '#10B981';

                    if (statusAlert) {
                        statusAlert.textContent = 'Thank you! Your project enquiry has been received. An Amee Technology technical consultant will review your specifications and contact you within 24 hours.';
                        statusAlert.classList.add('success');
                        statusAlert.style.display = 'block';
                    }

                    // Fire lead conversion event to GA4
                    trackEvent('generate_lead', {
                        form_name: enquiryForm.getAttribute('name') || 'lead_enquiry_form',
                        service_requested: enquiryForm.querySelector('[name="service"]')?.value || window.location.pathname,
                        page_location: window.location.href
                    });

                    enquiryForm.reset();

                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalBtnHTML;
                        submitBtn.style.backgroundColor = '';
                    }, 8000);
                } else {
                    throw new Error(`Server returned HTTP ${response.status}`);
                }
            } catch (err) {
                console.error('Lead form submission error:', err);
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHTML;

                if (statusAlert) {
                    statusAlert.textContent = 'Could not submit your enquiry automatically. Please reach out to us directly on WhatsApp (+234 810 001 5498) or email support@ameetechnology.com.ng.';
                    statusAlert.classList.add('error');
                    statusAlert.style.display = 'block';
                }
            }
        });
    }
});
