/* ============================================================
   AmeeBot – AI Business Assessment Consultant
   ============================================================
   EmailJS Setup (free at emailjs.com):
     1. Sign up → create a Gmail/Outlook service
     2. Create an email template (use variables below)
     3. Replace the three EMAILJS_* constants below
   ============================================================ */

const EMAILJS_PUBLIC_KEY  = 'YOUR_PUBLIC_KEY';   // ← replace
const EMAILJS_SERVICE_ID  = 'YOUR_SERVICE_ID';   // ← replace
const EMAILJS_TEMPLATE_ID = 'YOUR_TEMPLATE_ID';  // ← replace

// Initialise EmailJS
(function() {
  if (typeof emailjs !== 'undefined') emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });
})();

// ── DOM References ─────────────────────────────────────────────
const overlay       = document.getElementById('ab-overlay');
const chatMessages  = document.getElementById('ab-chat-messages');
const progressFill  = document.getElementById('ab-progress-fill');
const progressText  = document.getElementById('ab-progress-text');
const optionGroup   = document.getElementById('ab-option-group');
const textRow       = document.getElementById('ab-text-row');
const textInput     = document.getElementById('ab-text-input');
const sendBtn       = document.getElementById('ab-send-btn');
const reportWrap    = document.getElementById('ab-report-wrap');
const reportPanel   = document.getElementById('ab-report');
const chatWindow    = document.getElementById('ab-chat-window');
const inputArea     = document.getElementById('ab-input-area');
const modalClose    = document.getElementById('ab-modal-close');
const emailGate     = document.getElementById('ab-email-gate');
const emailForm     = document.getElementById('ab-email-form');
const gateNameInput = document.getElementById('ab-gate-name');
const gateEmailInput= document.getElementById('ab-gate-email');
const gateSubmitBtn = document.getElementById('ab-gate-submit');

// ── State ──────────────────────────────────────────────────────
let answers = {};
let currentStep = 0;
let isTyping   = false;
let cachedScores = null, cachedInsights = null, cachedRoadmap = null;

// ── Question Script ─────────────────────────────────────────────
const QUESTIONS = [
  // BUSINESS BASICS
  { id:'name',     category:'basics', q:'Hi! 👋 I\'m <b>AmeeBot</b>, your AI Business Consultant.<br><br>To get started, what is your <b>business name</b>?', type:'text', placeholder:'e.g. Sunrise Bakery' },
  { id:'industry', category:'basics', q:'Great! What <b>industry</b> are you in?', type:'options', options:['Retail / E-commerce','Food & Hospitality','Healthcare','Education','Technology','Logistics','Finance','Real Estate','Media & Creative','Other'] },
  { id:'age',      category:'basics', q:'How long have you been <b>operating</b>?', type:'options', options:['Less than 6 months','6 – 12 months','1 – 2 years','3 – 5 years','5+ years'] },
  { id:'employees',category:'basics', q:'How many <b>employees</b> do you currently have?', type:'options', options:['Just me','2 – 5','6 – 15','16 – 50','50+'] },
  // CUSTOMERS
  { id:'customer',   category:'customers', q:'Who is your <b>ideal customer</b>?', type:'text', placeholder:'e.g. Young professionals aged 25–35 in Lagos' },
  { id:'acquisition',category:'customers', q:'How do customers <b>currently find you</b>?', type:'options', options:['Word of mouth / referrals','Social media','Google search','Paid advertising','Walk-ins / offline','I struggle to get customers'] },
  { id:'cust_challenge', category:'customers', q:'What is your <b>biggest customer challenge</b>?', type:'options', options:['Getting new customers','Retaining existing customers','Understanding what customers want','Getting positive reviews','Handling complaints'] },
  // SALES
  { id:'sales_method', category:'sales', q:'How do you <b>get clients</b> right now?', type:'options', options:['Direct calls & follow-ups','Social media DMs','Website / online store','Referrals from existing clients','I don\'t have a clear process'] },
  { id:'sales_challenge', category:'sales', q:'What is your <b>biggest sales challenge</b>?', type:'options', options:['Too few leads','Low conversion rate','Inconsistent follow-up','Pricing / competition','No structured sales process'] },
  { id:'followup', category:'sales', q:'Do you have a <b>follow-up process</b> for leads who don\'t buy?', type:'options', options:['Yes – structured & consistent','Yes – but informal','Rarely or never','No follow-up process'] },
  // MARKETING
  { id:'website',   category:'marketing', q:'Do you have a <b>professional website</b>?', type:'options', options:['Yes – modern & up to date','Yes – but outdated','No – but planning one','No website at all'] },
  { id:'social',    category:'marketing', q:'Are you <b>active on social media</b>?', type:'options', options:['Yes – posting regularly','Yes – but inconsistently','Only personal accounts','Not active on social media'] },
  { id:'paid_ads',  category:'marketing', q:'Do you run <b>paid advertisements</b>?', type:'options', options:['Yes – consistently','Tried it but stopped','No – but interested','No paid advertising'] },
  { id:'seo',       category:'marketing', q:'Are you doing <b>SEO</b> (Search Engine Optimisation)?', type:'options', options:['Yes – actively','Somewhat','I don\'t know what SEO is','No SEO at all'] },
  // OPERATIONS
  { id:'crm',       category:'operations', q:'How do you <b>manage customer information</b>?', type:'options', options:['CRM software (e.g. HubSpot)','Spreadsheets','Paper records / notebooks','I don\'t track customer data'] },
  { id:'software',  category:'operations', q:'Do you use any <b>business software</b> (accounting, scheduling, etc.)?', type:'options', options:['Yes – multiple tools','One or two tools','Mostly manual','No software at all'] },
  { id:'manual',    category:'operations', q:'Which tasks are <b>still done manually</b>?', type:'options', options:['Invoicing & payments','Customer follow-ups','Appointment booking','Inventory management','Most tasks are automated'] },
  // FINANCE
  { id:'tracking',  category:'finance', q:'Do you <b>track your monthly income and expenses</b>?', type:'options', options:['Yes – in accounting software','Yes – in spreadsheets','Informally / in my head','No tracking at all'] },
  { id:'profit',    category:'finance', q:'Do you know your <b>monthly profit</b>?', type:'options', options:['Yes – exactly','Roughly','Not really','No idea'] },
  { id:'fin_challenge', category:'finance', q:'What is your <b>biggest financial challenge</b>?', type:'options', options:['Cash flow problems','Not knowing profitability','Managing expenses','Accessing funding / loans','Tax & compliance'] },
  // TECHNOLOGY
  { id:'online_pay', category:'tech', q:'Do you <b>accept online payments</b>?', type:'options', options:['Yes – multiple methods','Yes – one method','No – cash only','Not applicable'] },
  { id:'booking',    category:'tech', q:'Can customers <b>book or order online</b>?', type:'options', options:['Yes – automated system','Yes – via WhatsApp/DM','No – phone/walk-in only','Not applicable'] },
  { id:'automation', category:'tech', q:'Are any of your <b>business processes automated</b>?', type:'options', options:['Yes – several are automated','One or two things','Planning to automate','Nothing is automated'] },
  // GROWTH
  { id:'goal',    category:'growth', q:'What are your <b>main goals for the next 12 months</b>?', type:'text', placeholder:'e.g. Double revenue, open a second location, launch online store' },
  { id:'barrier', category:'growth', q:'What is the <b>biggest obstacle</b> preventing you from reaching those goals?', type:'text', placeholder:'e.g. Lack of funding, time, not enough customers' },
];

const TOTAL = QUESTIONS.length;

// ── Open / Close ────────────────────────────────────────────────
document.getElementById('start-assessment-btn').addEventListener('click', startAssessment);
modalClose.addEventListener('click', () => {
  overlay.classList.remove('ab-open');
  overlay.setAttribute('aria-hidden','true');
});
overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('ab-open'); });

function startAssessment() {
  answers = {}; currentStep = 0; cachedScores = null; cachedInsights = null;
  chatMessages.innerHTML = '';
  reportWrap.style.display = 'none';
  reportPanel.innerHTML = '';
  chatWindow.style.display = '';
  inputArea.style.display  = '';
  // Reset gate
  if (emailGate) {
    emailGate.classList.remove('ab-gate-hidden');
    const formEl = emailGate.querySelector('.ab-email-form');
    const sucEl  = emailGate.querySelector('.ab-gate-success');
    if (formEl) formEl.style.display = '';
    if (sucEl)  sucEl.classList.remove('show');
    if (gateNameInput) gateNameInput.value = '';
    if (gateEmailInput) gateEmailInput.value = '';
  }
  updateProgress(0);
  overlay.classList.add('ab-open');
  overlay.setAttribute('aria-hidden','false');
  setTimeout(() => askQuestion(0), 400);
}

// ── Progress ────────────────────────────────────────────────────
function updateProgress(step) {
  const pct = Math.round((step / TOTAL) * 100);
  progressFill.style.width = pct + '%';
  progressText.textContent  = pct + '%';
}

// ── Ask Question ────────────────────────────────────────────────
async function askQuestion(idx) {
  if (idx >= TOTAL) { await generateReport(); return; }
  const q = QUESTIONS[idx];
  updateProgress(idx);
  const typingEl = createTypingIndicator();
  chatMessages.appendChild(typingEl);
  scrollChat();
  await delay(900 + Math.random() * 500);
  typingEl.remove();
  if (idx > 0 && QUESTIONS[idx].category !== QUESTIONS[idx-1].category) {
    const label = document.createElement('div');
    label.style.cssText = 'text-align:center;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#9ca3af;padding:6px 0;margin-top:4px;';
    label.textContent = categoryLabel(q.category);
    chatMessages.appendChild(label);
  }
  addBotMessage(q.q.replace('{name}', answers.name || 'there'));
  scrollChat();
  renderInput(q);
}

function categoryLabel(cat) {
  const map = { basics:'Business Basics', customers:'Customers', sales:'Sales', marketing:'Marketing', operations:'Operations', finance:'Finance', tech:'Technology', growth:'Growth Goals' };
  return '── ' + (map[cat] || cat) + ' ──';
}

// ── Render Input ────────────────────────────────────────────────
function renderInput(q) {
  optionGroup.innerHTML = '';
  if (q.type === 'options') {
    textRow.style.display = 'none';
    q.options.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'ab-opt-btn';
      btn.textContent = opt;
      btn.addEventListener('click', () => handleAnswer(opt, q));
      optionGroup.appendChild(btn);
    });
  } else {
    textRow.style.display = 'flex';
    textInput.placeholder = q.placeholder || 'Type your answer...';
    textInput.value = '';
    textInput.focus();
    const submit = () => { const val = textInput.value.trim(); if (!val) return; handleAnswer(val, q); };
    sendBtn.onclick = submit;
    textInput.onkeydown = (e) => { if (e.key === 'Enter') submit(); };
  }
}

// ── Handle Answer ───────────────────────────────────────────────
function handleAnswer(value, q) {
  if (isTyping) return;
  isTyping = true;
  answers[q.id] = value;
  optionGroup.innerHTML = '';
  textRow.style.display = 'none';
  addUserMessage(value);
  scrollChat();
  currentStep++;
  isTyping = false;
  setTimeout(() => askQuestion(currentStep), 500);
}

// ── Message Bubbles ─────────────────────────────────────────────
function addBotMessage(html) {
  const wrap = document.createElement('div');
  wrap.className = 'ab-msg ab-msg-bot';
  wrap.innerHTML = `<div class="ab-msg-avatar"><i class="fa-solid fa-robot"></i></div><div class="ab-msg-bubble">${html}</div>`;
  chatMessages.appendChild(wrap);
}
function addUserMessage(text) {
  const wrap = document.createElement('div');
  wrap.className = 'ab-msg ab-msg-user';
  const initials = (answers.name || 'You').substring(0,2).toUpperCase();
  wrap.innerHTML = `<div class="ab-msg-bubble">${escHtml(text)}</div><div class="ab-msg-avatar user-avatar">${initials}</div>`;
  chatMessages.appendChild(wrap);
}
function createTypingIndicator() {
  const wrap = document.createElement('div');
  wrap.className = 'ab-msg ab-msg-bot';
  wrap.innerHTML = `<div class="ab-msg-avatar"><i class="fa-solid fa-robot"></i></div><div class="ab-msg-bubble"><div class="ab-typing"><span></span><span></span><span></span></div></div>`;
  return wrap;
}
function scrollChat() { requestAnimationFrame(() => { chatWindow.scrollTop = chatWindow.scrollHeight; }); }

// ── Analysis Engine ─────────────────────────────────────────────
function analyzeAnswers() {
  const a = answers;
  const scores = {};
  let brand = 50;
  if (a.website?.includes('modern')) brand += 30;
  else if (a.website?.includes('outdated')) brand += 10;
  else if (a.website?.includes('planning')) brand += 5;
  if (a.social?.includes('regularly')) brand += 20;
  else if (a.social?.includes('inconsistently')) brand += 8;
  scores.Branding = Math.min(brand, 100);

  let mkt = 30;
  if (a.paid_ads?.includes('consistently')) mkt += 30;
  else if (a.paid_ads?.includes('stopped')) mkt += 10;
  if (a.seo?.includes('actively')) mkt += 30;
  else if (a.seo?.includes('Somewhat')) mkt += 12;
  if (a.social?.includes('regularly')) mkt += 10;
  scores.Marketing = Math.min(mkt, 100);

  let sales = 30;
  if (!a.sales_method?.includes('don\'t')) sales += 20;
  if (a.followup?.includes('structured')) sales += 30;
  else if (a.followup?.includes('informal')) sales += 12;
  if (!a.sales_challenge?.includes('No structured')) sales += 20;
  scores.Sales = Math.min(sales, 100);

  let tech = 20;
  if (a.online_pay?.includes('multiple')) tech += 30;
  else if (a.online_pay?.includes('one method')) tech += 15;
  if (a.booking?.includes('automated')) tech += 25;
  else if (a.booking?.includes('WhatsApp')) tech += 10;
  if (a.automation?.includes('several')) tech += 25;
  else if (a.automation?.includes('One or two')) tech += 12;
  scores.Technology = Math.min(tech, 100);

  let cx = 40;
  if (a.followup?.includes('structured')) cx += 25;
  if (a.crm?.includes('CRM software')) cx += 20;
  scores['Customer Experience'] = Math.min(cx, 100);

  let ops = 30;
  if (a.crm?.includes('CRM')) ops += 25;
  else if (a.crm?.includes('Spreadsheets')) ops += 10;
  if (a.software?.includes('multiple')) ops += 25;
  else if (a.software?.includes('One or two')) ops += 12;
  if (a.manual?.includes('automated')) ops += 20;
  scores.Operations = Math.min(ops, 100);

  let fin = 20;
  if (a.tracking?.includes('accounting software')) fin += 40;
  else if (a.tracking?.includes('spreadsheets')) fin += 20;
  else if (a.tracking?.includes('Informally')) fin += 8;
  if (a.profit?.includes('exactly')) fin += 40;
  else if (a.profit?.includes('Roughly')) fin += 20;
  scores.Finance = Math.min(fin, 100);

  const overall = Math.round(Object.values(scores).reduce((s,v) => s+v,0) / Object.keys(scores).length);
  return { scores, overall };
}

function generateInsights() {
  const a = answers;
  const strengths=[], weaknesses=[], risks=[], services=[];
  const hiRec=[], midRec=[], ltRec=[];

  // Website
  const hasGoodSite = a.website?.includes('modern');
  const hasSite = !a.website?.includes('No website');
  if (hasGoodSite) { strengths.push('Professional website presence established'); }
  else if (!hasSite) {
    weaknesses.push('No website — invisible to online customers');
    risks.push('Losing customers to competitors who have an online presence');
    hiRec.push('Build a professional website immediately');
    services.push({ icon:'fa-globe', name:'Website Development', why:'Your business has no website. Customers cannot find you online. A professional website builds instant credibility and opens new sales channels.', priority:'High' });
  } else {
    weaknesses.push('Website is outdated — may damage brand credibility');
    midRec.push('Redesign your website with a modern, mobile-first approach');
    services.push({ icon:'fa-globe', name:'Website Development', why:'Your current website is outdated. A modern redesign will reflect your brand quality and convert more visitors into customers.', priority:'Medium' });
  }

  // Social Media
  if (a.social?.includes('regularly')) { strengths.push('Active and consistent social media presence'); }
  else if (!a.social?.includes('regular')) {
    weaknesses.push('Inconsistent or absent social media activity');
    midRec.push('Build a consistent social media posting schedule');
    services.push({ icon:'fa-hashtag', name:'Social Media Management', why:'Inconsistent posting reduces visibility. Our team will manage your social media daily, creating engaging content that grows your audience.', priority:'Medium' });
  }

  // SEO
  if (a.seo?.includes('actively')) { strengths.push('Active SEO strategy driving organic search traffic'); }
  else {
    weaknesses.push('Little or no SEO — business is invisible on Google');
    hiRec.push('Set up Google Business Profile (free, immediate impact)');
    midRec.push('Implement a full SEO strategy for organic growth');
    services.push({ icon:'fa-magnifying-glass', name:'SEO Optimisation', why:'Without SEO, customers searching for your services on Google will find your competitors instead. We will optimise your online presence for top search rankings.', priority:'High' });
  }

  // Paid Ads
  if (a.paid_ads?.includes('consistently')) { strengths.push('Running consistent paid advertising campaigns'); }
  else {
    midRec.push('Launch targeted social media or Google Ads campaign');
    services.push({ icon:'fa-chart-line', name:'Digital Marketing Strategy', why:'Paid advertising is the fastest way to reach new customers. Our team will build targeted campaigns that deliver real ROI for your business.', priority:'Medium' });
  }

  // CRM / Follow-Up
  if (a.followup?.includes('structured')) { strengths.push('Structured lead follow-up and sales process in place'); }
  else {
    weaknesses.push('No consistent follow-up process — losing warm leads');
    hiRec.push('Implement a CRM system to track and follow up all leads');
    services.push({ icon:'fa-address-card', name:'CRM Implementation', why:'Without a CRM, leads fall through the cracks. We will implement a system that automatically tracks, follows up, and converts more leads into paying customers.', priority:'High' });
  }

  // Customer Data
  if (a.crm?.includes('CRM software')) { strengths.push('Customer data managed with CRM software'); }
  else if (!a.crm?.includes('CRM')) {
    weaknesses.push('Customer information not properly organised or tracked');
    risks.push('Losing repeat customers due to poor relationship management');
  }

  // Finance
  if (a.tracking?.includes('accounting')) { strengths.push('Using accounting software for full financial visibility'); }
  else {
    weaknesses.push('Weak financial tracking — business running blind');
    risks.push('Unable to make informed decisions without financial data');
    hiRec.push('Set up accounting and financial tracking immediately');
  }

  // Automation
  if (a.automation?.includes('several')) { strengths.push('Multiple business processes successfully automated'); }
  else {
    weaknesses.push('Most business processes are still manual and inefficient');
    midRec.push('Automate follow-ups, invoicing, and repetitive tasks');
    ltRec.push('Build a comprehensive business automation pipeline');
    services.push({ icon:'fa-robot', name:'Business Automation', why:'Manual processes waste time and cause errors. We will automate your repetitive workflows so you can focus on growing your business instead of running it.', priority:'Medium' });
  }

  // Online Booking
  if (a.booking?.includes('automated')) { strengths.push('Online booking and ordering system in place'); }
  else if (!a.booking?.includes('applicable')) {
    weaknesses.push('Customers cannot book or order online — losing convenience sales');
    risks.push('Customers choosing competitors who offer online booking');
    hiRec.push('Enable online booking or ordering on your website');
    services.push({ icon:'fa-mobile-screen', name:'Mobile App Development', why:'Customers expect to book and pay online. We will build a mobile app or booking system so customers can transact with you anytime, from anywhere.', priority:'Medium' });
  }

  // Growth goal
  if (a.goal) { strengths.push(`Clear vision: "${a.goal.substring(0,80)}"`); }

  // Always-relevant long-term recommendations
  ltRec.push('Develop a customer loyalty and referral rewards programme');
  ltRec.push('Create professional brand video content to drive conversions');
  services.push({ icon:'fa-film', name:'Professional Videography', why:'High-quality video content builds trust and dramatically increases conversion rates on social media and your website.', priority:'Long Term' });

  // De-duplicate services
  const seen = new Set();
  const uniqueServices = services.filter(s => { if (seen.has(s.name)) return false; seen.add(s.name); return true; }).slice(0,7);

  return { strengths, weaknesses, risks, recommendations: { high:hiRec, medium:midRec, longterm:ltRec }, services: uniqueServices };
}

function generateRoadmap() {
  return {
    month1: ['Build or update your professional website', 'Set up Google Business Profile (free)', 'Create a dedicated business email address'],
    month2: ['Launch consistent social media content plan', 'Start first paid advertising campaign', 'Organise and clean up your customer database'],
    month3: ['Implement CRM to track leads and clients', 'Automate customer follow-ups and reminders', 'Begin SEO optimisation for long-term growth'],
  };
}

// ── Report Builder ──────────────────────────────────────────────
async function generateReport() {
  updateProgress(TOTAL);
  addBotMessage(`Thank you, <b>${answers.name || 'there'}</b>! 🎉<br><br>Excellent — I now have everything I need. Let me <b>analyse your business</b> and generate your personalised report...`);
  scrollChat();
  await delay(2000);

  const { scores, overall } = analyzeAnswers();
  const insights = generateInsights();
  const roadmap  = generateRoadmap();
  cachedScores   = scores;
  cachedInsights = insights;
  cachedRoadmap  = roadmap;

  // Build report HTML (blurred behind gate)
  reportPanel.innerHTML = buildReportHTML(scores, overall, insights, roadmap);

  // Pre-fill name in gate
  if (gateNameInput && answers.name) gateNameInput.value = answers.name;

  // Transition from chat to report (gated)
  chatWindow.style.display = 'none';
  inputArea.style.display  = 'none';
  reportWrap.style.display = 'flex';
  reportWrap.classList.add('ab-gated');

  // Animate score ring after gate shows
  setTimeout(() => animateScoreRing(overall), 300);

  // Wire up email gate form
  setupEmailGate(scores, overall, insights, roadmap);
}

// ── Email Gate ──────────────────────────────────────────────────
function setupEmailGate(scores, overall, insights, roadmap) {
  if (!emailForm) return;

  emailForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name  = gateNameInput.value.trim();
    const email = gateEmailInput.value.trim();
    const errorEl = emailGate.querySelector('.ab-gate-error');

    // Validation
    gateNameInput.classList.remove('ab-input-error');
    gateEmailInput.classList.remove('ab-input-error');
    if (errorEl) { errorEl.classList.remove('show'); errorEl.textContent = ''; }

    if (!name) { gateNameInput.classList.add('ab-input-error'); showGateError('Please enter your full name.'); return; }
    if (!email || !isValidEmail(email)) { gateEmailInput.classList.add('ab-input-error'); showGateError('Please enter a valid email address.'); return; }

    // Sending state
    gateSubmitBtn.disabled = true;
    gateSubmitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending Report...';

    const emailParams = buildEmailParams(name, email, scores, overall, insights, roadmap);

    try {
      if (typeof emailjs !== 'undefined' && EMAILJS_PUBLIC_KEY !== 'YOUR_PUBLIC_KEY') {
        await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, emailParams);
      } else {
        // Demo mode: simulate sending
        await delay(1800);
      }
      showGateSuccess(email);
    } catch(err) {
      console.error('EmailJS error:', err);
      gateSubmitBtn.disabled = false;
      gateSubmitBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Send My Report';
      showGateError('Could not send email. Please try again or contact us directly on WhatsApp.');
    }
  });
}

function showGateError(msg) {
  const errorEl = emailGate.querySelector('.ab-gate-error');
  if (!errorEl) return;
  errorEl.textContent = msg;
  errorEl.classList.add('show');
}

function showGateSuccess(email) {
  const formEl = emailGate.querySelector('.ab-email-form');
  let sucEl    = emailGate.querySelector('.ab-gate-success');

  if (!sucEl) {
    sucEl = document.createElement('div');
    sucEl.className = 'ab-gate-success';
    sucEl.innerHTML = `
      <div class="ab-gate-success-icon"><i class="fa-solid fa-check"></i></div>
      <h4>Report Sent! 🎉</h4>
      <p>Your Business Assessment Report has been sent to <b>${escHtml(email)}</b>. Check your inbox!</p>
      <button class="ab-gate-unlock-btn" id="ab-gate-unlock">View Report Now <i class="fa-solid fa-arrow-right"></i></button>`;
    emailGate.querySelector('.ab-email-gate-card').appendChild(sucEl);
  }

  if (formEl) formEl.style.display = 'none';
  sucEl.classList.add('show');

  document.getElementById('ab-gate-unlock')?.addEventListener('click', unlockReport);
}

function unlockReport() {
  emailGate.classList.add('ab-gate-hidden');
  reportWrap.classList.remove('ab-gated');
  setTimeout(() => { reportPanel.scrollTop = 0; }, 100);
}

// ── Email Template Builder ──────────────────────────────────────
function buildEmailParams(name, email, scores, overall, insights, roadmap) {
  const swLabel = overall >= 70 ? 'Healthy Business' : overall >= 50 ? 'Growing Business' : 'Needs Attention';

  const scoreLines = Object.entries(scores).map(([k,v]) => `${k}: ${v}%`).join('\n');

  const strengthLines  = insights.strengths.map(s => `✅ ${s}`).join('\n');
  const weaknessLines  = insights.weaknesses.map(w => `⚠️ ${w}`).join('\n');
  const riskLines      = insights.risks.map(r => `🔴 ${r}`).join('\n');
  const hiRecLines     = insights.recommendations.high.map(r => `🔴 ${r}`).join('\n');
  const midRecLines    = insights.recommendations.medium.map(r => `🟡 ${r}`).join('\n');
  const ltRecLines     = insights.recommendations.longterm.map(r => `🔵 ${r}`).join('\n');

  const serviceLines = insights.services.map(s =>
    `▸ ${s.name} [${s.priority}]\n  → ${s.why}`
  ).join('\n\n');

  const roadmapLines = `
Month 1:
${roadmap.month1.map(t=>`  • ${t}`).join('\n')}

Month 2:
${roadmap.month2.map(t=>`  • ${t}`).join('\n')}

Month 3:
${roadmap.month3.map(t=>`  • ${t}`).join('\n')}`.trim();

  return {
    to_name:      name,
    to_email:     email,
    business_name: answers.name || 'Your Business',
    industry:     answers.industry || 'N/A',
    overall_score: `${overall} / 100 — ${swLabel}`,
    score_breakdown: scoreLines,
    strengths:    strengthLines || 'None identified',
    weaknesses:   weaknessLines || 'None identified',
    risks:        riskLines     || 'None identified',
    high_priority:  hiRecLines  || 'None',
    medium_priority: midRecLines|| 'None',
    long_term:    ltRecLines    || 'None',
    amee_services: serviceLines,
    roadmap:      roadmapLines,
    goal:         answers.goal   || 'Not specified',
    barrier:      answers.barrier || 'Not specified',
    // Amee Technology contact details embedded in email
    amee_whatsapp:  '+234 810 001 5498',
    amee_phone:     '+234 810 001 5498',
    amee_email:     'technologyamee@gmail.com',
    amee_website:   'https://ameetechnology.com',
    amee_form:      'https://forms.gle/zzL8UaQjkGhGcXHs5',
    report_date:    new Date().toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'}),
  };
}

// ── Report HTML ─────────────────────────────────────────────────
function buildReportHTML(scores, overall, insights, roadmap) {
  const scoreBarItems = Object.entries(scores).map(([k,v]) =>
    `<div class="ab-score-bar-item">
       <span>${k}</span>
       <div class="ab-bar-track"><div class="ab-bar-fill" style="width:${v}%;--c:${scoreColor(v)}"></div></div>
       <b>${v}%</b>
     </div>`).join('');

  const swLabel = overall >= 70 ? 'Healthy Business' : overall >= 50 ? 'Growing Business' : 'Needs Attention';

  const strengthItems = insights.strengths.map(s =>
    `<div class="ab-report-item strength-item"><i class="fa-solid fa-check-circle"></i><span>${s}</span></div>`).join('');
  const weaknessItems = insights.weaknesses.map(w =>
    `<div class="ab-report-item weakness-item"><i class="fa-solid fa-circle-xmark"></i><span>${w}</span></div>`).join('');
  const riskItems = insights.risks.map(r =>
    `<div class="ab-report-item risk-item"><i class="fa-solid fa-triangle-exclamation"></i><span>${r}</span></div>`).join('');
  const hiRecs  = insights.recommendations.high.map(r => `<div class="ab-rec-item"><i class="fa-solid fa-circle-check"></i>${r}</div>`).join('');
  const midRecs = insights.recommendations.medium.map(r => `<div class="ab-rec-item"><i class="fa-solid fa-circle-check"></i>${r}</div>`).join('');
  const ltRecs  = insights.recommendations.longterm.map(r => `<div class="ab-rec-item"><i class="fa-solid fa-circle-check"></i>${r}</div>`).join('');

  const roadmapHTML = `
    <div class="ab-roadmap-month"><div class="ab-roadmap-month-tag">Month 1</div><div class="ab-roadmap-tasks">${roadmap.month1.map(t=>`<div class="ab-roadmap-task"><i class="fa-solid fa-circle-dot"></i>${t}</div>`).join('')}</div></div>
    <div class="ab-roadmap-month"><div class="ab-roadmap-month-tag">Month 2</div><div class="ab-roadmap-tasks">${roadmap.month2.map(t=>`<div class="ab-roadmap-task"><i class="fa-solid fa-circle-dot"></i>${t}</div>`).join('')}</div></div>
    <div class="ab-roadmap-month"><div class="ab-roadmap-month-tag">Month 3</div><div class="ab-roadmap-tasks">${roadmap.month3.map(t=>`<div class="ab-roadmap-task"><i class="fa-solid fa-circle-dot"></i>${t}</div>`).join('')}</div></div>`;

  const servicesHTML = insights.services.map(s => `
    <div class="ab-service-rec-item">
      <div class="ab-service-rec-icon"><i class="fa-solid ${s.icon}"></i></div>
      <div class="ab-service-rec-text">
        <h4>${s.name} <span style="font-size:0.68rem;padding:2px 8px;border-radius:20px;background:rgba(168,85,247,0.25);color:#c4b5fd;margin-left:6px;">${s.priority}</span></h4>
        <p>${s.why}</p>
      </div>
    </div>`).join('');

  const waMsg = encodeURIComponent(`Hi Amee Technology! 👋 I just completed the AmeeBot business assessment for ${answers.name || 'my business'} and scored ${overall}/100. I'd love to discuss how you can help me improve. Can we talk?`);

  return `
    <div class="ab-report-header">
      <h2>Business Assessment Report</h2>
      <p>Personalised for <b>${answers.name || 'Your Business'}</b> · ${answers.industry || ''} · ${new Date().toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'})}</p>
    </div>

    <div class="ab-report-score">
      <div class="ab-score-circle">
        <svg viewBox="0 0 110 110" id="ab-score-svg">
          <circle cx="55" cy="55" r="46" class="ab-rc-bg"/>
          <circle cx="55" cy="55" r="46" class="ab-rc-fill" id="ab-rc-fill-circle" stroke-dasharray="0 289" stroke-dashoffset="0"/>
        </svg>
        <div class="ab-score-circle-inner"><span class="n" id="ab-score-display">0</span><span class="d">/ 100</span></div>
      </div>
      <div class="ab-score-right">
        <h3>📊 Business Health Score – <span style="color:${scoreColor(overall)}">${swLabel}</span></h3>
        <div class="ab-score-bars">${scoreBarItems}</div>
      </div>
    </div>

    <div class="ab-report-block">
      <div class="ab-report-block-header strength"><i class="fa-solid fa-trophy"></i> Strengths</div>
      <div class="ab-report-block-body">${strengthItems || '<div class="ab-report-item">Keep building on your current foundation.</div>'}</div>
    </div>

    <div class="ab-report-block">
      <div class="ab-report-block-header weakness"><i class="fa-solid fa-circle-exclamation"></i> Weaknesses to Address</div>
      <div class="ab-report-block-body">${weaknessItems || '<div class="ab-report-item">No major weaknesses detected. Keep it up!</div>'}</div>
    </div>

    ${insights.risks.length ? `
    <div class="ab-report-block">
      <div class="ab-report-block-header risk"><i class="fa-solid fa-triangle-exclamation"></i> Business Risks</div>
      <div class="ab-report-block-body">${riskItems}</div>
    </div>` : ''}

    <div class="ab-report-block">
      <div class="ab-report-block-header recommendation"><i class="fa-solid fa-lightbulb"></i> Action Recommendations</div>
      <div class="ab-report-block-body">
        ${hiRecs  ? `<div class="ab-rec-group"><h4>🔴 High Priority — Do These First</h4>${hiRecs}</div>` : ''}
        ${midRecs ? `<div class="ab-rec-group"><h4>🟡 Medium Priority</h4>${midRecs}</div>` : ''}
        ${ltRecs  ? `<div class="ab-rec-group"><h4>🔵 Long-Term Growth</h4>${ltRecs}</div>` : ''}
      </div>
    </div>

    <div class="ab-report-block">
      <div class="ab-report-block-header roadmap"><i class="fa-solid fa-road"></i> Your 3-Month Growth Roadmap</div>
      <div class="ab-report-block-body"><div class="ab-roadmap-months">${roadmapHTML}</div></div>
    </div>

    ${insights.services.length ? `
    <div class="ab-report-block">
      <div class="ab-report-block-header amee-services"><i class="fa-solid fa-star"></i> How Amee Technology Can Help You</div>
      <div class="ab-report-block-body">
        <p style="font-size:0.82rem;color:#c4b5fd;margin-bottom:12px;">Based on your assessment results, these services directly address your identified weaknesses and growth opportunities:</p>
        <div class="ab-service-recs">${servicesHTML}</div>
      </div>
    </div>` : ''}

    <!-- Contact Amee Technology -->
    <div class="ab-report-contact">
      <div class="ab-report-contact-header">
        <i class="fa-solid fa-handshake"></i> Contact Amee Technology — We're Ready to Help
      </div>
      <div class="ab-report-contact-body">
        <p style="font-size:0.82rem;color:#9ca3af;margin-bottom:4px;">Reach out right now and mention your AmeeBot assessment score for a <b style="color:#a78bfa">free 30-minute strategy consultation</b>.</p>
        <a href="https://wa.me/2348100015498?text=${waMsg}" target="_blank" class="ab-contact-row">
          <div class="ab-contact-row-icon wa"><i class="fa-brands fa-whatsapp"></i></div>
          <div class="ab-contact-row-text"><b>WhatsApp (Fastest)</b><span>+234 810 001 5498 · Typically replies within minutes</span></div>
        </a>
        <a href="tel:+2348100015498" class="ab-contact-row">
          <div class="ab-contact-row-icon ph"><i class="fa-solid fa-phone"></i></div>
          <div class="ab-contact-row-text"><b>Call Us</b><span>+234 810 001 5498</span></div>
        </a>
        <a href="mailto:technologyamee@gmail.com?subject=AmeeBot Assessment – ${encodeURIComponent(answers.name||'My Business')}&body=Hi Amee Technology, I completed the AmeeBot assessment and scored ${overall}/100. I'd like to discuss how you can help." class="ab-contact-row">
          <div class="ab-contact-row-icon em"><i class="fa-solid fa-envelope"></i></div>
          <div class="ab-contact-row-text"><b>Email Us</b><span>technologyamee@gmail.com</span></div>
        </a>
        <a href="https://forms.gle/zzL8UaQjkGhGcXHs5" target="_blank" class="ab-contact-row">
          <div class="ab-contact-row-icon fm"><i class="fa-solid fa-file-signature"></i></div>
          <div class="ab-contact-row-text"><b>Start a Project</b><span>Fill our project brief and we'll respond within 24 hours</span></div>
        </a>
        <a href="https://ameetechnology.com" target="_blank" class="ab-contact-row">
          <div class="ab-contact-row-icon" style="background:rgba(168,85,247,0.2);color:#a855f7"><i class="fa-solid fa-globe"></i></div>
          <div class="ab-contact-row-text"><b>Visit Our Website</b><span>ameetechnology.com · See our full portfolio & services</span></div>
        </a>
      </div>
    </div>

    <div class="ab-report-cta">
      <h3>Ready to Transform Your Business?</h3>
      <p>Amee Technology Ltd specialises in turning these recommendations into reality — fast, professionally, and at the right price for your budget.</p>
      <div class="ab-report-cta-btns">
        <a href="https://wa.me/2348100015498?text=${waMsg}" target="_blank" class="ab-cta-primary"><i class="fa-brands fa-whatsapp"></i> Chat on WhatsApp Now</a>
        <a href="https://forms.gle/zzL8UaQjkGhGcXHs5" target="_blank" class="ab-cta-secondary"><i class="fa-solid fa-file-signature"></i> Start a Project</a>
      </div>
    </div>`;
}

// ── Score Ring Animation ─────────────────────────────────────────
function animateScoreRing(target) {
  const circumference = 2 * Math.PI * 46;
  const circle  = document.getElementById('ab-rc-fill-circle');
  const display = document.getElementById('ab-score-display');
  if (!circle || !display) return;
  let current = 0;
  const step = target / 60;
  const interval = setInterval(() => {
    current = Math.min(current + step, target);
    const filled = (current / 100) * circumference;
    circle.setAttribute('stroke-dasharray', `${filled} ${circumference}`);
    display.textContent = Math.round(current);
    if (current >= target) clearInterval(interval);
  }, 16);
}

function scoreColor(v) {
  if (v >= 75) return '#16a34a';
  if (v >= 55) return '#d97706';
  return '#dc2626';
}

// ── Utilities ───────────────────────────────────────────────────
function delay(ms)    { return new Promise(r => setTimeout(r, ms)); }
function escHtml(str) { return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function isValidEmail(e) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e); }
