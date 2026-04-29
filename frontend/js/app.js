const TOKEN_KEY = 'erp_token';
const USER_KEY = 'erp_user';
const THEME_KEY = 'erp_theme';
const ASSISTANT_WIDGET_KEY = 'erp_assistant_widget_hidden';

const ROUTE_META = {
    dashboard: { title: 'Dashboard', subtitle: 'GroceryERP / Overview' },
    alerts: { title: 'Alerts', subtitle: 'GroceryERP / Notifications' },
    products: { title: 'Products', subtitle: 'GroceryERP / Product Catalog' },
    stock: { title: 'Stock Levels', subtitle: 'GroceryERP / Inventory' },
    expiry_tracking: { title: 'Expiry Tracking', subtitle: 'GroceryERP / Expiry' },
    vendors: { title: 'Vendors', subtitle: 'GroceryERP / Vendor Management' },
    purchase_orders: { title: 'Purchase Orders', subtitle: 'GroceryERP / Procurement' },
    create_po: { title: 'Create Purchase Order', subtitle: 'GroceryERP / Procurement' },
    goods_receiving: { title: 'Goods Receiving', subtitle: 'GroceryERP / Procurement / Receiving' },
    reports: { title: 'Reports', subtitle: 'GroceryERP / Analytics' },
    ai_chat: { title: 'AI Assistant', subtitle: 'GroceryERP / Smart Tools' },
    settings: { title: 'Settings', subtitle: 'GroceryERP / Preferences' },
    login: { title: 'Login', subtitle: 'Sign in to GroceryERP' },
    register: { title: 'Create account', subtitle: 'Join GroceryERP' },
};

const SAMPLE = {
    stats: [
        { label: 'Total Products', value: '1,284', hint: '+4.2%', icon: 'fa-box', tone: 'green' },
        { label: 'Active Vendors', value: '47', hint: '+2', icon: 'fa-building', tone: 'blue' },
        { label: 'Open Purchase Orders', value: '12', hint: '2 pending', icon: 'fa-file-invoice', tone: 'orange' },
        { label: 'Low Stock Items', value: '23', hint: '+3', icon: 'fa-triangle-exclamation', tone: 'red' },
        { label: 'Expiring in 7 Days', value: '8', hint: 'Critical', icon: 'fa-clock', tone: 'purple' },
        { label: 'Inventory Value', value: '$284K', hint: '+1.8%', icon: 'fa-sack-dollar', tone: 'green' },
    ],
    quickActions: [
        { label: 'New Purchase Order', icon: 'fa-clipboard', href: 'create_po.html' },
        { label: 'Check Stock Levels', icon: 'fa-chart-column', href: 'stock.html' },
        { label: 'View Expiry Status', icon: 'fa-timer', href: 'expiry_tracking.html' },
        { label: 'Add Vendor', icon: 'fa-building', href: 'vendors.html' },
    ],
    recentOrders: [
        { po: 'PO-2024-0047', vendor: 'GreenValley Farms', amount: 5357.08, status: 'Approved', date: 'Dec 15', action: 'Print' },
        { po: 'PO-2024-0046', vendor: 'SunDry Foods Co.', amount: 2890.00, status: 'Sent', date: 'Dec 14', action: 'Print' },
        { po: 'PO-2024-0045', vendor: 'Pacific Dairy Ltd.', amount: 4120.50, status: 'Received', date: 'Dec 12', action: 'Print' },
        { po: 'PO-2024-0044', vendor: 'OrchardFresh Exports', amount: 3450.00, status: 'Partially Rcvd', date: 'Dec 10', action: 'Print' },
        { po: 'PO-2024-0043', vendor: 'Metro Staples Inc.', amount: 7800.00, status: 'Draft', date: 'Dec 9', action: 'Print' },
    ],
    alerts: [
        { type: 'expired', title: 'Organic Milk', meta: 'Batch B2024-091 · 240 units', severity: 'danger' },
        { type: 'low_stock', title: 'Basmati Rice', meta: '12 bags left (min: 50)', severity: 'danger' },
        { type: 'expiry_critical', title: 'Greek Yogurt', meta: '156 units expiring soon', severity: 'warning' },
        { type: 'low_stock', title: 'Sunflower Oil', meta: '8 cases left (min: 20)', severity: 'warning' },
        { type: 'po_overdue', title: 'PO-0046 Ready to Send', meta: 'SunDry Foods Co.', severity: 'info' },
    ],
    products: [
        { name: 'Kashmiri Red Apples', sku: 'GRN-001', category: 'Fresh Produce', unit: 'Box (20kg)', cost: 2280.00, perishable: true, shelf: '14 days' },
        { name: 'Amul Full Cream Milk 1L', sku: 'DRY-015', category: 'Dairy', unit: 'Carton (12)', cost: 864.00, perishable: true, shelf: '7 days' },
        { name: 'India Gate Basmati Rice', sku: 'DRY-042', category: 'Dry Goods', unit: 'Bag (25kg)', cost: 2560.00, perishable: false, shelf: '730 days' },
        { name: 'Fortune Sunlite Oil 5L', sku: 'OIL-007', category: 'Dry Goods', unit: 'Case (12)', cost: 4992.00, perishable: false, shelf: '365 days' },
        { name: 'Fresh Broccoli', sku: 'GRN-002', category: 'Fresh Produce', unit: 'Box (10kg)', cost: 1480.00, perishable: true, shelf: '5 days' },
    ],
    stock: [
        { name: 'Organic Red Apples', sku: 'GRN-001', location: 'Warehouse A', current: 390, total: 500, reorder: 50, status: 'Normal', tone: 'green', updated: '2 hrs ago' },
        { name: 'Basmati Rice Long Grain', sku: 'DRY-042', location: 'Warehouse C — Dry', current: 12, total: 100, reorder: 50, status: 'Low Stock', tone: 'amber', updated: '1 day ago' },
        { name: 'Sunflower Cooking Oil 5L', sku: 'OIL-007', location: 'Warehouse C — Dry', current: 8, total: 100, reorder: 20, status: 'Critical', tone: 'red', updated: '3 hrs ago' },
        { name: 'Full Cream Milk 1L', sku: 'DRY-015', location: 'Warehouse B — Cold', current: 130, total: 200, reorder: 40, status: 'Normal', tone: 'green', updated: '30 min ago' },
        { name: 'Fresh Broccoli', sku: 'GRN-002', location: 'Warehouse A', current: 56, total: 100, reorder: 20, status: 'Normal', tone: 'green', updated: '5 hrs ago' },
    ],
    expiry: [
        { product: 'Organic Full Cream Milk', vendor: 'Pacific Dairy', batch: 'B2024-091', received: 'Dec 5, 2024', expiry: 'Dec 12, 2024', days: 0, remaining: '240 units', status: 'Expired', action: 'Write Off' },
        { product: 'Greek Yogurt Tubs 500g', vendor: 'Dairy Fresh Co.', batch: 'B2024-112', received: 'Dec 12, 2024', expiry: 'Dec 18, 2024', days: 3, remaining: '156 units', status: 'Critical', action: 'Markdown' },
        { product: 'Fresh Orange Juice 1L', vendor: 'CitrusCo', batch: 'B2024-108', received: 'Dec 10, 2024', expiry: 'Dec 22, 2024', days: 7, remaining: '320 bottles', status: 'Warning', action: 'Alert' },
        { product: 'Strawberry Jam 500g', vendor: 'SweetSpread', batch: 'B2024-099', received: 'Nov 28, 2024', expiry: 'Dec 29, 2024', days: 14, remaining: '480 jars', status: 'Safe', action: 'View' },
        { product: 'Organic Red Apples', vendor: 'GreenValley Farms', batch: 'B2024-120', received: 'Dec 14, 2024', expiry: 'Dec 28, 2024', days: 13, remaining: '390 boxes', status: 'Safe', action: 'View' },
    ],
    vendors: [
        { initials: 'GV', name: 'GreenValley Farms India Pvt. Ltd.', category: 'Fresh Produce · Fruits & Veg', contact: 'Arjun Mehta', phone: '+91 98765 43210', email: 'arjun@greenvalley.in', city: 'Navi Mumbai, MH', terms: 'Net 30 Days', status: 'Active' },
        { initials: 'PD', name: 'Pacific Dairy India', category: 'Dairy & Refrigerated', contact: 'Ananya Rao', phone: '+91 98123 45678', email: 'ananya@pacificdairy.in', city: 'Bengaluru, KA', terms: 'Net 15 Days', status: 'Active' },
        { initials: 'SD', name: 'SunDry Foods Co.', category: 'Dry Goods & Staples', contact: 'Vikram Singh', phone: '+91 97654 32109', email: 'vikram@sundryfoods.in', city: 'Delhi NCR', terms: 'Net 45 Days', status: 'Active' },
        { initials: 'QS', name: 'QuickShip Wholesale', category: 'General Merchandise', contact: 'Tony Kim', phone: '+91 90000 11122', email: 'tony@quickship.in', city: 'Chennai, TN', terms: 'COD', status: 'Blacklisted' },
    ],
    purchaseOrders: [
        { po: 'PO-2024-0047', vendor: 'GreenValley Farms India Pvt. Ltd.', items: 5, total: 535708.00, order: '15 Dec 2024', expected: '20 Dec 2024', status: 'Approved', actions: ['Print', 'Send'] },
        { po: 'PO-2024-0046', vendor: 'SunDry Foods Co.', items: 3, total: 289000.00, order: '14 Dec 2024', expected: '19 Dec 2024', status: 'Sent', actions: ['Print', 'Receive'] },
        { po: 'PO-2024-0045', vendor: 'Pacific Dairy India', items: 4, total: 412050.00, order: '12 Dec 2024', expected: '17 Dec 2024', status: 'Received', actions: ['Print'] },
        { po: 'PO-2024-0044', vendor: 'OrchardFresh Exports', items: 6, total: 345000.00, order: '10 Dec 2024', expected: '16 Dec 2024', status: 'Partially Rcvd', actions: ['Print'] },
        { po: 'PO-2024-0043', vendor: 'Metro Staples Inc.', items: 8, total: 780000.00, order: '09 Dec 2024', expected: '—', status: 'Draft', actions: ['Edit', 'Print', 'Delete'] },
    ],
    receipts: [
        { po: 'PO-2024-0046', vendor: 'SunDry Foods Co.', items: '3 items · ₹2,890.00', eta: 'Due Today' },
        { po: 'PO-2024-0047', vendor: 'GreenValley Farms', items: '5 items · ₹5,357.08', eta: '20 Dec' },
    ],
    reports: [
        { key: 'stock_valuation', title: 'Stock Valuation Report', icon: 'fa-chart-column', desc: 'Total inventory value by category' },
        { key: 'expiry_analysis', title: 'Expiry Analysis', icon: 'fa-clock', desc: 'Waste and expiry loss tracking' },
        { key: 'vendor_performance', title: 'Vendor Performance', icon: 'fa-building', desc: 'Delivery times and compliance rate' },
        { key: 'purchase_history', title: 'Purchase Order History', icon: 'fa-clipboard-list', desc: 'Full PO audit trail with totals' },
        { key: 'low_stock', title: 'Low Stock Report', icon: 'fa-triangle-exclamation', desc: 'All items below reorder level' },
        { key: 'stock_movement', title: 'Stock Movement Audit', icon: 'fa-rotate', desc: 'All receipts, adjustments, and write-offs' },
    ],
    expirySummary: [
        { label: 'Expired', value: 2, tone: 'red' },
        { label: 'Critical', value: 3, tone: 'orange' },
        { label: 'Warning', value: 8, tone: 'amber' },
        { label: 'Safe', value: 19, tone: 'green' },
    ],
};

function apiBase() {
    const stored = localStorage.getItem('erp_api_base');
    if (stored) return stored.replace(/\/$/, '');
    if (window.location.protocol === 'file:') return 'http://localhost:8000/api/v1';
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return window.location.port === '8000' ? `${window.location.origin}/api/v1` : 'http://localhost:8000/api/v1';
    }
    return `${window.location.origin}/api/v1`;
}

function getToken() { return localStorage.getItem(TOKEN_KEY); }
function setToken(token) { localStorage.setItem(TOKEN_KEY, token); }
function getUser() { const raw = localStorage.getItem(USER_KEY); return raw ? JSON.parse(raw) : null; }
function setUser(user) { localStorage.setItem(USER_KEY, JSON.stringify(user)); }
function isAuthenticated() { return !!getToken(); }
function logout() { localStorage.removeItem(TOKEN_KEY); localStorage.removeItem(USER_KEY); window.location.href = 'login.html'; }
function isAssistantWidgetHidden() { return localStorage.getItem(ASSISTANT_WIDGET_KEY) === '1'; }
function setAssistantWidgetHidden(hidden) { localStorage.setItem(ASSISTANT_WIDGET_KEY, hidden ? '1' : '0'); }
function toggleAssistantWidgetHidden() {
    const hidden = !isAssistantWidgetHidden();
    setAssistantWidgetHidden(hidden);
    const host = document.getElementById('assistantWidgetHost');
    if (host && hidden) host.remove();
    if (!hidden) mountAssistantWidget(normalizeRoute());
    const toggleButton = document.getElementById('toggleAssistantWidgetBtn');
    if (toggleButton) toggleButton.textContent = hidden ? 'Show' : 'Hide';
    showToast(hidden ? 'API Bridge hidden' : 'API Bridge shown', 'info');
}

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

function formatApiError(errorBody, status) {
    const detail = errorBody?.detail;
    if (typeof detail === 'string') return detail;

    if (Array.isArray(detail)) {
        const messages = detail
            .map((entry) => {
                const field = Array.isArray(entry.loc) ? entry.loc.slice(1).join('.') : '';
                const message = entry.msg || 'Invalid value';
                return field ? `${field}: ${message}` : message;
            })
            .filter(Boolean);
        if (messages.length) return messages.join('; ');
    }

    if (detail && typeof detail === 'object') {
        return detail.message || JSON.stringify(detail);
    }

    return `API Error ${status}`;
}

async function api(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {}),
    };

    try {
        const response = await fetch(`${apiBase()}${endpoint}`, { ...options, headers });
        if (response.status === 401) {
            logout();
            return null;
        }
        if (!response.ok) {
            const errorBody = await response.json().catch(() => ({}));
            throw new Error(formatApiError(errorBody, response.status));
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

const apiGet = (endpoint) => api(endpoint);
const apiPost = (endpoint, payload) => api(endpoint, { method: 'POST', body: JSON.stringify(payload) });
const apiPut = (endpoint, payload) => api(endpoint, { method: 'PUT', body: JSON.stringify(payload) });
const apiDelete = (endpoint) => api(endpoint, { method: 'DELETE' });

function getTheme() { return localStorage.getItem(THEME_KEY) || 'light'; }
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    const icon = document.getElementById('themeIcon');
    if (icon) icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}
function toggleTheme() { setTheme(getTheme() === 'dark' ? 'light' : 'dark'); }
function initTheme() { setTheme(getTheme()); }

function normalizeRoute() {
    const file = window.location.pathname.split('/').pop().toLowerCase();
    if (!file || file === 'index.html') return 'dashboard';
    return file.replace('.html', '');
}

function setPageTitle(route) {
    const meta = ROUTE_META[route] || ROUTE_META.dashboard;
    const title = document.getElementById('pageTitle');
    if (title) title.textContent = meta.title;
    const subtitle = document.getElementById('pageSubtitle');
    if (subtitle) subtitle.textContent = meta.subtitle;
    document.title = `GroceryERP · ${meta.title}`;
}

function highlightActiveNav(route = normalizeRoute()) {
    document.querySelectorAll('.nav-link').forEach((link) => {
        link.classList.toggle('active', link.dataset.page === route);
    });
}

function showToast(message, type = 'info', duration = 4000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    const icons = {
        success: 'fa-circle-check',
        error: 'fa-circle-xmark',
        warning: 'fa-triangle-exclamation',
        info: 'fa-circle-info',
    };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas ${icons[type] || icons.info} toast-icon"></i><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function showSpinner() {
    if (document.querySelector('.spinner-overlay')) return;
    const overlay = document.createElement('div');
    overlay.className = 'spinner-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

function hideSpinner() {
    const overlay = document.querySelector('.spinner-overlay');
    if (overlay) overlay.remove();
}

async function loadComponent(id, url) {
    try {
        const response = await fetch(url);
        if (!response.ok) return;
        const element = document.getElementById(id);
        if (element) element.innerHTML = await response.text();
    } catch (error) {
        console.warn('Component load failed:', url, error);
    }
}

function formatINR(amount) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount || 0);
}

function formatDate(dateString) {
    if (!dateString) return '—';
    const date = new Date(dateString);
    return Number.isNaN(date.getTime()) ? dateString : date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function statusBadge(status) {
    const safe = (status || '').toLowerCase().replace(/\s+/g, '_');
    return `<span class="status-badge ${safe}">${status}</span>`;
}

function pill(text, tone = 'green') {
    return `<span class="pill ${tone}">${text}</span>`;
}

const REPORT_ENDPOINTS = {
    stock_valuation: '/reports/stock-valuation',
    expiry_analysis: '/reports/expiry-analysis',
    vendor_performance: '/reports/vendor-performance',
    purchase_history: '/reports/purchase-history',
    low_stock: '/reports/low-stock',
    stock_movement: '/reports/stock-movement',
};

function safeReportLabel(reportKey) {
    return (reportKey || '').replace(/_/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase());
}

function buildReportPreview(reportKey, data) {
    if (!data) {
        return '<div class="report-empty">No data returned.</div>';
    }

    if (reportKey === 'stock_valuation') {
        const rows = (data.items || []).map((item) => `<tr><td class="font-mono">${item.product_id}</td><td>${item.qty}</td><td>${formatINR(item.avg_cost)}</td><td><strong>${formatINR(item.value)}</strong></td></tr>`).join('');
        return `
            <div class="report-summary-grid">
                <div class="mini-kpi green"><strong>${formatINR(data.total_value)}</strong><span>Total Stock Value</span></div>
                <div class="mini-kpi blue"><strong>${(data.items || []).length}</strong><span>Products Counted</span></div>
            </div>
            <div class="table-container compact-report"><table><thead><tr><th>Product ID</th><th>Qty</th><th>Avg Cost</th><th>Value</th></tr></thead><tbody>${rows || '<tr><td colspan="4">No stock data available</td></tr>'}</tbody></table></div>
        `;
    }

    if (reportKey === 'expiry_analysis') {
        return `
            <div class="report-summary-grid">
                <div class="mini-kpi red"><strong>${data.expired}</strong><span>Expired</span></div>
                <div class="mini-kpi amber"><strong>${data.critical_7_days}</strong><span>Critical 7 Days</span></div>
                <div class="mini-kpi green"><strong>${data.warning_30_days}</strong><span>Warning 30 Days</span></div>
            </div>
        `;
    }

    if (reportKey === 'vendor_performance') {
        const rows = (data.items || []).map((item) => `<tr><td>${item.vendor_name}</td><td>${item.po_count}</td><td><strong>${formatINR(item.total_spend)}</strong></td></tr>`).join('');
        return `<div class="table-container compact-report"><table><thead><tr><th>Vendor</th><th>PO Count</th><th>Total Spend</th></tr></thead><tbody>${rows || '<tr><td colspan="3">No vendor data available</td></tr>'}</tbody></table></div>`;
    }

    if (reportKey === 'purchase_history') {
        const rows = (data.items || []).map((item) => `<tr><td class="font-mono">${item.po_number}</td><td>${formatDate(item.order_date)}</td><td>${statusBadge(item.status)}</td><td><strong>${formatINR(item.total_amount)}</strong></td></tr>`).join('');
        return `<div class="table-container compact-report"><table><thead><tr><th>PO Number</th><th>Order Date</th><th>Status</th><th>Total</th></tr></thead><tbody>${rows || '<tr><td colspan="4">No purchase history available</td></tr>'}</tbody></table></div>`;
    }

    if (reportKey === 'low_stock') {
        const rows = (data.items || []).map((item) => `<tr><td class="font-mono">${item.stock_id}</td><td>${item.product_id}</td><td>${item.warehouse_location}</td><td>${item.current_qty}</td><td>${item.reorder_level}</td></tr>`).join('');
        return `<div class="table-container compact-report"><table><thead><tr><th>Stock ID</th><th>Product ID</th><th>Warehouse</th><th>Current</th><th>Reorder</th></tr></thead><tbody>${rows || '<tr><td colspan="5">No low-stock items found</td></tr>'}</tbody></table></div>`;
    }

    if (reportKey === 'stock_movement') {
        const rows = (data.items || []).map((item) => `<tr><td class="font-mono">${item.id}</td><td>${item.movement_type}</td><td>${item.quantity}</td><td>${formatDate(item.created_at)}</td></tr>`).join('');
        return `<div class="table-container compact-report"><table><thead><tr><th>ID</th><th>Type</th><th>Qty</th><th>Created</th></tr></thead><tbody>${rows || '<tr><td colspan="4">No movement data available</td></tr>'}</tbody></table></div>`;
    }

    return `<pre class="report-json">${JSON.stringify(data, null, 2)}</pre>`;
}

function renderReportOutput(reportKey, data) {
    const output = document.getElementById('reportOutput');
    if (!output) return;
    output.innerHTML = `
        <div class="report-output-head">
            <div>
                <strong>${safeReportLabel(reportKey)}</strong>
                <div class="text-muted text-sm">Live backend response loaded successfully.</div>
            </div>
            <button class="btn btn-secondary btn-sm" id="downloadCurrentReport">Download JSON</button>
        </div>
        ${buildReportPreview(reportKey, data)}
    `;
    window.__lastReportData = { reportKey, data };

    const downloadCurrentReport = document.getElementById('downloadCurrentReport');
    if (downloadCurrentReport) {
        downloadCurrentReport.onclick = () => downloadReportJson(reportKey, data);
    }
}

function downloadReportJson(reportKey, data) {
    const blob = new Blob([JSON.stringify({ report: reportKey, generated_at: new Date().toISOString(), data }, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${reportKey || 'report'}.json`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
}

async function loadReport(reportKey) {
    const endpoint = REPORT_ENDPOINTS[reportKey];
    if (!endpoint) {
        showToast('Unknown report selected', 'warning');
        return;
    }

    const output = document.getElementById('reportOutput');
    if (output) output.innerHTML = `<div class="report-loading">Generating ${safeReportLabel(reportKey)}...</div>`;

    try {
        const data = await apiGet(endpoint);
        renderReportOutput(reportKey, data);
        showToast(`${safeReportLabel(reportKey)} generated`, 'success');
    } catch (error) {
        if (output) output.innerHTML = `<div class="report-error">${error.message || 'Report generation failed.'}</div>`;
        showToast(error.message || 'Report generation failed', 'error');
    }
}

function metricCard(stat) {
    return `
        <article class="stat-card ${stat.tone}">
            <div class="stat-info">
                <h4>${stat.label}</h4>
                <div class="stat-value">${stat.value}</div>
                <div class="stat-sub">${stat.hint}</div>
            </div>
            <div class="stat-icon ${stat.tone}"><i class="fas ${stat.icon}"></i></div>
        </article>
    `;
}

function quickActionCard(action) {
    return `
        <a class="quick-action-card" href="${action.href}">
            <span class="quick-action-icon"><i class="fas ${action.icon}"></i></span>
            <span>${action.label}</span>
        </a>
    `;
}

function renderDashboard() {
    const recentRows = SAMPLE.recentOrders.map((order) => `
        <tr>
            <td class="font-mono">${order.po}</td>
            <td>${order.vendor}</td>
            <td><strong>${formatINR(order.amount)}</strong></td>
            <td>${statusBadge(order.status)}</td>
            <td>${order.date}</td>
            <td><a href="#" class="ghost-link">Print</a></td>
        </tr>
    `).join('');

    const alertRows = SAMPLE.alerts.map((alert) => `
        <div class="alert-item ${alert.severity}">
            <div class="alert-icon ${alert.type}"><i class="fas ${alert.type === 'expired' ? 'fa-circle-xmark' : alert.type === 'low_stock' ? 'fa-box' : 'fa-triangle-exclamation'}"></i></div>
            <div class="alert-copy">
                <strong>${alert.title}</strong>
                <div class="text-muted text-sm">${alert.meta}</div>
            </div>
        </div>
    `).join('');

    const expiringRows = SAMPLE.expiry.slice(0, 2).map((row) => `
        <div class="list-row">
            <div>
                <strong>${row.product}</strong>
                <div class="text-muted text-sm">${row.remaining} · ${row.vendor}</div>
            </div>
            <div class="days-badge ${row.days === 0 ? 'danger' : 'warning'}">${row.days} day${row.days === 1 ? '' : 's'}</div>
        </div>
    `).join('');

    const bars = [54, 66, 72, 61, 78, 69, 74, 66, 71, 84, 68, 77]
        .map((height) => `<span style="height:${height}%"></span>`)
        .join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Dashboard</h1>
                    <p>Indian wholesale inventory, procurement, and expiry tracking in one place.</p>
                </div>
                <div class="toolbar">
                    <a class="btn btn-secondary btn-sm" href="reports.html"><i class="fas fa-chart-line"></i> Export</a>
                    <a class="btn btn-primary btn-sm" href="create_po.html"><i class="fas fa-plus"></i> New PO</a>
                </div>
            </div>

            <div class="stats-grid">
                ${SAMPLE.stats.map(metricCard).join('')}
            </div>

            <div class="quick-action-grid">
                ${SAMPLE.quickActions.map(quickActionCard).join('')}
            </div>

            <div class="dashboard-layout">
                <section class="table-container dashboard-main">
                    <div class="table-header">
                        <div>
                            <h3>Recent Purchase Orders</h3>
                            <div class="table-caption">Live procurement activity</div>
                        </div>
                        <a class="ghost-link" href="purchase_orders.html">View All →</a>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>PO Number</th>
                                <th>Vendor</th>
                                <th>Amount</th>
                                <th>Status</th>
                                <th>Date</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>${recentRows}</tbody>
                    </table>
                </section>

                <aside class="glass-card dashboard-side">
                    <div class="section-title-row">
                        <h3>Active Alerts</h3>
                        <span class="alert-count">7</span>
                    </div>
                    <div class="list-stack">${alertRows}</div>
                    <div class="table-footer">
                        <a class="ghost-link" href="alerts.html">View all alerts</a>
                    </div>
                </aside>
            </div>

            <div class="dashboard-layout bottom-row">
                <section class="glass-card chart-card">
                    <div class="table-header compact">
                        <div>
                            <h3>Stock Overview (Last 30 Days)</h3>
                            <div class="table-caption">Purchase volume by week</div>
                        </div>
                    </div>
                    <div class="mini-chart">${bars}</div>
                </section>

                <section class="glass-card expiring-card">
                    <div class="table-header compact">
                        <div>
                            <h3>Expiring Soon</h3>
                            <div class="table-caption">Items requiring attention</div>
                        </div>
                    </div>
                    <div class="list-stack">${expiringRows}</div>
                </section>
            </div>
        </section>
    `;
}

function renderAlerts() {
    const summary = SAMPLE.expirySummary.map((item) => `<div class="mini-kpi ${item.tone}"><strong>${item.value}</strong><span>${item.label}</span></div>`).join('');
    const alerts = SAMPLE.alerts.map((alert, index) => `
        <div class="alert-row ${alert.severity}">
            <div class="alert-mark ${alert.type}"><i class="fas ${alert.type === 'expired' ? 'fa-circle-xmark' : alert.type === 'low_stock' ? 'fa-box' : 'fa-triangle-exclamation'}"></i></div>
            <div class="alert-copy">
                <div class="alert-title">${alert.type.replace(/_/g, ' ').toUpperCase()} — ${alert.title}</div>
                <div class="text-muted text-sm">${alert.meta}</div>
            </div>
            <div class="alert-actions">
                <button class="btn btn-secondary btn-sm" onclick="showToast('Marked resolved', 'success')">Resolve</button>
                ${index < 2 ? '<button class="btn btn-danger btn-sm" onclick="showToast(\'Action queued\', \'warning\')">Write Off</button>' : ''}
            </div>
        </div>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Alerts & Notifications</h1>
                    <p>7 unresolved alerts require your attention.</p>
                </div>
                <button class="btn btn-secondary btn-sm" onclick="showToast('All alerts marked resolved', 'success')"><i class="fas fa-check"></i> Mark All Resolved</button>
            </div>
            <div class="mini-kpi-grid">${summary}</div>
            <div class="tab-row">
                <button class="page-tab active">All (7)</button>
                <button class="page-tab">Expired (1)</button>
                <button class="page-tab">Expiry Warning (3)</button>
                <button class="page-tab">Low Stock (2)</button>
                <button class="page-tab">PO Alerts (1)</button>
            </div>
            <div class="panel-stack">${alerts}</div>
        </section>
    `;
}

function renderProducts() {
    const rows = SAMPLE.products.map((product) => `
        <tr>
            <td>
                <div class="table-name">${product.name}</div>
                <div class="text-muted text-sm">Barcode: ${product.sku.replace('DRY', '50')}${product.sku.includes('GRN') ? '123456789' : '987654321'}</div>
            </td>
            <td class="font-mono">${product.sku}</td>
            <td>${product.category}</td>
            <td>${product.unit}</td>
            <td><strong>${formatINR(product.cost)}</strong></td>
            <td>${product.perishable ? pill('Yes', 'amber') : pill('No', 'slate')}</td>
            <td>${product.shelf}</td>
            <td class="action-icons"><a href="#" title="Edit"><i class="fas fa-pen"></i></a><a href="#" title="View"><i class="fas fa-eye"></i></a></td>
        </tr>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Products</h1>
                    <p>Manage your product catalog (${SAMPLE.products.length * 256} products shown in this preview).</p>
                </div>
                <div class="toolbar">
                    <button class="btn btn-secondary btn-sm" onclick="showToast('CSV export queued', 'info')"><i class="fas fa-file-csv"></i> Import CSV</button>
                    <button class="btn btn-primary btn-sm" onclick="showToast('Open product form', 'success')"><i class="fas fa-plus"></i> Add Product</button>
                </div>
            </div>
            <div class="filters-bar">
                <div class="search-wrapper"><i class="fas fa-search"></i><input class="search-input" placeholder="Search by name, SKU, barcode..."></div>
                <select class="filter-select"><option>All Categories</option></select>
                <select class="filter-select"><option>All Products</option></select>
            </div>
            <section class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>SKU</th>
                            <th>Category</th>
                            <th>Unit</th>
                            <th>Cost Price</th>
                            <th>Perishable</th>
                            <th>Shelf Life</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
                <div class="pagination">
                    <button class="page-btn">← Prev</button>
                    <button class="page-btn active">1</button>
                    <button class="page-btn">2</button>
                    <button class="page-btn">3</button>
                    <button class="page-btn">Next →</button>
                </div>
            </section>
        </section>
    `;
}

function renderStock() {
    const summary = [
        { label: 'Normal Stock', value: 874, tone: 'green' },
        { label: 'Low Stock', value: 23, tone: 'amber' },
        { label: 'Critical', value: 8, tone: 'red' },
        { label: 'Out of Stock', value: 379, tone: 'blue' },
    ].map((item) => `<div class="mini-kpi ${item.tone}"><strong>${item.value}</strong><span>${item.label}</span></div>`).join('');

    const rows = SAMPLE.stock.map((row) => `
        <tr class="${row.tone === 'red' ? 'row-danger' : row.tone === 'amber' ? 'row-warning' : ''}">
            <td>
                <div class="table-name">${row.name}</div>
                <div class="text-muted text-sm">${row.sku}</div>
            </td>
            <td>${row.location}</td>
            <td>
                <div class="progress-track"><span class="progress-fill ${row.tone}" style="width:${Math.round((row.current / row.total) * 100)}%"></span></div>
                <div class="text-sm text-muted">${row.current} / ${row.total}</div>
            </td>
            <td>${row.current} / ${row.total}</td>
            <td>${row.reorder}</td>
            <td>${pill(row.status, row.tone === 'green' ? 'green' : row.tone === 'amber' ? 'amber' : 'red')}</td>
            <td>${row.updated}</td>
            <td class="action-buttons"><button class="btn btn-secondary btn-sm">Adjust</button><button class="btn btn-primary btn-sm">PO</button></td>
        </tr>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Stock Levels</h1>
                    <p>Real-time inventory across all warehouse locations.</p>
                </div>
                <div class="toolbar">
                    <button class="btn btn-secondary btn-sm"><i class="fas fa-balance-scale"></i> Adjust Stock</button>
                    <button class="btn btn-primary btn-sm"><i class="fas fa-file-export"></i> Export Report</button>
                </div>
            </div>
            <div class="filters-bar">
                <div class="search-wrapper"><i class="fas fa-search"></i><input class="search-input" placeholder="Search products..."></div>
                <select class="filter-select"><option>All Locations</option></select>
                <select class="filter-select"><option>All Stock Status</option></select>
            </div>
            <div class="mini-kpi-grid">${summary}</div>
            <section class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Location</th>
                            <th>Current Stock</th>
                            <th>Stock Level</th>
                            <th>Reorder Level</th>
                            <th>Status</th>
                            <th>Last Updated</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            </section>
        </section>
    `;
}

function renderExpiryTracking() {
    const tabs = ['All Batches', 'Expired (2)', 'Critical — ≤7 days (3)', 'Warning — ≤30 days (8)', 'Safe'];
    const rows = SAMPLE.expiry.map((row) => `
        <tr class="${row.status === 'Expired' ? 'row-danger' : row.status === 'Critical' ? 'row-warning' : ''}">
            <td>
                <div class="table-name">${row.product}</div>
                <div class="text-muted text-sm">${row.vendor}</div>
            </td>
            <td class="font-mono">${row.batch}</td>
            <td>${row.received}</td>
            <td><strong>${row.expiry}</strong></td>
            <td><span class="days-badge ${row.days === 0 ? 'danger' : row.days <= 7 ? 'warning' : 'green'}">${row.days} day${row.days === 1 ? '' : 's'}</span></td>
            <td>${row.remaining}</td>
            <td>${pill(row.status, row.status === 'Expired' ? 'red' : row.status === 'Critical' ? 'amber' : row.status === 'Warning' ? 'yellow' : 'green')}</td>
            <td><button class="btn btn-sm ${row.action === 'Write Off' ? 'btn-danger' : row.action === 'Markdown' ? 'btn-secondary' : 'btn-primary'}">${row.action}</button></td>
        </tr>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Expiry Tracking</h1>
                    <p>Monitor batch expiry dates and take action quickly.</p>
                </div>
                <button class="btn btn-secondary btn-sm"><i class="fas fa-file-lines"></i> Expiry Report</button>
            </div>
            <div class="tab-row">${tabs.map((tab, index) => `<button class="page-tab ${index === 0 ? 'active' : ''}">${tab}</button>`).join('')}</div>
            <section class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Batch #</th>
                            <th>Received</th>
                            <th>Expiry Date</th>
                            <th>Days Left</th>
                            <th>Remaining Qty</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            </section>
        </section>
    `;
}

function renderVendors() {
    const cards = SAMPLE.vendors.map((vendor) => `
        <article class="vendor-card">
            <div class="vendor-head">
                <div class="vendor-avatar">${vendor.initials}</div>
                <div>
                    <h3>${vendor.name}</h3>
                    <p>${vendor.category}</p>
                </div>
            </div>
            <ul class="vendor-meta">
                <li><i class="fas fa-user"></i> ${vendor.contact}</li>
                <li><i class="fas fa-phone"></i> ${vendor.phone}</li>
                <li><i class="fas fa-envelope"></i> ${vendor.email}</li>
                <li><i class="fas fa-location-dot"></i> ${vendor.city}</li>
                <li><i class="fas fa-receipt"></i> ${vendor.terms}</li>
            </ul>
            <div class="vendor-footer">
                ${pill(vendor.status, vendor.status === 'Active' ? 'green' : 'red')}
                <div class="action-buttons">
                    <button class="btn btn-secondary btn-sm">Edit</button>
                    <button class="btn btn-primary btn-sm">New PO</button>
                </div>
            </div>
        </article>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Vendors</h1>
                    <p>Manage your supplier network (${SAMPLE.vendors.length} active vendors).</p>
                </div>
                <button class="btn btn-primary btn-sm"><i class="fas fa-plus"></i> Add Vendor</button>
            </div>
            <div class="filters-bar">
                <div class="search-wrapper"><i class="fas fa-search"></i><input class="search-input" placeholder="Search vendors..."></div>
                <select class="filter-select"><option>All Status</option></select>
                <select class="filter-select"><option>All Categories</option></select>
            </div>
            <div class="vendor-grid">${cards}</div>
        </section>
    `;
}

function renderPurchaseOrders() {
    const rows = SAMPLE.purchaseOrders.map((po) => `
        <tr>
            <td class="font-mono">${po.po}</td>
            <td>${po.vendor}</td>
            <td>${po.items} items</td>
            <td><strong>${formatINR(po.total)}</strong></td>
            <td>${po.order}</td>
            <td>${po.expected}</td>
            <td>${statusBadge(po.status)}</td>
            <td class="action-buttons">${po.actions.map((action) => `<button class="btn btn-secondary btn-sm">${action}</button>`).join(' ')}</td>
        </tr>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Purchase Orders</h1>
                    <p>Manage and track all procurement orders.</p>
                </div>
                <div class="toolbar">
                    <button class="btn btn-secondary btn-sm"><i class="fas fa-file-export"></i> Export</button>
                    <a class="btn btn-primary btn-sm" href="create_po.html"><i class="fas fa-plus"></i> New PO</a>
                </div>
            </div>
            <div class="tab-row">
                <button class="page-tab active">All (47)</button>
                <button class="page-tab">Draft (3)</button>
                <button class="page-tab">Pending Approval (2)</button>
                <button class="page-tab">Sent (5)</button>
                <button class="page-tab">Received</button>
            </div>
            <div class="filters-bar">
                <div class="search-wrapper"><i class="fas fa-search"></i><input class="search-input" placeholder="Search by PO#, vendor..."></div>
                <input class="search-input" type="date">
                <input class="search-input" type="date">
                <select class="filter-select"><option>All Vendors</option></select>
            </div>
            <section class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>PO Number</th>
                            <th>Vendor</th>
                            <th>Items</th>
                            <th>Total Amount</th>
                            <th>Order Date</th>
                            <th>Expected</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            </section>
        </section>
    `;
}

function renderCreatePo() {
    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Create Purchase Order</h1>
                    <p>Build a new PO with supplier, item, and delivery details.</p>
                </div>
            </div>
            <div class="split-layout">
                <section class="glass-card">
                    <div class="form-row">
                        <div class="form-group"><label class="form-label">Vendor</label><select class="form-control"><option>Select vendor</option></select></div>
                        <div class="form-group"><label class="form-label">Expected Date</label><input type="date" class="form-control"></div>
                    </div>
                    <div class="form-group"><label class="form-label">Shipping Address</label><textarea class="form-control" rows="3" placeholder="Enter shipping destination"></textarea></div>
                    <div class="item-row"><input class="form-control" placeholder="Product"><input class="form-control" placeholder="Qty"><input class="form-control" placeholder="Price"><input class="form-control" placeholder="Tax %"><button class="btn btn-secondary btn-sm">Remove</button></div>
                    <div class="item-row"><input class="form-control" placeholder="Product"><input class="form-control" placeholder="Qty"><input class="form-control" placeholder="Price"><input class="form-control" placeholder="Tax %"><button class="btn btn-secondary btn-sm">Remove</button></div>
                    <button class="btn btn-secondary btn-sm"><i class="fas fa-plus"></i> Add Line Item</button>
                    <div class="totals-section">
                        <div class="total-row"><span>Subtotal</span><span>${formatINR(0)}</span></div>
                        <div class="total-row"><span>Tax</span><span>${formatINR(0)}</span></div>
                        <div class="total-row grand-total"><span>Total</span><span>${formatINR(0)}</span></div>
                    </div>
                    <div class="mt-3 action-buttons">
                        <button class="btn btn-secondary">Save Draft</button>
                        <button class="btn btn-primary">Submit PO</button>
                    </div>
                </section>
                <aside class="glass-card">
                    <h3>PO Preview</h3>
                    <div class="preview-card">
                        <div class="table-caption">Vendor: Pacific Dairy Ltd.</div>
                        <div class="table-caption">Items: 3</div>
                        <div class="table-caption">Status: Draft</div>
                    </div>
                </aside>
            </div>
        </section>
    `;
}

function renderGoodsReceiving() {
    const deliveries = SAMPLE.receipts.map((item) => `
        <div class="delivery-card">
            <div>
                <strong>${item.po}</strong>
                <div class="text-muted text-sm">${item.vendor}</div>
                <div class="text-muted text-sm">${item.items}</div>
            </div>
            <span class="days-badge warning">${item.eta}</span>
        </div>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Goods Receiving</h1>
                    <p>Record deliveries and update inventory.</p>
                </div>
            </div>
            <div class="two-column-layout">
                <section class="glass-card">
                    <h3>Find Purchase Order</h3>
                    <div class="search-inline">
                        <input class="form-control" placeholder="e.g. PO-2024-0046">
                        <button class="btn btn-primary">Search</button>
                    </div>
                    <div class="receipt-card">
                        <div class="section-title-row"><strong>PO-2024-0046</strong><span class="status-badge sent">Sent</span></div>
                        <table class="compact-table">
                            <thead><tr><th>Product</th><th>Ordered</th><th>Received</th></tr></thead>
                            <tbody>
                                <tr><td>Basmati Rice 25kg</td><td>40 bags</td><td><input class="form-control form-control-sm" value="40"></td></tr>
                                <tr><td>Sunflower Oil 5L</td><td>20 cases</td><td><input class="form-control form-control-sm" value="20"></td></tr>
                                <tr><td>Sea Salt 1kg</td><td>50 bags</td><td><input class="form-control form-control-sm" value="48"></td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="form-group"><label class="form-label">Batch / Lot Number</label><input class="form-control" placeholder="Enter batch number from delivery note"></div>
                    <div class="form-row">
                        <div class="form-group"><label class="form-label">Received Date</label><input type="date" class="form-control" value="2024-12-15"></div>
                        <div class="form-group"><label class="form-label">Expiry Date (if applicable)</label><input type="date" class="form-control"></div>
                    </div>
                    <div class="form-group"><label class="form-label">Warehouse Location</label><select class="form-control"><option>Main Warehouse A</option></select></div>
                    <div class="form-group"><label class="form-label">Notes</label><textarea class="form-control" rows="4" placeholder="Any discrepancies, damages, or special notes..."></textarea></div>
                    <button class="btn btn-success w-100"><i class="fas fa-check"></i> Confirm Receipt & Update Stock</button>
                </section>
                <aside class="glass-card">
                    <h3>Pending Deliveries</h3>
                    <div class="list-stack">${deliveries}</div>
                </aside>
            </div>
        </section>
    `;
}

function renderReports() {
    const cards = SAMPLE.reports.map((report) => `
        <article class="report-card">
            <div class="report-icon"><i class="fas ${report.icon}"></i></div>
            <h3>${report.title}</h3>
            <p>${report.desc}</p>
            <button class="btn btn-secondary btn-sm" data-report="${report.key}">Generate Report</button>
        </article>
    `).join('');

    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Reports</h1>
                    <p>Analytics, insights, and exportable reports for Indian operations.</p>
                </div>
                <div class="toolbar">
                    <button class="btn btn-secondary btn-sm" id="generateAllReports"><i class="fas fa-layer-group"></i> Generate All</button>
                    <button class="btn btn-primary btn-sm" id="downloadReportJson"><i class="fas fa-download"></i> Download JSON</button>
                </div>
            </div>
            <div class="glass-card" id="reportResultCard">
                <div class="table-header compact">
                    <div>
                        <h3>Report Output</h3>
                        <div class="table-caption">Click a report to load live data from the backend.</div>
                    </div>
                </div>
                <div id="reportOutput" class="report-output">No report generated yet.</div>
            </div>
            <div class="report-grid">${cards}</div>
        </section>
    `;
}

function renderAiChat() {
    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>AI Assistant</h1>
                    <p>Ask about stock, purchase orders, expiry risk, and vendor performance.</p>
                </div>
            </div>
            <div class="chat-container">
                <div class="chat-messages" id="chatMessages">
                    <div class="chat-msg ai">I can summarize inventory risk, draft purchase order notes, or spot expiry items.</div>
                    <div class="chat-msg user">Show me items expiring in 7 days.</div>
                    <div class="chat-msg ai">Greek yogurt and milk batches are the highest priority. Consider markdown or transfer to fast-moving stores.</div>
                </div>
                <form class="chat-input-area" id="chatForm">
                    <input class="form-control" id="chatPrompt" placeholder="Ask about stock, PO, expiry risk...">
                    <button class="btn btn-primary" type="submit">Ask AI</button>
                </form>
            </div>
        </section>
    `;
}

function renderSettings() {
    const assistantHidden = isAssistantWidgetHidden();
    return `
        <section class="page-stack">
            <div class="page-header">
                <div>
                    <h1>Settings</h1>
                    <p>Account, notifications, and system preferences.</p>
                </div>
            </div>
            <div class="split-layout">
                <section class="glass-card">
                    <h3>Profile</h3>
                    <div class="form-row">
                        <div class="form-group"><label class="form-label">Name</label><input class="form-control" value="Sarah Chen"></div>
                        <div class="form-group"><label class="form-label">Role</label><input class="form-control" value="Purchasing Manager"></div>
                    </div>
                    <div class="form-group"><label class="form-label">Email</label><input class="form-control" value="sarah.chen@groceryerp.local"></div>
                    <button class="btn btn-primary">Save Changes</button>
                </section>
                <section class="glass-card">
                    <h3>Preferences</h3>
                    <div class="list-stack">
                        <div class="list-row"><span>Dark mode</span><button class="btn btn-secondary btn-sm" onclick="toggleTheme()">Toggle</button></div>
                        <div class="list-row"><span>Alert notifications</span>${pill('Enabled', 'green')}</div>
                        <div class="list-row"><span>Auto PO suggestions</span>${pill('Enabled', 'green')}</div>
                        <div class="list-row"><span>API Bridge</span><button class="btn btn-secondary btn-sm" id="toggleAssistantWidgetBtn">${assistantHidden ? 'Show' : 'Hide'}</button></div>
                    </div>
                </section>
            </div>
        </section>
    `;
}

function renderAuthPage(route) {
    const isRegister = route === 'register';
    return `
        <section class="auth-shell">
            <div class="auth-hero">
                <div class="brand-mark"><i class="fas fa-cube"></i></div>
                <h1>GroceryERP</h1>
                <p>Wholesale inventory, procurement, and expiry control built for busy operations teams.</p>
                <div class="auth-feature-list">
                    <div><i class="fas fa-circle-check"></i> Live stock and expiry monitoring</div>
                    <div><i class="fas fa-circle-check"></i> Vendor, PO, and receiving workflow</div>
                    <div><i class="fas fa-circle-check"></i> Analytics and AI assistant</div>
                </div>
            </div>
            <div class="auth-card glass-card">
                <div class="auth-card-head">
                    <h2>${isRegister ? 'Create your account' : 'Welcome back'}</h2>
                    <p>${isRegister ? 'Register to access the ERP workspace.' : 'Sign in to continue to your dashboard.'}</p>
                </div>
                <form id="authForm" class="auth-form">
                    ${isRegister ? '<div class="form-group"><label class="form-label">Full Name</label><input class="form-control" id="authName" autocomplete="name" placeholder="Sarah Chen" required></div>' : ''}
                    <div class="form-group"><label class="form-label">Email</label><input class="form-control" id="authEmail" type="email" autocomplete="email" autocapitalize="none" spellcheck="false" placeholder="you@example.com" required></div>
                    <div class="form-group"><label class="form-label">Password</label><input class="form-control" id="authPassword" type="password" autocomplete="${isRegister ? 'new-password' : 'current-password'}" placeholder="••••••••" required></div>
                    ${isRegister ? '<div class="form-group"><label class="form-label">Role</label><select class="form-control" id="authRole"><option value="staff">Staff</option><option value="manager">Manager</option><option value="admin">Admin</option></select></div>' : ''}
                    <button class="btn btn-primary w-100" type="submit">${isRegister ? 'Register' : 'Login'}</button>
                </form>
                <div class="auth-switch">
                    ${isRegister ? 'Already have an account? <a href="login.html">Login</a>' : 'Need an account? <a href="register.html">Register</a>'}
                </div>
            </div>
        </section>
    `;
}

function renderPage(route) {
    const pageContent = document.getElementById('pageContent');
    if (!pageContent) return;

    const rendererMap = {
        dashboard: renderDashboard,
        alerts: renderAlerts,
        products: renderProducts,
        stock: renderStock,
        expiry_tracking: renderExpiryTracking,
        vendors: renderVendors,
        purchase_orders: renderPurchaseOrders,
        create_po: renderCreatePo,
        goods_receiving: renderGoodsReceiving,
        reports: renderReports,
        ai_chat: renderAiChat,
        settings: renderSettings,
        login: () => renderAuthPage('login'),
        register: () => renderAuthPage('register'),
    };

    pageContent.innerHTML = (rendererMap[route] || renderDashboard)();
    highlightActiveNav(route);
    bindPageActions(route);
}

function bindPageActions(route) {
    if (route === 'ai_chat') {
        const form = document.getElementById('chatForm');
        const prompt = document.getElementById('chatPrompt');
        if (form) {
            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                const value = prompt.value.trim();
                if (!value) return;
                const messages = document.getElementById('chatMessages');
                messages.insertAdjacentHTML('beforeend', `<div class="chat-msg user">${value}</div>`);
                prompt.value = '';

                try {
                    const result = await apiPost('/ai/chat', { prompt: value });
                    messages.insertAdjacentHTML('beforeend', `<div class="chat-msg ai">${result.response}</div>`);
                } catch (error) {
                    messages.insertAdjacentHTML('beforeend', `<div class="chat-msg ai">${error.message || 'AI request failed.'}</div>`);
                }
            });
        }
    }

    if (route === 'login' || route === 'register') {
        const form = document.getElementById('authForm');
        if (!form) return;

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('authEmail').value.trim().toLowerCase();
            const password = document.getElementById('authPassword').value;

            try {
                if (route === 'register') {
                    const name = document.getElementById('authName').value.trim();
                    const role = document.getElementById('authRole').value;
                    await apiPost('/auth/register', { name, email, password, role });
                }

                const login = await apiPost('/auth/login', { email, password });
                setToken(login.access_token);
                const me = await apiGet('/auth/me');
                setUser(me);
                window.location.href = 'index.html';
            } catch (error) {
                showToast(error.message || 'Authentication failed', 'error');
            }
        });
    }

    if (route === 'reports') {
        const reportButtons = document.querySelectorAll('[data-report]');
        reportButtons.forEach((button) => {
            button.addEventListener('click', () => loadReport(button.dataset.report));
        });

        const generateAllReports = document.getElementById('generateAllReports');
        if (generateAllReports) {
            generateAllReports.addEventListener('click', async () => {
                for (const key of Object.keys(REPORT_ENDPOINTS)) {
                    // Load the first available report into the preview, then continue generating the rest.
                    await loadReport(key);
                }
            });
        }

        const downloadReportJsonButton = document.getElementById('downloadReportJson');
        if (downloadReportJsonButton) {
            downloadReportJsonButton.addEventListener('click', () => {
                if (!window.__lastReportData) {
                    showToast('Generate a report first', 'warning');
                    return;
                }
                downloadReportJson(window.__lastReportData.reportKey, window.__lastReportData.data);
            });
        }

        const initialReport = document.querySelector('[data-report]');
        if (initialReport) {
            loadReport(initialReport.dataset.report);
        }
    }

    if (route === 'settings') {
        const toggleAssistantWidgetBtn = document.getElementById('toggleAssistantWidgetBtn');
        if (toggleAssistantWidgetBtn) {
            toggleAssistantWidgetBtn.addEventListener('click', toggleAssistantWidgetHidden);
        }
    }
}

async function startApp() {
    const route = normalizeRoute();
    initTheme();

    if (route === 'login' || route === 'register') {
        document.body.classList.add('auth-mode');
        const pageContent = document.getElementById('pageContent');
        if (pageContent) pageContent.innerHTML = renderAuthPage(route);
        bindPageActions(route);
        setPageTitle(route);
        return;
    }

    if (!requireAuth()) return;

    await Promise.all([
        loadComponent('sidebar-container', 'components/sidebar.html'),
        loadComponent('navbar-container', 'components/navbar.html'),
    ]);

    const user = getUser();
    if (user && user.name) {
        const initials = user.name.split(' ').map((part) => part[0]).join('').toUpperCase();
        const userInitials = document.getElementById('userInitials');
        if (userInitials) userInitials.textContent = initials;
    }

    setPageTitle(route);
    renderPage(route);
    mountAssistantWidget(route);
    setTimeout(() => {
        const alertBadge = document.getElementById('alertBadge');
        if (alertBadge) alertBadge.textContent = '7';
    }, 50);
}

function renderAssistantWidget() {
    return `
        <aside class="assistant-widget glass-card" id="assistantWidget">
            <div class="assistant-head">
                <div>
                    <div class="assistant-title">API Bridge</div>
                    <div class="assistant-subtitle">Quick auth and AI access</div>
                </div>
                <button class="assistant-close-btn" type="button" onclick="toggleAssistantWidgetHidden()" title="Hide API Bridge"><i class="fas fa-xmark"></i></button>
            </div>
            <form class="assistant-form" id="assistantLoginForm">
                <input class="form-control form-control-sm" id="assistantEmail" type="email" placeholder="Email">
                <input class="form-control form-control-sm" id="assistantPassword" type="password" placeholder="Password">
                <div class="assistant-actions">
                    <a class="btn btn-secondary btn-sm" href="register.html">Register</a>
                    <button class="btn btn-primary btn-sm" type="submit">Login</button>
                </div>
            </form>
            <textarea class="form-control assistant-prompt" id="assistantPrompt" rows="4" placeholder="Ask AI about stock, PO, expiry risk..."></textarea>
            <button class="btn btn-success btn-sm w-100" id="assistantAskBtn" type="button">Ask AI</button>
            <button class="btn btn-secondary btn-sm w-100" type="button" onclick="window.location.href='products.html'">Load Products</button>
        </aside>
    `;
}

function mountAssistantWidget(route) {
    if (route === 'login' || route === 'register') return;
    if (isAssistantWidgetHidden()) {
        const existing = document.getElementById('assistantWidgetHost');
        if (existing) existing.remove();
        return;
    }
    let host = document.getElementById('assistantWidgetHost');
    if (!host) {
        host = document.createElement('div');
        host.id = 'assistantWidgetHost';
        document.body.appendChild(host);
    }
    host.innerHTML = renderAssistantWidget();

    const loginForm = document.getElementById('assistantLoginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('assistantEmail').value.trim();
            const password = document.getElementById('assistantPassword').value;
            if (!email || !password) return;

            try {
                const login = await apiPost('/auth/login', { email, password });
                setToken(login.access_token);
                const me = await apiGet('/auth/me');
                setUser(me);
                showToast('Logged in successfully', 'success');
                window.location.reload();
            } catch (error) {
                showToast(error.message || 'Login failed', 'error');
            }
        });
    }

    const askBtn = document.getElementById('assistantAskBtn');
    if (askBtn) {
        askBtn.addEventListener('click', async () => {
            const prompt = document.getElementById('assistantPrompt').value.trim();
            if (!prompt) return;
            try {
                const result = await apiPost('/ai/chat', { prompt });
                showToast(result.response || 'AI response ready', 'success');
            } catch (error) {
                showToast(error.message || 'AI request failed', 'error');
            }
        });
    }

}

async function initApp(pageTitle = 'Dashboard') {
    setPageTitle(normalizeRoute());
    await startApp(pageTitle);
}

window.addEventListener('DOMContentLoaded', startApp);
