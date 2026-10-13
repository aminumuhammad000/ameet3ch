/**
 * Ameetech Technology — Blog & Marketing Lead Generation Page Script
 * Handles Reading Progress, Active Table of Contents, Lead Form AJAX,
 * and Google Analytics 4 (GA4) Conversion Event Tracking.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ── 1. Reading Progress Bar ──
    const progressBar = document.getElementById('reading-progress');
    const article = document.querySelector('.article-content');

    if (progressBar && article) {
        window.addEventListener('scroll', () => {
            const articleRect = article.getBoundingClientRect();
            const articleTop = articleRect.top + window.scrollY;
            const articleHeight = article.offsetHeight;
            const windowHeight = window.innerHeight;
            const scrollPos = window.scrollY;

            if (scrollPos < articleTop) {
                progressBar.style.width = '0%';
            } else if (scrollPos > articleTop + articleHeight - windowHeight) {
                progressBar.style.width = '100%';
            } else {
                const progress = ((scrollPos - articleTop) / (articleHeight - windowHeight)) * 100;
                progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
            }
        }, { passive: true });
    }

    // ── 2. Table of Contents Active Link Highlighting ──
    const tocLinks = document.querySelectorAll('.toc-link');
    const sections = document.querySelectorAll('.article-content section[id]');

    if (tocLinks.length > 0 && sections.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '-80px 0px -60% 0px',
            threshold: 0
        };

        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    tocLinks.forEach(link => {
                        if (link.getAttribute('href') === `#${id}`) {
                            link.classList.add('active');
                        } else {
                            link.classList.remove('active');
                        }
                    });
                }
            });
        }, observerOptions);

        sections.forEach(sec => sectionObserver.observe(sec));
    }

    // ── 3. Mobile Navigation Menu Toggle ──
    const menu = document.querySelector('.menu');
    const mobNav = document.querySelector('.mobile');
    const navs = document.querySelectorAll('.nav');

    if (menu && mobNav) {
        menu.addEventListener('click', () => {
            menu.classList.toggle('active');
            mobNav.classList.toggle('show');
        });

        navs.forEach(nav => {
            nav.addEventListener('click', () => {
                menu.classList.remove('active');
                mobNav.classList.remove('show');
                menu.innerHTML = '<i class="fa-solid fa-bars" title="Menu"></i><i class="fa-solid fa-xmark" title="Close Menu"></i>';
            });
        });
    }

    // ── 4. GA4 Helper Function ──
    const trackEvent = (eventName, params = {}) => {
        if (typeof window.gtag === 'function') {
            window.gtag('event', eventName, params);
        }
    };

    // Track Article View
    const pageArticleTitle = document.querySelector('h1')?.textContent.trim() || document.title;
    trackEvent('article_view', {
        article_title: pageArticleTitle,
        category: 'Business Growth & Marketing',
        author: 'Aminu Muhammad'
    });

    // ── 5. Contextual CTAs and Outbound Tracking ──
    // Primary CTAs
    document.querySelectorAll('[data-cta="primary"]').forEach(el => {
        el.addEventListener('click', () => {
            trackEvent('primary_cta_click', {
                cta_text: el.textContent.trim(),
                destination: el.getAttribute('href')
            });
        });
    });

    // WhatsApp Clicks
    document.querySelectorAll('a[href*="wa.me"]').forEach(el => {
        el.addEventListener('click', () => {
            trackEvent('whatsapp_click', {
                channel: 'WhatsApp',
                source_page: window.location.pathname
            });
        });
    });

    // Phone Calls
    document.querySelectorAll('a[href^="tel:"]').forEach(el => {
        el.addEventListener('click', () => {
            trackEvent('phone_click', {
                channel: 'Phone',
                source_page: window.location.pathname
            });
        });
    });

    // Service Internal Links
    document.querySelectorAll('a[href*="#services"], a[href*="/pages/"]').forEach(el => {
        el.addEventListener('click', () => {
            trackEvent('service_link_click', {
                service_url: el.getAttribute('href'),
                anchor_text: el.textContent.trim()
            });
        });
    });

    // ── 6. Lead Enquiry Form AJAX Handler ──
    const leadForm = document.getElementById('article-lead-form');
    if (leadForm) {
        let formStarted = false;

        // Track when user first interacts with any form input
        leadForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('focus', () => {
                if (!formStarted) {
                    formStarted = true;
                    trackEvent('contact_form_start', {
                        form_id: 'article-lead-form',
                        form_name: 'article_lead_enquiry'
                    });
                }
            }, { once: true });
        });

        leadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = leadForm.querySelector('button[type="submit"]');
            const statusMsg = document.getElementById('article-lead-status');
            const originalBtnHTML = submitBtn.innerHTML;

            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting...';

            if (statusMsg) {
                statusMsg.style.display = 'none';
                statusMsg.className = 'lead-status-msg';
                statusMsg.textContent = '';
            }

            try {
                const formData = new FormData(leadForm);
                const response = await fetch('/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams(formData).toString()
                });

                if (response.ok || response.status === 200 || response.status === 204) {
                    submitBtn.innerHTML = '<i class="fa-solid fa-check"></i> Request Received!';
                    submitBtn.style.backgroundColor = '#10B981';

                    if (statusMsg) {
                        statusMsg.textContent = 'Thank you! Your enquiry has been received. An Ameetech technology consultant will review your business requirements and contact you within 24 hours.';
                        statusMsg.classList.add('success');
                        statusMsg.style.display = 'block';
                    }

                    // Fire lead conversion event to GA4
                    trackEvent('generate_lead', {
                        form_id: 'article-lead-form',
                        service_selected: leadForm.querySelector('[name="service"]')?.value || 'Not Specified',
                        preferred_contact: leadForm.querySelector('[name="preferred_contact"]')?.value || 'Not Specified'
                    });

                    leadForm.reset();

                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalBtnHTML;
                        submitBtn.style.backgroundColor = '';
                    }, 8000);
                } else {
                    throw new Error(`Server returned status: ${response.status}`);
                }
            } catch (err) {
                console.error('Lead form submission error:', err);
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHTML;

                if (statusMsg) {
                    statusMsg.textContent = 'We could not submit your request automatically right now. Please message us directly on WhatsApp (+234 810 001 5498) or email support@ameetechnology.com.ng.';
                    statusMsg.classList.add('error');
                    statusMsg.style.display = 'block';
                }
            }
        });
    }
});
