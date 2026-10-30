/**
 * Amee Technology Ltd — Privacy-First Cookie Consent & Preference Manager
 * Compliant with Nigeria Data Protection Act (NDPA 2023) & GDPR
 * Supports Google Analytics Consent Mode v2
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'amee_cookie_consent';
  var CONSENT_VERSION = '1.0';

  // Read existing consent from localStorage
  function getSavedConsent() {
    try {
      var item = localStorage.getItem(STORAGE_KEY);
      if (item) {
        var parsed = JSON.parse(item);
        if (parsed && typeof parsed.analytics === 'boolean') {
          return parsed;
        }
      }
    } catch (e) {
      /* ignore storage errors */
    }
    return null;
  }

  // Save consent to localStorage
  function saveConsent(analytics, functional) {
    var consentData = {
      necessary: true,
      analytics: Boolean(analytics),
      functional: Boolean(functional),
      timestamp: Date.now(),
      version: CONSENT_VERSION
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(consentData));
    } catch (e) {
      /* ignore storage errors */
    }
    applyGtagConsent(consentData.analytics);
    if (!consentData.analytics) {
      purgeAnalyticsCookies();
    }
    return consentData;
  }

  // Google Analytics Consent Mode Handler
  function applyGtagConsent(isGranted) {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    gtag('consent', 'update', {
      analytics_storage: isGranted ? 'granted' : 'denied'
    });
  }

  // Default consent mode initialization
  var initialSaved = getSavedConsent();
  window.dataLayer = window.dataLayer || [];
  function gtagInit() {
    window.dataLayer.push(arguments);
  }
  gtagInit('consent', 'default', {
    analytics_storage: initialSaved && initialSaved.analytics ? 'granted' : 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });

  // Purge Google Analytics tracking cookies when user rejects
  function purgeAnalyticsCookies() {
    var cookies = document.cookie.split(';');
    var hostname = window.location.hostname;
    var domainParts = hostname.split('.');
    var rootDomain = domainParts.length > 1 ? '.' + domainParts.slice(-2).join('.') : hostname;

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      var eqPos = cookie.indexOf('=');
      var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      if (name.indexOf('_ga') === 0 || name.indexOf('_gid') === 0 || name.indexOf('_gat') === 0) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + hostname + ';';
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + rootDomain + ';';
      }
    }
  }

  // Inject Styles
  function injectStyles() {
    if (document.getElementById('amee-cookie-styles')) return;
    var style = document.createElement('style');
    style.id = 'amee-cookie-styles';
    style.textContent = `
      #amee-cookie-banner {
        position: fixed;
        bottom: 1.5rem;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 2rem);
        max-width: 980px;
        background: #0d0520;
        color: #f8fafc;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(108, 43, 217, 0.35);
        z-index: 99999;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        animation: ameeFadeUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }
      @media (min-width: 768px) {
        #amee-cookie-banner {
          flex-direction: row;
          align-items: center;
          justify-content: space-between;
          padding: 1.15rem 1.75rem;
        }
      }
      @keyframes ameeFadeUp {
        from { opacity: 0; transform: translate(-50%, 20px); }
        to { opacity: 1; transform: translate(-50%, 0); }
      }
      .amee-cb-content {
        flex: 1;
        font-size: 0.875rem;
        line-height: 1.5;
        color: #cbd5e1;
      }
      .amee-cb-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.25rem;
      }
      .amee-cb-title i {
        color: #a855f7;
      }
      .amee-cb-content a {
        color: #a855f7;
        text-decoration: underline;
        font-weight: 500;
      }
      .amee-cb-content a:hover {
        color: #c084fc;
      }
      .amee-cb-actions {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.5rem;
        flex-shrink: 0;
      }
      .amee-btn {
        padding: 0.55rem 1rem;
        border-radius: 8px;
        font-size: 0.8125rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-family: inherit;
        white-space: nowrap;
      }
      .amee-btn-primary {
        background: #6C2BD9;
        color: #ffffff;
      }
      .amee-btn-primary:hover {
        background: #581cba;
        box-shadow: 0 4px 12px rgba(108, 43, 217, 0.4);
      }
      .amee-btn-secondary {
        background: rgba(255, 255, 255, 0.08);
        color: #f1f5f9;
        border: 1px solid rgba(255, 255, 255, 0.15);
      }
      .amee-btn-secondary:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
      }
      .amee-btn-text {
        background: transparent;
        color: #94a3b8;
        padding: 0.55rem 0.75rem;
      }
      .amee-btn-text:hover {
        color: #ffffff;
      }

      /* Modal Overlay */
      #amee-cookie-modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(13, 5, 32, 0.8);
        backdrop-filter: blur(4px);
        z-index: 100000;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        animation: ameeFadeIn 0.2s ease forwards;
      }
      @keyframes ameeFadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      #amee-cookie-modal {
        background: #ffffff;
        color: #0f172a;
        width: 100%;
        max-width: 580px;
        max-height: 90vh;
        overflow-y: auto;
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      }
      .amee-modal-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e2e8f0;
      }
      .amee-modal-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
      }
      .amee-modal-close {
        background: none;
        border: none;
        font-size: 1.25rem;
        color: #64748b;
        cursor: pointer;
        padding: 0.25rem;
        line-height: 1;
        border-radius: 6px;
      }
      .amee-modal-close:hover {
        color: #0f172a;
        background: #f1f5f9;
      }
      .amee-cookie-group {
        padding: 1rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 1rem;
      }
      .amee-group-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.35rem;
      }
      .amee-group-title {
        font-weight: 600;
        font-size: 0.925rem;
        color: #0f172a;
      }
      .amee-badge {
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 9999px;
        font-weight: 600;
      }
      .amee-badge-required {
        background: #e0e7ff;
        color: #3730a3;
      }
      .amee-group-desc {
        font-size: 0.8125rem;
        line-height: 1.45;
        color: #475569;
      }

      /* Toggle switch */
      .amee-switch {
        position: relative;
        display: inline-block;
        width: 44px;
        height: 24px;
      }
      .amee-switch input {
        opacity: 0;
        width: 0;
        height: 0;
      }
      .amee-slider {
        position: absolute;
        cursor: pointer;
        inset: 0;
        background-color: #cbd5e1;
        transition: 0.2s ease;
        border-radius: 24px;
      }
      .amee-slider:before {
        position: absolute;
        content: "";
        height: 18px;
        width: 18px;
        left: 3px;
        bottom: 3px;
        background-color: white;
        transition: 0.2s ease;
        border-radius: 50%;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
      }
      .amee-switch input:checked + .amee-slider {
        background-color: #6C2BD9;
      }
      .amee-switch input:checked + .amee-slider:before {
        transform: translateX(20px);
      }

      .amee-modal-footer {
        display: flex;
        justify-content: flex-end;
        gap: 0.75rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
      }
      .amee-modal-footer .amee-btn-primary {
        background: #6C2BD9;
        color: white;
      }
      .amee-modal-footer .amee-btn-primary:hover {
        background: #581cba;
      }
      .amee-modal-footer .amee-btn-secondary {
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
      }
      .amee-modal-footer .amee-btn-secondary:hover {
        background: #e2e8f0;
      }
    `;
    document.head.appendChild(style);
  }

  // Render floating cookie banner
  function renderBanner() {
    if (document.getElementById('amee-cookie-banner')) return;
    if (getSavedConsent() !== null) return;

    injectStyles();

    var banner = document.createElement('aside');
    banner.id = 'amee-cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie Consent Preferences');

    banner.innerHTML = `
      <div class="amee-cb-content">
        <div class="amee-cb-title">
          <i class="fa-solid fa-shield-halved"></i>
          <span>We Respect Your Privacy</span>
        </div>
        <div>
          We use cookies and local browser storage to keep our services secure, remember your preferences, and analyze traffic to improve our offerings in compliance with the <strong>Nigeria Data Protection Act (NDPA 2023)</strong> and GDPR. Review our <a href="/cookie-policy.html">Cookie Policy</a> or <a href="/privacy-policy.html">Privacy Policy</a>.
        </div>
      </div>
      <div class="amee-cb-actions">
        <button id="amee-cb-accept-all" class="amee-btn amee-btn-primary">Accept All</button>
        <button id="amee-cb-reject-all" class="amee-btn amee-btn-secondary">Reject Non-Essential</button>
        <button id="amee-cb-customize" class="amee-btn amee-btn-text">Preferences</button>
      </div>
    `;

    document.body.appendChild(banner);

    document.getElementById('amee-cb-accept-all').addEventListener('click', function () {
      saveConsent(true, true);
      banner.remove();
    });

    document.getElementById('amee-cb-reject-all').addEventListener('click', function () {
      saveConsent(false, true);
      banner.remove();
    });

    document.getElementById('amee-cb-customize').addEventListener('click', function () {
      openPreferencesModal();
    });
  }

  // Render & Open Preferences Modal
  function openPreferencesModal() {
    injectStyles();

    var existingOverlay = document.getElementById('amee-cookie-modal-overlay');
    if (existingOverlay) {
      existingOverlay.remove();
    }

    var saved = getSavedConsent() || { necessary: true, analytics: false, functional: true };

    var overlay = document.createElement('div');
    overlay.id = 'amee-cookie-modal-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Cookie Preferences');

    overlay.innerHTML = `
      <div id="amee-cookie-modal">
        <div class="amee-modal-header">
          <div>
            <div class="amee-modal-title">Cookie & Tracking Preferences</div>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">
              Manage how Amee Technology Ltd handles cookies on your browser.
            </div>
          </div>
          <button class="amee-modal-close" aria-label="Close preferences">&times;</button>
        </div>

        <div class="amee-cookie-group">
          <div class="amee-group-header">
            <span class="amee-group-title">Strictly Necessary Cookies</span>
            <span class="amee-badge amee-badge-required">Always Active</span>
          </div>
          <div class="amee-group-desc">
            Essential for security, CSRF protection, page navigation, and recording your cookie consent status (e.g. <code>amee_cookie_consent</code>). These cookies cannot be deactivated.
          </div>
        </div>

        <div class="amee-cookie-group">
          <div class="amee-group-header">
            <span class="amee-group-title">Analytics & Performance</span>
            <label class="amee-switch" aria-label="Toggle Analytics Cookies">
              <input type="checkbox" id="amee-pref-analytics" ${saved.analytics ? 'checked' : ''}>
              <span class="amee-slider"></span>
            </label>
          </div>
          <div class="amee-group-desc">
            Uses Google Analytics 4 (<code>_ga</code>, <code>_ga_7T17W9SPKB</code>) to gather aggregated, privacy-preserving metrics on page usage and device performance. No personal or commercial invoice content is ever transmitted.
          </div>
        </div>

        <div class="amee-cookie-group">
          <div class="amee-group-header">
            <span class="amee-group-title">Functional & Client Storage</span>
            <label class="amee-switch" aria-label="Toggle Functional Storage">
              <input type="checkbox" id="amee-pref-functional" ${saved.functional ? 'checked' : ''}>
              <span class="amee-slider"></span>
            </label>
          </div>
          <div class="amee-group-desc">
            Stores client-side draft invoices, receipts, and assessment answers in your browser's local storage so you don't lose progress when navigating or refreshing.
          </div>
        </div>

        <div class="amee-modal-footer">
          <button id="amee-modal-reject" class="amee-btn amee-btn-secondary">Reject All</button>
          <button id="amee-modal-save" class="amee-btn amee-btn-primary">Save Preferences</button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    function closeModal() {
      overlay.remove();
    }

    overlay.querySelector('.amee-modal-close').addEventListener('click', closeModal);

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) {
        closeModal();
      }
    });

    document.addEventListener('keydown', function escHandler(e) {
      if (e.key === 'Escape' && document.getElementById('amee-cookie-modal-overlay')) {
        closeModal();
        document.removeEventListener('keydown', escHandler);
      }
    });

    document.getElementById('amee-modal-reject').addEventListener('click', function () {
      saveConsent(false, false);
      closeModal();
      var banner = document.getElementById('amee-cookie-banner');
      if (banner) banner.remove();
    });

    document.getElementById('amee-modal-save').addEventListener('click', function () {
      var analyticsChecked = document.getElementById('amee-pref-analytics').checked;
      var functionalChecked = document.getElementById('amee-pref-functional').checked;
      saveConsent(analyticsChecked, functionalChecked);
      closeModal();
      var banner = document.getElementById('amee-cookie-banner');
      if (banner) banner.remove();
    });
  }

  // Expose global methods
  window.openAmeeCookieSettings = openPreferencesModal;
  window.getAmeeCookieConsent = getSavedConsent;

  // Bind to any link with class "open-cookie-settings" or href="#cookie-settings"
  function bindReopenTriggers() {
    document.querySelectorAll('.open-cookie-settings, a[href="#cookie-settings"]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        openPreferencesModal();
      });
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      renderBanner();
      bindReopenTriggers();
    });
  } else {
    renderBanner();
    bindReopenTriggers();
  }
})();
