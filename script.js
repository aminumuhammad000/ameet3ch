// // Select all elements with the class 'hidden'
// const boxes = document.querySelectorAll('.section');

// const handleScroll = () => {
//   boxes.forEach((box) => {
//     // Get the element's position relative to the viewport
//     const rect = box.getBoundingClientRect();
//     const isVisible = rect.top < window.innerHeight && rect.bottom > 0;

//     if (isVisible) {
//       box.classList.add('visible');
//       box.classList.remove('hidden');
//     }
//   });
// };

// // Attach the scroll event listener
// window.addEventListener('scroll', handleScroll);

const menu = document.querySelector('.menu')
const mobNav = document.querySelector('.mobile')
const navs = document.querySelectorAll('.nav')

menu.addEventListener('click', (e) =>{
    menu.classList.toggle('active')
    mobNav.classList.toggle('show')
})

navs.forEach((nav) => {
    nav.addEventListener('click', (e) => {
        menu.classList.remove('active')
        mobNav.classList.remove('show')
    })
});

// ── Netlify Contact Form AJAX Handler ──
const mainContactForm = document.getElementById('main-contact-form');
if (mainContactForm) {
    mainContactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = mainContactForm.querySelector('button[type="submit"]');
        const statusMsg = mainContactForm.querySelector('.form-status-msg');
        const originalBtnHTML = submitBtn.innerHTML;

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
        if (statusMsg) {
            statusMsg.style.display = 'none';
            statusMsg.textContent = '';
        }

        try {
            const formData = new FormData(mainContactForm);
            await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData).toString()
            });

            submitBtn.innerHTML = '<i class="fa-solid fa-check"></i> Message Sent!';
            submitBtn.style.backgroundColor = '#16a34a';
            mainContactForm.reset();

            if (statusMsg) {
                statusMsg.textContent = 'Thank you! Your message has been received. A consultant will reach out to you within 24 hours.';
                statusMsg.style.color = '#16a34a';
                statusMsg.style.display = 'block';
            }

            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHTML;
                submitBtn.style.backgroundColor = '';
            }, 6000);
        } catch (err) {
            console.error('Contact form submission error:', err);
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHTML;
            if (statusMsg) {
                statusMsg.textContent = 'Could not send message. Please try again or chat with us on WhatsApp.';
                statusMsg.style.color = '#dc2626';
                statusMsg.style.display = 'block';
            }
        }
    });
}

// ── Smooth Scrollable Google Reviews Carousel ──
const storiesTrack = document.getElementById('stories-track');
const storiesPrevBtn = document.querySelector('.stories-prev');
const storiesNextBtn = document.querySelector('.stories-next');

if (storiesTrack) {
    const getScrollStep = () => {
        const firstCard = storiesTrack.querySelector('.story-card');
        return firstCard ? firstCard.offsetWidth + 22 : 380;
    };

    if (storiesPrevBtn) {
        storiesPrevBtn.addEventListener('click', () => {
            storiesTrack.scrollBy({ left: -getScrollStep(), behavior: 'smooth' });
        });
    }

    if (storiesNextBtn) {
        storiesNextBtn.addEventListener('click', () => {
            storiesTrack.scrollBy({ left: getScrollStep(), behavior: 'smooth' });
        });
    }

    // Smooth click-and-drag scrolling for desktop users
    let isDown = false;
    let startX = 0;
    let scrollStart = 0;

    storiesTrack.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - storiesTrack.offsetLeft;
        scrollStart = storiesTrack.scrollLeft;
        storiesTrack.style.scrollBehavior = 'auto';
    });

    const stopDragging = () => {
        if (!isDown) return;
        isDown = false;
        storiesTrack.style.scrollBehavior = 'smooth';
    };

    storiesTrack.addEventListener('mouseleave', stopDragging);
    storiesTrack.addEventListener('mouseup', stopDragging);

    storiesTrack.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - storiesTrack.offsetLeft;
        const walk = (x - startX) * 1.4;
        storiesTrack.scrollLeft = scrollStart - walk;
    });
}

// ── Cookie Consent & Privacy Preference Loader ──
(function() {
    if (!window.openAmeeCookieSettings && !document.querySelector('script[src*="cookie-consent.js"]')) {
        const cs = document.createElement('script');
        cs.src = '/cookie-consent.js';
        cs.defer = true;
        document.head.appendChild(cs);
    }
})();





// ── Public Email Subscription Handler (Lead Intelligence & NDPA 2023) ──
(function() {
    const subForm = document.getElementById('public-newsletter-form');
    if (!subForm) return;

    subForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const alertBox = document.getElementById('sub-alert');
        const submitBtn = document.getElementById('sub-submit-btn');

        alertBox.style.display = 'none';
        alertBox.className = 'sub-alert';

        const firstName = document.getElementById('sub-first-name').value.trim();
        const email = document.getElementById('sub-email').value.trim();
        const businessName = document.getElementById('sub-business-name').value.trim();
        const industry = document.getElementById('sub-industry').value;
        const consent = document.getElementById('sub-consent').checked;

        const topicCheckboxes = document.querySelectorAll('input[name="topics"]:checked');
        const preferredTopics = Array.from(topicCheckboxes).map(cb => cb.value);

        if (!consent) {
            alertBox.className = 'sub-alert error';
            alertBox.textContent = 'Please confirm marketing consent under the Nigeria Data Protection Act 2023.';
            alertBox.style.display = 'block';
            return;
        }

        const originalBtnHtml = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Securing your subscription...';

        try {
            const resp = await fetch('/api/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    first_name: firstName,
                    email: email,
                    business_name: businessName,
                    industry: industry,
                    preferred_topics: preferredTopics,
                    consent_given: true,
                    source_page: window.location.pathname
                })
            });

            const data = await resp.json();

            if (resp.ok && data.success) {
                alertBox.className = 'sub-alert success';
                alertBox.innerHTML = '<i class="fa-solid fa-circle-check"></i> ' + (data.message || 'Verification link sent! Please check your email inbox to confirm your subscription.');
                alertBox.style.display = 'block';
                subForm.reset();
            } else {
                alertBox.className = 'sub-alert error';
                alertBox.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> ' + (data.error || 'Unable to register subscription. Please try again.');
                alertBox.style.display = 'block';
            }
        } catch (err) {
            alertBox.className = 'sub-alert error';
            alertBox.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Connection issue. Please check your internet connection.';
            alertBox.style.display = 'block';
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHtml;
        }
    });
})();
