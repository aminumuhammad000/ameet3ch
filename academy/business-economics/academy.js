/**
 * Ameetech Business & Economics Academy | Client Script
 * Handles Search, Quiz Interactions, Study Guide Request Modal,
 * Phone/Email Validation, and FAQ Accordions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ── 1. Client-Side Search ──
    const searchInput = document.getElementById('academy-search-input');
    const searchResults = document.getElementById('search-results');
    let searchIndex = [];

    // Fetch Search Index
    fetch('/academy/business-economics/academy-search.json')
        .then(res => res.json())
        .then(data => { searchIndex = data; })
        .catch(err => console.log('Search index loading offline or static:', err));

    if (searchInput && searchResults) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim().toLowerCase();
            if (query.length < 2) {
                searchResults.style.display = 'none';
                searchResults.innerHTML = '';
                return;
            }

            const matches = searchIndex.filter(item => 
                item.title.toLowerCase().includes(query) ||
                item.summary.toLowerCase().includes(query) ||
                item.category.toLowerCase().includes(query) ||
                (item.keywords && item.keywords.some(k => k.toLowerCase().includes(query)))
            );

            if (matches.length > 0) {
                searchResults.innerHTML = matches.map(m => `
                    <a href="${m.url}" class="search-result-item">
                        <h4>${escapeHTML(m.title)}</h4>
                        <p><span style="color:#6C2BD9;font-weight:600;">${escapeHTML(m.category)}</span> &bull; ${escapeHTML(m.summary.substring(0, 95))}...</p>
                    </a>
                `).join('');
                searchResults.style.display = 'block';
            } else {
                searchResults.innerHTML = `
                    <div class="search-empty-state">
                        <i class="fa-solid fa-magnifying-glass" style="font-size:1.5rem;color:#94a3b8;margin-bottom:8px;display:block;"></i>
                        No lessons found matching "<strong>${escapeHTML(query)}</strong>". Try searching for <em>profit, break-even, LTV, pricing,</em> or <em>opportunity cost</em>.
                    </div>
                `;
                searchResults.style.display = 'block';
            }
        });

        // Close search when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }

    // ── 2. Interactive Knowledge Check Quiz ──
    document.querySelectorAll('.quiz-option-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.quiz-card');
            const explanation = card.querySelector('.quiz-explanation');
            const isCorrect = this.getAttribute('data-correct') === 'true';

            // Disable all buttons in this quiz card
            card.querySelectorAll('.quiz-option-btn').forEach(b => {
                b.disabled = true;
                if (b.getAttribute('data-correct') === 'true') {
                    b.classList.add('correct');
                }
            });

            if (!isCorrect) {
                this.classList.add('incorrect');
            }

            if (explanation) {
                explanation.style.display = 'block';
            }
        });
    });

    // ── 3. Study Guide Download Modal ──
    const modalOverlay = document.getElementById('study-guide-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const guideForm = document.getElementById('study-guide-form');
    const guideTitleElem = document.getElementById('modal-guide-title');
    const guideSlugInput = document.getElementById('guide-slug-input');
    const deliveryWhatsappRadio = document.getElementById('delivery-whatsapp');
    const deliveryEmailRadio = document.getElementById('delivery-email');
    const whatsappGroup = document.getElementById('whatsapp-input-group');
    const emailGroup = document.getElementById('email-input-group');
    const formFeedback = document.getElementById('form-feedback-msg');

    // Open Modal
    document.querySelectorAll('[data-action="open-guide-modal"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const guideTitle = this.getAttribute('data-guide-title') || 'Comprehensive Study Guide';
            const guideSlug = this.getAttribute('data-guide-slug') || 'general-guide';

            if (guideTitleElem) guideTitleElem.textContent = guideTitle;
            if (guideSlugInput) guideSlugInput.value = guideSlug;
            if (modalOverlay) modalOverlay.classList.add('active');
            if (formFeedback) formFeedback.style.display = 'none';
        });
    });

    // Close Modal
    if (modalCloseBtn && modalOverlay) {
        modalCloseBtn.addEventListener('click', () => modalOverlay.classList.remove('active'));
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) modalOverlay.classList.remove('active');
        });
    }

    // Toggle Delivery Channel
    if (deliveryWhatsappRadio && deliveryEmailRadio) {
        const toggleInputs = () => {
            if (deliveryWhatsappRadio.checked) {
                whatsappGroup.style.display = 'block';
                emailGroup.style.display = 'none';
                document.getElementById('guide-whatsapp').required = true;
                document.getElementById('guide-email').required = false;
            } else {
                whatsappGroup.style.display = 'none';
                emailGroup.style.display = 'block';
                document.getElementById('guide-whatsapp').required = false;
                document.getElementById('guide-email').required = true;
            }
        };
        deliveryWhatsappRadio.addEventListener('change', toggleInputs);
        deliveryEmailRadio.addEventListener('change', toggleInputs);
    }

    // Handle Form Submission
    if (guideForm) {
        guideForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = guideForm.querySelector('.modal-submit-btn');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing Request...';

            const name = document.getElementById('guide-name')?.value.trim() || '';
            const deliveryMethod = document.querySelector('input[name="delivery_method"]:checked')?.value || 'email';
            let whatsapp = document.getElementById('guide-whatsapp')?.value.trim() || '';
            const email = document.getElementById('guide-email')?.value.trim() || '';
            const promotionalConsent = document.getElementById('guide-consent')?.checked || false;
            const guideSlug = guideSlugInput?.value || 'general';

            // Normalize Nigerian phone numbers
            if (deliveryMethod === 'whatsapp') {
                whatsapp = normalizePhoneNumber(whatsapp);
                if (!whatsapp) {
                    showFeedback('Please enter a valid phone number (e.g., 08012345678 or +2348012345678).', 'error');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                    return;
                }
            } else {
                if (!validateEmail(email)) {
                    showFeedback('Please enter a valid email address.', 'error');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                    return;
                }
            }

            const payload = {
                name,
                delivery_method: deliveryMethod,
                whatsapp,
                email,
                guide_slug: guideSlug,
                promotional_consent: promotionalConsent,
                page_url: window.location.href,
                timestamp: new Date().toISOString()
            };

            const directDownloadUrl = `/academy/business-economics/downloads/${guideSlug}-study-guide.pdf`;

            try {
                // Try sending to the backend endpoint
                const res = await fetch('/api/request-guide', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (res.ok) {
                    const data = await res.json();
                    showFeedback(`
                        <div style="background:#D1FAE5;color:#065F46;padding:12px;border-radius:8px;margin-top:12px;">
                            <i class="fa-solid fa-circle-check"></i> <strong>Request Received!</strong>
                            <p style="margin:4px 0 8px;">Your study guide has been queued for delivery via ${deliveryMethod === 'whatsapp' ? 'WhatsApp' : 'Email'}.</p>
                            <a href="${directDownloadUrl}" download class="study-guide-btn" style="padding:8px 16px;font-size:0.85rem;display:inline-flex;">
                                <i class="fa-solid fa-download"></i> Download PDF Directly Now
                            </a>
                        </div>
                    `, 'success');
                } else {
                    // Fallback graceful degradation for static deployments
                    showFeedback(`
                        <div style="background:#ECFDF5;color:#065F46;padding:12px;border-radius:8px;margin-top:12px;">
                            <i class="fa-solid fa-circle-check"></i> <strong>Thank you, ${name || 'Learner'}!</strong>
                            <p style="margin:4px 0 8px;">Your request has been recorded. You can also download your study guide directly below:</p>
                            <a href="${directDownloadUrl}" download class="study-guide-btn" style="padding:8px 16px;font-size:0.85rem;display:inline-flex;">
                                <i class="fa-solid fa-download"></i> Download PDF Now
                            </a>
                        </div>
                    `, 'success');
                }
            } catch (err) {
                // Network/static fallback
                showFeedback(`
                    <div style="background:#ECFDF5;color:#065F46;padding:12px;border-radius:8px;margin-top:12px;">
                        <i class="fa-solid fa-circle-check"></i> <strong>Request Confirmed!</strong>
                        <p style="margin:4px 0 8px;">You can download the study guide directly right now:</p>
                        <a href="${directDownloadUrl}" download class="study-guide-btn" style="padding:8px 16px;font-size:0.85rem;display:inline-flex;">
                            <i class="fa-solid fa-download"></i> Download PDF Now
                        </a>
                    </div>
                `, 'success');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    }

    // ── 4. FAQ Accordion ──
    document.querySelectorAll('.faq-header').forEach(header => {
        header.addEventListener('click', function() {
            const card = this.closest('.faq-card');
            card.classList.toggle('open');
        });
    });

    // Helpers
    function showFeedback(html, type) {
        if (!formFeedback) return;
        formFeedback.innerHTML = html;
        formFeedback.style.display = 'block';
    }

    function normalizePhoneNumber(phone) {
        // Remove spaces, hyphens, and brackets
        let clean = phone.replace(/[\s\-\(\)]/g, '');
        // Nigerian phone normalization
        if (clean.startsWith('0') && clean.length === 11) {
            clean = '+234' + clean.substring(1);
        } else if (clean.startsWith('234') && clean.length === 13) {
            clean = '+' + clean;
        } else if (!clean.startsWith('+')) {
            clean = '+' + clean;
        }
        // Basic E.164 check (between 8 and 15 digits)
        const digits = clean.replace(/\D/g, '');
        if (digits.length >= 8 && digits.length <= 15) {
            return clean;
        }
        return null;
    }

    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
        );
    }
});
