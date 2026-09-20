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
        // if (menu.classList.contains('active')) {
            menu.classList.remove('active')
            mobNav.classList.remove('show')
            menu.innerHTML = '<i class="fa-solid fa-bars"></i>';
        // } 
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


