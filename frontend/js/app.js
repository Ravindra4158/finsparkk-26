/* ═══════════════════════════════════════════════════════════
   BANKGUARD ENTERPRISE — Dashboard Application
   ═══════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ─── COLOR TOKENS ──────────────────────────────────── */
  const COLORS = {
    bg:      '#060D1A',
    surface: '#091524',
    card:    '#0D1B2E',
    border:  '#162840',
    text:    '#C8DCF2',
    muted:   '#4A6482',
    cyan:    '#00C8F8',
    green:   '#00D78F',
    amber:   '#F5A623',
    purple:  '#9260FF',
    orange:  '#FF7230',
    red:     '#FF3B5C',
    neon:    '#00FFB2',
  };

  /* ─── MOCK ALERT DATA ───────────────────────────────── */
  const ALERTS = [
    { id: 'ALT-7842', entity: 'R. Sharma / ADM-07',        module: 'Behavior', riskScore: 92, threatLevel: 'critical', timestamp: '2026-07-13T21:47:00Z', reason: 'Off-hours SWIFT override access + new device fingerprint detected from unusual IP' },
    { id: 'ALT-7841', entity: 'Meridian Exports Pvt Ltd',  module: 'SWIFT',    riskScore: 87, threatLevel: 'critical', timestamp: '2026-07-13T21:32:00Z', reason: 'Beneficiary mismatch in SWIFT MT103 + high-value cross-border transfer to sanctioned jurisdiction' },
    { id: 'ALT-7839', entity: 'K. Iyer / LO-22',           module: 'Fraud',    riskScore: 74, threatLevel: 'high',     timestamp: '2026-07-13T20:58:00Z', reason: 'Loan amount modified 3.8x above approved limit + duplicate application within 24 hours' },
    { id: 'ALT-7836', entity: 'Aarav Textiles',            module: 'Loan',     riskScore: 68, threatLevel: 'high',     timestamp: '2026-07-13T20:15:00Z', reason: 'Financial statement inconsistencies + collateral valuation mismatch' },
    { id: 'ALT-7834', entity: 'Coastal Foods LLP',         module: 'KYC',      riskScore: 55, threatLevel: 'medium',   timestamp: '2026-07-13T19:44:00Z', reason: 'KYC documentation incomplete + beneficial ownership not disclosed' },
    { id: 'ALT-7830', entity: 'N. Khan / BM-04',           module: 'Behavior', riskScore: 48, threatLevel: 'medium',   timestamp: '2026-07-13T18:30:00Z', reason: 'Unusual bulk customer record access pattern + abnormal report generation' },
    { id: 'ALT-7827', entity: 'Sterling Minerals',         module: 'Fraud',    riskScore: 41, threatLevel: 'medium',   timestamp: '2026-07-13T17:20:00Z', reason: 'Multiple failed authentication attempts followed by successful login' },
    { id: 'ALT-7825', entity: 'Evergreen Traders',         module: 'AML',      riskScore: 33, threatLevel: 'low',      timestamp: '2026-07-13T16:05:00Z', reason: 'Minor PEP name match in transaction screening + low confidence score' },
    { id: 'ALT-7822', entity: 'Pacific Machinery Co.',     module: 'Loan',     riskScore: 25, threatLevel: 'low',      timestamp: '2026-07-13T14:50:00Z', reason: 'Standard industry risk profile + established customer history' },
    { id: 'ALT-7819', entity: 'Summit Retail Group',       module: 'KYC',      riskScore: 18, threatLevel: 'low',      timestamp: '2026-07-13T13:30:00Z', reason: 'Complete KYC documentation + verified business address' },
  ];

  const EMPLOYEES = [
    { name: 'Rohan Sharma', code: 'ADM-07', branch: 'Mumbai Fort', branchKey: 'mumbai', role: 'Branch Manager', lastLogin: '2026-07-13T21:47:00Z', device: 'New Windows device / 103.88.21.14', score: 92, signal: 'Off-hours login + SWIFT override attempt', reason: 'Device is new to system, access pattern deviates from baseline, and SWIFT overrides flagged by compliance' },
    { name: 'Kavya Iyer', code: 'LO-22', branch: 'Mumbai Fort', branchKey: 'mumbai', role: 'Loan Officer', lastLogin: '2026-07-13T20:58:00Z', device: 'Known laptop / 10.4.18.22', score: 74, signal: 'Loan edits 3.8x above peer baseline', reason: 'Editing frequency and amounts exceed typical peer behavior by 3.8x - potential fraud indicator' },
    { name: 'Nadeem Khan', code: 'BM-04', branch: 'Delhi CP', branchKey: 'delhi', role: 'Branch Manager', lastLogin: '2026-07-13T18:30:00Z', device: 'Mobile browser / 49.37.8.12', score: 48, signal: 'Unusual customer profile access pattern', reason: 'Access to customer records shows 5x normal frequency with bulk download attempts' },
    { name: 'Meera Rao', code: 'CS-18', branch: 'Pune Camp', branchKey: 'pune', role: 'Customer Service', lastLogin: '2026-07-13T10:12:00Z', device: 'Known desktop / 10.7.2.88', score: 21, signal: 'Normal teller workflow', reason: 'All activities within normal operating parameters and approved by branch manager' },
    { name: 'Arjun Sen', code: 'CO-03', branch: 'Delhi CP', branchKey: 'delhi', role: 'Compliance Officer', lastLogin: '2026-07-13T09:44:00Z', device: 'Known desktop / 10.5.4.9', score: 16, signal: 'Routine alert review', reason: 'Standard compliance review activities with no anomalies detected' },
  ];

  const CUSTOMERS = [
    { name: 'Meridian Exports Pvt Ltd', branch: 'Mumbai Fort', id: 'CUST-44081', kyc: 'Complete', loans: '₹4.85 Cr', deposits: '₹1.20 Cr', rm: 'Rohan Sharma', score: 91, level: 'critical', reason: 'High-value transactions to sanctioned regions + complex ownership structure not fully disclosed' },
    { name: 'Aarav Textiles', branch: 'Mumbai Fort', id: 'CUST-33042', kyc: 'Review', loans: '₹2.50 Cr', deposits: '₹48 L', rm: 'Kavya Iyer', score: 68, level: 'high', reason: 'Financial statements show inconsistencies + collateral verification incomplete' },
    { name: 'Coastal Foods LLP', branch: 'Delhi CP', id: 'CUST-22319', kyc: 'Review', loans: '₹72 L', deposits: '₹93 L', rm: 'Nadeem Khan', score: 55, level: 'medium', reason: 'KYC documentation incomplete + beneficial owners not fully verified' },
    { name: 'Evergreen Traders', branch: 'Pune Camp', id: 'CUST-19022', kyc: 'Complete', loans: '₹18 L', deposits: '₹2.1 Cr', rm: 'Meera Rao', score: 33, level: 'low', reason: 'Long-standing customer with stable transaction history + full KYC documentation' },
    { name: 'Summit Retail Group', branch: 'Delhi CP', id: 'CUST-11872', kyc: 'Complete', loans: '₹0', deposits: '₹76 L', rm: 'Arjun Sen', score: 18, level: 'low', reason: 'Verified business operations + clean compliance history' },
  ];

  /* ─── DOM REFERENCES ────────────────────────────────── */
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  const sidebar        = $('#sidebar');
  const sidebarOverlay = $('#sidebarOverlay');
  const menuToggle     = $('#menuToggle');
  const themeToggle    = $('#themeToggle');
  const searchInput    = $('#searchInput');
  const alertBadge     = $('#alertBadge');
  const roleSelect     = $('#roleSelect');
  const userInitials   = $('#userInitials');

  const ROLE_CONFIG = {
    manager: {
      label: 'Manager',
      initials: 'BM',
      landingPage: 'dashboard',
      allowedPages: ['dashboard', 'alerts', 'loans', 'employees', 'customers', 'graph', 'swift', 'reports'],
    },
    employee: {
      label: 'Employee',
      initials: 'BE',
      landingPage: 'customers',
      allowedPages: ['dashboard', 'loans', 'customers'],
    },
  };

  let currentRole = localStorage.getItem('bankguard-role') || 'manager';

  /* ═══════════════════════════════════════════════════════
     ROUTING (SPA)
     ═══════════════════════════════════════════════════════ */
  function navigateTo(pageId) {
    const role = ROLE_CONFIG[currentRole] || ROLE_CONFIG.manager;
    if (!role.allowedPages.includes(pageId)) {
      pageId = role.landingPage;
    }

    // Hide all pages
    $$('.page').forEach(page => page.classList.remove('page--active'));
    // Show selected page
    const targetPage = $(`#page-${pageId}`);
    if (targetPage) targetPage.classList.add('page--active');

    // Update active nav link
    $$('.sidebar__link').forEach(link => {
      link.classList.remove('sidebar__link--active');
      if (link.dataset.page === pageId) {
        link.classList.add('sidebar__link--active');
      }
    });

    // Close sidebar on mobile
    if (window.innerWidth <= 768) closeSidebar();

    // Trigger page-specific initializations
    if (pageId === 'dashboard') {
      renderRiskChart();
    } else if (pageId === 'alerts') {
      renderFullAlerts();
    } else if (pageId === 'loans') {
      renderLoans();
    } else if (pageId === 'employees') {
      renderEmployees();
    } else if (pageId === 'customers') {
      renderCustomers();
    } else if (pageId === 'swift') {
      renderSwift();
    } else if (pageId === 'reports') {
      renderReports();
    }
  }

  $$('.sidebar__link[data-page]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      navigateTo(link.dataset.page);
    });
  });

  function applyRBAC(roleName) {
    const role = ROLE_CONFIG[roleName] || ROLE_CONFIG.manager;
    currentRole = roleName in ROLE_CONFIG ? roleName : 'manager';
    localStorage.setItem('bankguard-role', currentRole);

    if (roleSelect) roleSelect.value = currentRole;
    if (userInitials) userInitials.textContent = role.initials;
    document.documentElement.setAttribute('data-role', currentRole);

    $$('.sidebar__link[data-page]').forEach((link) => {
      const allowedRoles = (link.dataset.roles || 'manager,employee').split(',');
      const isAllowed = allowedRoles.includes(currentRole);
      link.hidden = !isAllowed;
      link.setAttribute('aria-hidden', String(!isAllowed));
    });

    const activePage = $('.page--active')?.id.replace('page-', '') || role.landingPage;
    if (!role.allowedPages.includes(activePage)) {
      navigateTo(role.landingPage);
    }
  }

  /* ═══════════════════════════════════════════════════════
     SIDEBAR NAVIGATION TOGGLE
     ═══════════════════════════════════════════════════════ */
  function openSidebar() {
    sidebar.classList.add('sidebar--open');
    sidebarOverlay.classList.add('sidebar-overlay--visible');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('sidebar--open');
    sidebarOverlay.classList.remove('sidebar-overlay--visible');
    document.body.style.overflow = '';
  }

  menuToggle.addEventListener('click', () => {
    sidebar.classList.contains('sidebar--open') ? closeSidebar() : openSidebar();
  });

  sidebarOverlay.addEventListener('click', closeSidebar);

  /* ═══════════════════════════════════════════════════════
     DARK / LIGHT THEME TOGGLE
     ═══════════════════════════════════════════════════════ */
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('bankguard-theme', next);
  }

  function loadTheme() {
    const saved = localStorage.getItem('bankguard-theme');
    if (saved) {
      document.documentElement.setAttribute('data-theme', saved);
    }
  }

  themeToggle.addEventListener('click', toggleTheme);

  /* ═══════════════════════════════════════════════════════
     ANIMATED STAT COUNTERS
     ═══════════════════════════════════════════════════════ */
  function animateCounter(el, target, duration = 1800) {
    const start = performance.now();
    const from = 0;

    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(from + (target - from) * eased);

      el.textContent = current.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    }
    requestAnimationFrame(tick);
  }

  function initCounters() {
    $$('.stat-card__value[data-target]').forEach((el) => {
      const target = parseInt(el.getAttribute('data-target'), 10);
      animateCounter(el, target);
    });
  }

  /* ═══════════════════════════════════════════════════════
     TABLE RENDERERS
     ═══════════════════════════════════════════════════════ */
  function getRiskColor(score) {
    if (score >= 80) return COLORS.red;
    if (score >= 60) return COLORS.orange;
    if (score >= 40) return COLORS.amber;
    return COLORS.green;
  }

  function getThreatLevel(score) {
    if (score >= 80) return 'critical';
    if (score >= 60) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
  }

  function formatTimestamp(isoStr) {
    const d = new Date(isoStr);
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  function renderAlertRow(alert, i) {
    const moduleClass = `alert-module--${alert.module.toLowerCase()}`;
    const threatClass = `threat-badge--${alert.threatLevel}`;
    const riskColor = getRiskColor(alert.riskScore);
    const riskWidth = `${alert.riskScore}%`;

    return `
      <tr class="fade-row" style="animation-delay: ${i * 50}ms">
        <td><span class="alert-id">${alert.id}</span></td>
        <td><span class="alert-entity">${alert.entity}</span></td>
        <td><span class="alert-module ${moduleClass}">${alert.module}</span></td>
        <td>
          <div class="risk-bar">
            <div class="risk-bar__track">
              <div class="risk-bar__fill" style="width:${riskWidth};background:${riskColor}"></div>
            </div>
            <span class="risk-bar__value" style="color:${riskColor}">${alert.riskScore}</span>
          </div>
        </td>
        <td><span class="threat-badge ${threatClass}">${alert.threatLevel}</span></td>
        <td><span class="alert-timestamp">${formatTimestamp(alert.timestamp)}</span></td>
      </tr>
    `;
  }

  // Dashboard Table
  function renderDashAlerts() {
    const tbody = $('#alertsTableBody');
    if (tbody) {
      tbody.innerHTML = ALERTS.slice(0, 5).map((a, i) => renderAlertRow(a, i)).join('');
      attachDashboardAlertListeners();
    }
  }

  // Alerts Page Table
  function renderFullAlerts() {
    const tbody = $('#alertsFullBody');
    if (tbody) {
      tbody.innerHTML = ALERTS.map((alert, i) => {
        const rowHTML = renderAlertRow(alert, i);
        return rowHTML.replace('</tr>', `<td><a href="#">Investigate →</a></td></tr>`);
      }).join('');
      attachDetailViewListeners();
    }
  }

  // Loans Page Table
  function renderLoans() {
    const tbody = $('#loansBody');
    if (tbody && tbody.innerHTML === '') {
      const mockLoans = [
        { id: 'LN-8842', applicant: 'TechNova Solutions', amount: '2,500,000', officer: 'J. Smith', score: 88, status: 'Held', shap: 'High velocity | New entity' },
        { id: 'LN-8841', applicant: 'Green Earth Co', amount: '500,000', officer: 'M. Davis', score: 45, status: 'Review', shap: 'Missing KYC doc' },
        { id: 'LN-8840', applicant: 'Prime Industries', amount: '1,200,000', officer: 'A. Patel', score: 22, status: 'Approved', shap: 'Stable history' }
      ];
      tbody.innerHTML = mockLoans.map((l, i) => `
        <tr class="fade-row" style="animation-delay: ${i * 50}ms">
          <td><span class="alert-id">${l.id}</span></td>
          <td><span class="alert-entity">${l.applicant}</span></td>
          <td>${l.amount}</td>
          <td>${l.officer}</td>
          <td>
            <div class="risk-bar">
              <div class="risk-bar__track"><div class="risk-bar__fill" style="width:${l.score}%;background:${getRiskColor(l.score)}"></div></div>
              <span class="risk-bar__value" style="color:${getRiskColor(l.score)}">${l.score}</span>
            </div>
          </td>
          <td><span class="threat-badge threat-badge--${l.score > 80 ? 'critical' : (l.score > 40 ? 'medium' : 'low')}">${l.status}</span></td>
          <td><span class="alert-timestamp">${l.shap}</span></td>
        </tr>
      `).join('');
      attachDetailViewListeners();
    }
  }

  function renderEmployees() {
    const tbody = $('#employeesBody');
    const signalList = $('#behaviorSignals');
    const selectedBranch = $('#employeeBranchFilter')?.value || 'all';
    const rows = selectedBranch === 'all' ? EMPLOYEES : EMPLOYEES.filter((e) => e.branchKey === selectedBranch);

    if (tbody) {
      tbody.innerHTML = rows.map((e, i) => {
        const level = getThreatLevel(e.score);
        return `
          <tr class="fade-row" style="animation-delay: ${i * 50}ms">
            <td><span class="alert-entity">${e.name}</span><br><span class="alert-id">${e.code}</span></td>
            <td>${e.branch}</td>
            <td><span class="alert-module alert-module--behavior">${e.role}</span></td>
            <td><span class="alert-timestamp">${formatTimestamp(e.lastLogin)}</span></td>
            <td>${e.device}</td>
            <td>
              <div class="risk-bar">
                <div class="risk-bar__track"><div class="risk-bar__fill" style="width:${e.score}%;background:${getRiskColor(e.score)}"></div></div>
                <span class="risk-bar__value" style="color:${getRiskColor(e.score)}">${e.score}</span>
              </div>
            </td>
            <td><span class="threat-badge threat-badge--${level}">${e.signal}</span></td>
          </tr>
        `;
      }).join('');
      attachDetailViewListeners();
    }

    if (signalList) {
      const summary = [
        { label: 'New device fingerprint', value: '4 sessions', score: 76 },
        { label: 'Off-hour privileged access', value: '11 events', score: 88 },
        { label: 'Customer record bulk view', value: '6 employees', score: 62 },
        { label: 'Failed MFA challenge', value: '3 attempts', score: 71 },
      ];
      signalList.innerHTML = summary.map((s) => `
        <div class="signal-item">
          <div>
            <strong>${s.label}</strong>
            <span>${s.value}</span>
          </div>
          <span class="risk-pill" style="color:${getRiskColor(s.score)}">${s.score}</span>
        </div>
      `).join('');
      attachDetailViewListeners();
    }
  }

  function renderCustomers() {
    const tbody = $('#customersBody');
    const selected = $('#customerFilter')?.value || 'all';
    const rows = selected === 'all' ? CUSTOMERS : CUSTOMERS.filter((c) => c.level === selected);

    if (tbody) {
      tbody.innerHTML = rows.map((c, i) => `
        <tr class="fade-row" style="animation-delay: ${i * 50}ms">
          <td><span class="alert-entity">${c.name}</span></td>
          <td>${c.branch}</td>
          <td><span class="alert-id">${c.id}</span></td>
          <td><span class="threat-badge threat-badge--${c.kyc === 'Complete' ? 'low' : 'medium'}">${c.kyc}</span></td>
          <td>${c.loans}</td>
          <td>${c.deposits}</td>
          <td>${c.rm}</td>
          <td>
            <div class="risk-bar">
              <div class="risk-bar__track"><div class="risk-bar__fill" style="width:${c.score}%;background:${getRiskColor(c.score)}"></div></div>
              <span class="risk-bar__value" style="color:${getRiskColor(c.score)}">${c.score}</span>
            </div>
          </td>
          <td><a href="#">Open Profile</a></td>
        </tr>
      `).join('');
      attachDetailViewListeners();
    }
  }

  // SWIFT Page Table
  function renderSwift() {
    const tbody = $('#swiftBody');
    if (tbody && tbody.innerHTML === '') {
      const mockSwift = [
        { id: 'SW-MT103-92', type: 'MT103', sender: 'JPM', amount: '4,000,000', ben: 'ShellCorp Ltd', match: 'Mismatch', flag: 'High' },
        { id: 'SW-MT103-91', type: 'MT103', sender: 'HSBC', amount: '250,000', ben: 'Global Trade LLC', match: 'Matched', flag: 'Low' },
      ];
      tbody.innerHTML = mockSwift.map((s, i) => `
        <tr class="fade-row" style="animation-delay: ${i * 50}ms">
          <td><span class="alert-id">${s.id}</span></td>
          <td><span class="alert-module alert-module--swift">${s.type}</span></td>
          <td>${s.sender}</td>
          <td>${s.amount}</td>
          <td><span class="alert-entity">${s.ben}</span></td>
          <td><span class="threat-badge threat-badge--${s.match === 'Matched' ? 'low' : 'critical'}">${s.match}</span></td>
          <td><span style="color: ${s.flag === 'High' ? COLORS.red : COLORS.green}">${s.flag}</span></td>
        </tr>
      `).join('');
      attachDetailViewListeners();
    }
  }

  // Reports Page Table
  function renderReports() {
    const tbody = $('#reportsBody');
    if (tbody && tbody.innerHTML === '') {
      const mockReports = [
        { id: 'REP-102', entity: 'Meridian Capital LLC', type: 'SAR', score: 92, date: '2026-07-13', status: 'Filed' },
        { id: 'REP-101', entity: 'Weekly Audit', type: 'Audit', score: 45, date: '2026-07-12', status: 'Completed' },
      ];
      tbody.innerHTML = mockReports.map((r, i) => `
        <tr class="fade-row" style="animation-delay: ${i * 50}ms">
          <td><span class="alert-id">${r.id}</span></td>
          <td><span class="alert-entity">${r.entity}</span></td>
          <td><span class="alert-module alert-module--kyc">${r.type}</span></td>
          <td><span style="color: ${getRiskColor(r.score)}; font-weight: bold;">${r.score}</span></td>
          <td><span class="alert-timestamp">${r.date}</span></td>
          <td><span class="threat-badge threat-badge--${r.status === 'Filed' ? 'high' : 'low'}">${r.status}</span></td>
          <td><a href="#">Download PDF</a></td>
        </tr>
      `).join('');
      attachDetailViewListeners();
    }
  }


  /* ═══════════════════════════════════════════════════════
     BAR CHART — RISK DISTRIBUTION (Canvas)
     ═══════════════════════════════════════════════════════ */
  function renderRiskChart() {
    const canvas = $('#riskChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    // Resize canvas for crisp rendering
    const rect = canvas.parentElement.getBoundingClientRect();
    if(rect.width === 0) return; // Hidden
    canvas.width = rect.width * dpr;
    canvas.height = 280 * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = '280px';
    ctx.scale(dpr, dpr);

    const W = rect.width;
    const H = 280;

    // Data
    const categories = [
      { label: 'Critical', value: 23, color: COLORS.red },
      { label: 'High',     value: 38, color: COLORS.orange },
      { label: 'Medium',   value: 52, color: COLORS.amber },
      { label: 'Low',      value: 71, color: COLORS.green },
      { label: 'Info',     value: 45, color: COLORS.cyan },
    ];

    const maxVal = Math.max(...categories.map((c) => c.value));
    const padding = { top: 20, right: 20, bottom: 44, left: 20 };
    const chartW = W - padding.left - padding.right;
    const chartH = H - padding.top - padding.bottom;
    const barGap = 16;
    const barWidth = (chartW - barGap * (categories.length - 1)) / categories.length;

    // Clear
    ctx.clearRect(0, 0, W, H);

    // Draw horizontal grid lines
    const gridLines = 4;
    ctx.strokeStyle = 'rgba(22, 40, 64, 0.5)';
    ctx.lineWidth = 1;

    // Animate bars
    const animDuration = 1200;
    const startTime = performance.now();

    function drawFrame(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / animDuration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);

      // Clear chart area
      ctx.clearRect(0, 0, W, H);

      // Redraw grid
      ctx.strokeStyle = 'rgba(22, 40, 64, 0.5)';
      ctx.lineWidth = 1;
      for (let i = 0; i <= gridLines; i++) {
        const y = padding.top + (chartH / gridLines) * i;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(W - padding.right, y);
        ctx.stroke();
      }

      // Draw bars
      categories.forEach((cat, i) => {
        const x = padding.left + i * (barWidth + barGap);
        const barH = (cat.value / maxVal) * chartH * eased;
        const y = padding.top + chartH - barH;

        // Bar gradient
        const grad = ctx.createLinearGradient(x, y, x, padding.top + chartH);
        grad.addColorStop(0, cat.color);
        grad.addColorStop(1, cat.color + '33');

        // Bar shadow glow
        ctx.shadowColor = cat.color;
        ctx.shadowBlur = 12;
        ctx.shadowOffsetY = 4;

        // Draw rounded bar
        const radius = 6;
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + barWidth - radius, y);
        ctx.quadraticCurveTo(x + barWidth, y, x + barWidth, y + radius);
        ctx.lineTo(x + barWidth, padding.top + chartH);
        ctx.lineTo(x, padding.top + chartH);
        ctx.lineTo(x, y + radius);
        ctx.quadraticCurveTo(x, y, x + radius, y);
        ctx.closePath();
        ctx.fillStyle = grad;
        ctx.fill();

        // Reset shadow
        ctx.shadowColor = 'transparent';
        ctx.shadowBlur = 0;
        ctx.shadowOffsetY = 0;

        // Value on top
        if (progress > 0.4) {
          const valOpacity = Math.min((progress - 0.4) / 0.3, 1);
          ctx.fillStyle = `rgba(200, 220, 242, ${valOpacity})`;
          ctx.font = '600 12px Inter, Segoe UI, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(cat.value, x + barWidth / 2, y - 8);
        }

        // Category label
        ctx.fillStyle = COLORS.muted;
        ctx.font = '500 11px Inter, Segoe UI, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(cat.label, x + barWidth / 2, H - 12);
      });

      if (progress < 1) {
        requestAnimationFrame(drawFrame);
      }
    }

    requestAnimationFrame(drawFrame);
  }

  /* ═══════════════════════════════════════════════════════
     RESPONSIVE — handle window resize
     ═══════════════════════════════════════════════════════ */
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if($('#page-dashboard').classList.contains('page--active')){
          renderRiskChart();
      }
      if (window.innerWidth > 768) closeSidebar();
    }, 200);
  });

  /* ═══════════════════════════════════════════════════════
     DETAIL VIEW SYSTEM — Open full-page details for any row
     ═══════════════════════════════════════════════════════ */
  
  const detailView = {
    currentType: null,
    currentData: null,
    
    open(type, data) {
      this.currentType = type;
      this.currentData = data;
      const detailPage = $('#detailView');
      const detailContent = $('#detailViewContent');
      
      if (type === 'alert') {
        detailContent.innerHTML = this.renderAlertDetail(data);
      } else if (type === 'employee') {
        detailContent.innerHTML = this.renderEmployeeDetail(data);
      } else if (type === 'customer') {
        detailContent.innerHTML = this.renderCustomerDetail(data);
      } else if (type === 'loan') {
        detailContent.innerHTML = this.renderLoanDetail(data);
      } else if (type === 'swift') {
        detailContent.innerHTML = this.renderSwiftDetail(data);
      } else if (type === 'report') {
        detailContent.innerHTML = this.renderReportDetail(data);
      }
      
      detailPage.classList.add('detail-view--active');
      document.body.style.overflow = 'hidden';
    },
    
    close() {
      const detailPage = $('#detailView');
      detailPage.classList.remove('detail-view--active');
      document.body.style.overflow = '';
      this.currentType = null;
      this.currentData = null;
    },
    
    renderAlertDetail(alert) {
      const riskColor = getRiskColor(alert.riskScore);
      return `
        <div class="detail-header">
          <button class="detail-close" onclick="app.detailView.close()">← Back to Alerts</button>
          <h1>${alert.id}</h1>
        </div>
        <div class="detail-body">
          <div class="detail-section">
            <h2>Alert Summary</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Entity / Subject</label>
                <value>${alert.entity}</value>
              </div>
              <div class="detail-field">
                <label>Module</label>
                <span class="alert-module alert-module--${alert.module.toLowerCase()}">${alert.module}</span>
              </div>
              <div class="detail-field">
                <label>Risk Score</label>
                <value style="color: ${riskColor}; font-weight: bold; font-size: 1.2em;">${alert.riskScore}%</value>
              </div>
              <div class="detail-field">
                <label>Threat Level</label>
                <span class="threat-badge threat-badge--${alert.threatLevel}">${alert.threatLevel.toUpperCase()}</span>
              </div>
              <div class="detail-field">
                <label>Detection Time</label>
                <value>${formatTimestamp(alert.timestamp)}</value>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Why This Risk?</h2>
            <div class="signal-highlight">${alert.reason}</div>
          </div>
          
          <div class="detail-section">
            <h2>Risk Indicators</h2>
            <ul class="detail-list">
              <li>High anomaly score detected in transaction pattern</li>
              <li>Unusual time-of-day activity flagged</li>
              <li>Cross-border transfer with new beneficiary</li>
              <li>Multiple failed authentication attempts preceding transaction</li>
            </ul>
          </div>
          
          <div class="detail-section">
            <h2>Recommended Actions</h2>
            <div class="action-buttons">
              <button class="btn btn--primary">Investigate Further</button>
              <button class="btn btn--secondary">Contact Customer</button>
              <button class="btn btn--secondary">Block Transaction</button>
            </div>
          </div>
        </div>
      `;
    },
    
    renderEmployeeDetail(emp) {
      const riskColor = getRiskColor(emp.score);
      const level = getThreatLevel(emp.score);
      return `
        <div class="detail-header">
          <button class="detail-close" onclick="app.detailView.close()">← Back to Employees</button>
          <h1>${emp.name} (${emp.code})</h1>
        </div>
        <div class="detail-body">
          <div class="detail-section">
            <h2>Employee Information</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Full Name</label>
                <value>${emp.name}</value>
              </div>
              <div class="detail-field">
                <label>Employee Code</label>
                <value>${emp.code}</value>
              </div>
              <div class="detail-field">
                <label>Branch</label>
                <value>${emp.branch}</value>
              </div>
              <div class="detail-field">
                <label>Role</label>
                <span class="alert-module alert-module--behavior">${emp.role}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Behavioral Indicators</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Last Login</label>
                <value>${formatTimestamp(emp.lastLogin)}</value>
              </div>
              <div class="detail-field">
                <label>Device / IP</label>
                <value>${emp.device}</value>
              </div>
              <div class="detail-field">
                <label>Risk Score</label>
                <value style="color: ${riskColor}; font-weight: bold; font-size: 1.1em;">${emp.score}</value>
              </div>
              <div class="detail-field">
                <label>Threat Level</label>
                <span class="threat-badge threat-badge--${level}">${level.toUpperCase()}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Primary Signal</h2>
            <div class="signal-highlight">${emp.signal}</div>
          </div>
          
          <div class="detail-section">
            <h2>Why This Risk?</h2>
            <div class="signal-highlight">${emp.reason}</div>
          </div>
          
          <div class="detail-section">
            <h2>Actions</h2>
            <div class="action-buttons">
              <button class="btn btn--primary">Review History</button>
              <button class="btn btn--secondary">Set Expiration (30 min)</button>
              <button class="btn btn--secondary">Flag for Review</button>
            </div>
          </div>
        </div>
      `;
    },
    
    renderCustomerDetail(cust) {
      const riskColor = getRiskColor(cust.score);
      return `
        <div class="detail-header">
          <button class="detail-close" onclick="app.detailView.close()">← Back to Customers</button>
          <h1>${cust.name}</h1>
        </div>
        <div class="detail-body">
          <div class="detail-section">
            <h2>Customer Profile</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Customer Name</label>
                <value>${cust.name}</value>
              </div>
              <div class="detail-field">
                <label>Customer ID</label>
                <value>${cust.id}</value>
              </div>
              <div class="detail-field">
                <label>Branch</label>
                <value>${cust.branch}</value>
              </div>
              <div class="detail-field">
                <label>Relationship Manager</label>
                <value>${cust.rm}</value>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Compliance Status</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>KYC Status</label>
                <span class="threat-badge threat-badge--${cust.kyc === 'Complete' ? 'low' : 'medium'}">${cust.kyc}</span>
              </div>
              <div class="detail-field">
                <label>Risk Score</label>
                <value style="color: ${riskColor}; font-weight: bold; font-size: 1.1em;">${cust.score}</value>
              </div>
              <div class="detail-field">
                <label>Risk Level</label>
                <span class="threat-badge threat-badge--${cust.level}">${cust.level.toUpperCase()}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Financial Position</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Loan Portfolio</label>
                <value>${cust.loans}</value>
              </div>
              <div class="detail-field">
                <label>Deposits</label>
                <value>${cust.deposits}</value>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Why This Risk?</h2>
            <div class="signal-highlight">${cust.reason}</div>
          </div>
          
          <div class="detail-section">
            <h2>Actions</h2>
            <div class="action-buttons">
              <button class="btn btn--primary">View Full Profile</button>
              <button class="btn btn--secondary">Review Transactions</button>
              <button class="btn btn--secondary">Contact Customer</button>
            </div>
          </div>
        </div>
      `;
    },
    
    renderLoanDetail(loan) {
      const riskColor = getRiskColor(loan.score);
      const statusClass = loan.score > 80 ? 'critical' : (loan.score > 40 ? 'medium' : 'low');
      return `
        <div class="detail-header">
          <button class="detail-close" onclick="app.detailView.close()">← Back to Loans</button>
          <h1>${loan.id}</h1>
        </div>
        <div class="detail-body">
          <div class="detail-section">
            <h2>Loan Application Details</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Loan ID</label>
                <value>${loan.id}</value>
              </div>
              <div class="detail-field">
                <label>Applicant</label>
                <value>${loan.applicant}</value>
              </div>
              <div class="detail-field">
                <label>Loan Amount</label>
                <value>₹${loan.amount}</value>
              </div>
              <div class="detail-field">
                <label>Loan Officer</label>
                <value>${loan.officer}</value>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Risk Assessment</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Risk Score</label>
                <value style="color: ${riskColor}; font-weight: bold; font-size: 1.1em;">${loan.score}</value>
              </div>
              <div class="detail-field">
                <label>Status</label>
                <span class="threat-badge threat-badge--${statusClass}">${loan.status}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Risk Factors</h2>
            <ul class="detail-list">
              <li>${loan.shap}</li>
              <li>Applicant credit history review pending</li>
              <li>Collateral valuation in progress</li>
            </ul>
          </div>
          
          <div class="detail-section">
            <h2>Why This Risk?</h2>
            <div class="signal-highlight">${loan.reason}</div>
          </div>
          
          <div class="detail-section">
            <h2>Actions</h2>
            <div class="action-buttons">
              <button class="btn btn--primary">Approve Loan</button>
              <button class="btn btn--secondary">Request More Info</button>
              <button class="btn btn--secondary">Hold for Review</button>
            </div>
          </div>
        </div>
      `;
    },
    
    renderSwiftDetail(swift) {
      const matchClass = swift.match === 'Matched' ? 'low' : 'critical';
      return `
        <div class="detail-header">
          <button class="detail-close" onclick="app.detailView.close()">← Back to SWIFT</button>
          <h1>${swift.id}</h1>
        </div>
        <div class="detail-body">
          <div class="detail-section">
            <h2>SWIFT Message Details</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Message ID</label>
                <value>${swift.id}</value>
              </div>
              <div class="detail-field">
                <label>Message Type</label>
                <span class="alert-module alert-module--swift">${swift.type}</span>
              </div>
              <div class="detail-field">
                <label>Sender BIC</label>
                <value>${swift.sender}</value>
              </div>
              <div class="detail-field">
                <label>Amount</label>
                <value>₹${swift.amount}</value>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Beneficiary Information</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Beneficiary</label>
                <value>${swift.ben}</value>
              </div>
              <div class="detail-field">
                <label>Reconciliation Status</label>
                <span class="threat-badge threat-badge--${matchClass}">${swift.match}</span>
              </div>
              <div class="detail-field">
                <label>Risk Flag</label>
                <span style="color: ${swift.flag === 'High' ? COLORS.red : COLORS.green}; font-weight: bold;">${swift.flag}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Compliance Check</h2>
            <ul class="detail-list">
              <li>OFAC screening completed - no matches</li>
              <li>Sanctions list checked - clear</li>
              <li>Beneficiary KYC verified</li>
            </ul>
          </div>
          
          <div class="detail-section">
            <h2>Why This Risk?</h2>
            <div class="signal-highlight">${swift.reason}</div>
          </div>
          
          <div class="detail-section">
            <h2>Actions</h2>
            <div class="action-buttons">
              <button class="btn btn--primary">Process Transfer</button>
              <button class="btn btn--secondary">Request Clarification</button>
              <button class="btn btn--secondary">Hold for Manual Review</button>
            </div>
          </div>
        </div>
      `;
    },
    
    renderReportDetail(report) {
      const riskColor = getRiskColor(report.score);
      return `
        <div class="detail-header">
          <button class="detail-close" onclick="app.detailView.close()">← Back to Reports</button>
          <h1>${report.id}</h1>
        </div>
        <div class="detail-body">
          <div class="detail-section">
            <h2>Report Information</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Report ID</label>
                <value>${report.id}</value>
              </div>
              <div class="detail-field">
                <label>Entity</label>
                <value>${report.entity}</value>
              </div>
              <div class="detail-field">
                <label>Report Type</label>
                <span class="alert-module alert-module--kyc">${report.type}</span>
              </div>
              <div class="detail-field">
                <label>Report Date</label>
                <value>${report.date}</value>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Report Metrics</h2>
            <div class="detail-grid">
              <div class="detail-field">
                <label>Risk Score</label>
                <value style="color: ${riskColor}; font-weight: bold; font-size: 1.1em;">${report.score}</value>
              </div>
              <div class="detail-field">
                <label>Status</label>
                <span class="threat-badge threat-badge--${report.status === 'Filed' ? 'high' : 'low'}">${report.status}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h2>Document Summary</h2>
            <p>This ${report.type} report provides a comprehensive analysis of ${report.entity}. The report includes risk assessment, compliance findings, and recommended follow-up actions.</p>
          </div>
          
          <div class="detail-section">
            <h2>Why This Risk?</h2>
            <div class="signal-highlight">${report.reason}</div>
          </div>
          
          <div class="detail-section">
            <h2>Actions</h2>
            <div class="action-buttons">
              <button class="btn btn--primary">Download PDF</button>
              <button class="btn btn--secondary">Email Report</button>
              <button class="btn btn--secondary">Archive</button>
            </div>
          </div>
        </div>
      `;
    }
  };

  // Expose detailView globally for onclick handlers
  window.app = { detailView };

  function attachDashboardAlertListeners() {
    $$('#alertsTableBody tr').forEach((row) => {
      row.style.cursor = 'pointer';
      row.removeEventListener('click', row._detailClickHandler);
      row._detailClickHandler = () => {
        const alertId = row.querySelector('td:first-child')?.textContent?.trim();
        const alert = ALERTS.find(a => a.id === alertId);
        if (alert) detailView.open('alert', alert);
      };
      row.addEventListener('click', row._detailClickHandler);
    });
  }

  function attachDetailViewListeners() {
    // Alerts
    $$('#alertsFullBody tr').forEach((row) => {
      row.style.cursor = 'pointer';
      row.removeEventListener('click', row._detailClickHandler);
      row._detailClickHandler = () => {
        const alertId = row.querySelector('td:first-child')?.textContent?.trim();
        const alert = ALERTS.find(a => a.id === alertId);
        if (alert) detailView.open('alert', alert);
      };
      row.addEventListener('click', row._detailClickHandler);
    });
    
    // Employees
    $$('#employeesBody tr').forEach((row) => {
      row.style.cursor = 'pointer';
      row.removeEventListener('click', row._detailClickHandler);
      row._detailClickHandler = () => {
        const empCode = row.querySelector('td:nth-child(2)')?.textContent?.trim();
        const emp = EMPLOYEES.find(e => e.code === empCode);
        if (emp) detailView.open('employee', emp);
      };
      row.addEventListener('click', row._detailClickHandler);
    });
    
    // Customers
    $$('#customersBody tr').forEach((row) => {
      row.style.cursor = 'pointer';
      row.removeEventListener('click', row._detailClickHandler);
      row._detailClickHandler = () => {
        const custName = row.querySelector('td:first-child')?.textContent?.trim();
        const cust = CUSTOMERS.find(c => c.name === custName);
        if (cust) detailView.open('customer', cust);
      };
      row.addEventListener('click', row._detailClickHandler);
    });
    
    // Loans
    $$('#loansBody tr').forEach((row) => {
      row.style.cursor = 'pointer';
      row.removeEventListener('click', row._detailClickHandler);
      row._detailClickHandler = () => {
        const mockLoans = [
          { id: 'LN-8842', applicant: 'TechNova Solutions', amount: '2,500,000', officer: 'J. Smith', score: 88, status: 'Held', shap: 'High velocity | New entity', reason: 'Applicant is newly incorporated + unusual transaction velocity with no credit history' },
          { id: 'LN-8841', applicant: 'Green Earth Co', amount: '500,000', officer: 'M. Davis', score: 45, status: 'Review', shap: 'Missing KYC doc', reason: 'Beneficial owner documentation incomplete + business address not verified' },
          { id: 'LN-8840', applicant: 'Prime Industries', amount: '1,200,000', officer: 'A. Patel', score: 22, status: 'Approved', shap: 'Stable history', reason: 'Established business with 8+ years history + strong financial ratios' }
        ];
        const loanId = row.querySelector('td:first-child')?.textContent?.trim();
        const loan = mockLoans.find(l => l.id === loanId);
        if (loan) detailView.open('loan', loan);
      };
      row.addEventListener('click', row._detailClickHandler);
    });
    
    // SWIFT
    $$('#swiftBody tr').forEach((row) => {
      row.style.cursor = 'pointer';
      row.removeEventListener('click', row._detailClickHandler);
      row._detailClickHandler = () => {
        const mockSwift = [
          { id: 'SW-MT103-92', type: 'MT103', sender: 'JPM', amount: '4,000,000', ben: 'ShellCorp Ltd', match: 'Mismatch', flag: 'High', reason: 'Beneficiary name does not match invoice + amount exceeds contract terms' },
          { id: 'SW-MT103-91', type: 'MT103', sender: 'HSBC', amount: '250,000', ben: 'Global Trade LLC', match: 'Matched', flag: 'Low', reason: 'Standard trade transaction with verified beneficiary and matching documentation' },
        ];
        const swiftId = row.querySelector('td:first-child')?.textContent?.trim();
        const swift = mockSwift.find(s => s.id === swiftId);
        if (swift) detailView.open('swift', swift);
      };
      row.addEventListener('click', row._detailClickHandler);
    });
    
    // Reports
    $$('#reportsBody tr').forEach((row) => {
      row.style.cursor = 'pointer';
      row.removeEventListener('click', row._detailClickHandler);
      row._detailClickHandler = () => {
        const mockReports = [
          { id: 'REP-102', entity: 'Meridian Capital LLC', type: 'SAR', score: 92, date: '2026-07-13', status: 'Filed', reason: 'Suspicious activity detected: structuring pattern + rapid fund transfers to high-risk jurisdictions' },
          { id: 'REP-101', entity: 'Weekly Audit', type: 'Audit', score: 45, date: '2026-07-12', status: 'Completed', reason: 'Routine compliance audit with no material findings or control deficiencies' },
        ];
        const reportId = row.querySelector('td:first-child')?.textContent?.trim();
        const report = mockReports.find(r => r.id === reportId);
        if (report) detailView.open('report', report);
      };
      row.addEventListener('click', row._detailClickHandler);
    });
    
    // Close detail view on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && detailView.currentType) {
        detailView.close();
      }
    });
    
    // Close detail view on outside click
    const detailPage = $('#detailView');
    if (detailPage) {
      detailPage.addEventListener('click', (e) => {
        if (e.target === detailPage) {
          detailView.close();
        }
      });
    }
  }

  /* ═══════════════════════════════════════════════════════
     INITIALIZATION
     ═══════════════════════════════════════════════════════ */
  document.addEventListener('DOMContentLoaded', () => {
    // Load saved theme
    loadTheme();

    // Init badge
    const criticalCount = ALERTS.filter((a) => a.threatLevel === 'critical' || a.threatLevel === 'high').length;
    alertBadge.textContent = criticalCount;

    // Initialize SPA to dashboard
    applyRBAC(currentRole);
    navigateTo('dashboard');
    renderDashAlerts();
    initCounters();

    $('#employeeBranchFilter')?.addEventListener('change', renderEmployees);
    $('#customerFilter')?.addEventListener('change', renderCustomers);
    roleSelect?.addEventListener('change', (event) => {
      applyRBAC(event.target.value);
      navigateTo(ROLE_CONFIG[currentRole].landingPage);
    });

    console.log(
      '%c⬢ BANKGUARD ENTERPRISE %cv1.0.0',
      'color:#00FFB2;font-weight:800;font-size:14px;',
      'color:#4A6482;font-size:12px;'
    );
  });
})();
