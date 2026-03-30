/**
 * ERP PO Management System — Core Application Logic
 * Auth management, API helpers, dark mode, sidebar, toasts, component loader.
 */

// ── Configuration ───────────────────────────────────────
const API_BASE = window.location.origin;
const TOKEN_KEY = 'erp_token';
const USER_KEY  = 'erp_user';
const THEME_KEY = 'erp_theme';

// ── Auth Helpers ────────────────────────────────────────

function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

function getUser() {
    const u = localStorage.getItem(USER_KEY);
    return u ? JSON.parse(u) : null;
}

function setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function isAuthenticated() {
    return !!getToken();
}

function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.location.href = '/static/login.html';
}

function requireAuth() {
    // Check for token in URL (OAuth callback)
    const params = new URLSearchParams(window.location.search);
    const urlToken = params.get('token');
    if (urlToken) {
        setToken(urlToken);
        // Clean URL
        window.history.replaceState({}, '', window.location.pathname);
    }

    if (!isAuthenticated()) {
        window.location.href = '/static/login.html';
        return false;
    }
    return true;
}

// ── API Helpers ─────────────────────────────────────────

async function api(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
    };

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            logout();
            return null;
        }

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || `API Error ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

async function apiGet(endpoint)          { return api(endpoint); }
async function apiPost(endpoint, data)   { return api(endpoint, { method: 'POST', body: JSON.stringify(data) }); }
async function apiPut(endpoint, data)    { return api(endpoint, { method: 'PUT', body: JSON.stringify(data) }); }
async function apiDelete(endpoint)       { return api(endpoint, { method: 'DELETE' }); }

// ── Dev Login ──────────────────────────────────────────

async function devLogin() {
    try {
        showSpinner();
        const data = await api('/auth/dev-login', { method: 'POST' });
        if (data && data.access_token) {
            setToken(data.access_token);
            setUser(data.user);
            showToast('Welcome back, ' + data.user.full_name + '!', 'success');
            setTimeout(() => {
                window.location.href = '/static/dashboard.html';
            }, 600);
        }
    } catch (error) {
        showToast('Login failed: ' + error.message, 'error');
    } finally {
        hideSpinner();
    }
}

// ── Theme Management ────────────────────────────────────

function getTheme() {
    return localStorage.getItem(THEME_KEY) || 'light';
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

function toggleTheme() {
    const current = getTheme();
    setTheme(current === 'dark' ? 'light' : 'dark');
}

function initTheme() {
    setTheme(getTheme());
}

// ── Sidebar ─────────────────────────────────────────────

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const main = document.querySelector('.main-content');
    const navbar = document.getElementById('navbar');

    sidebar.classList.toggle('collapsed');
    if (main) main.classList.toggle('sidebar-collapsed');
    if (navbar) navbar.classList.toggle('sidebar-collapsed');

    // Mobile
    if (window.innerWidth <= 768) {
        sidebar.classList.toggle('mobile-open');
    }
}

function highlightActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href && path.includes(href.replace('/static/', ''))) {
            link.classList.add('active');
        }
    });
}

// ── Toast Notifications ─────────────────────────────────

function showToast(message, type = 'info', duration = 4000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle',
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info} toast-icon"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// ── Loading Spinner ─────────────────────────────────────

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

// ── Component Loader ────────────────────────────────────

async function loadComponent(id, url) {
    try {
        const resp = await fetch(url);
        if (resp.ok) {
            const html = await resp.text();
            const el = document.getElementById(id);
            if (el) el.innerHTML = html;
        }
    } catch (e) {
        console.warn('Component load failed:', url, e);
    }
}

async function initApp(pageTitle = 'Dashboard') {
    // Load sidebar and navbar components
    await Promise.all([
        loadComponent('sidebar-container', '/static/components/sidebar.html'),
        loadComponent('navbar-container', '/static/components/navbar.html'),
    ]);

    // Set page title
    setTimeout(() => {
        const titleEl = document.getElementById('pageTitle');
        if (titleEl) titleEl.textContent = pageTitle;
    }, 50);

    // Init theme
    initTheme();

    // Highlight active nav
    setTimeout(highlightActiveNav, 100);

    // Set user avatar
    const user = getUser();
    if (user) {
        setTimeout(() => {
            const initialsEl = document.getElementById('userInitials');
            if (initialsEl && user.full_name) {
                initialsEl.textContent = user.full_name.split(' ').map(n => n[0]).join('').toUpperCase();
            }
        }, 100);
    }
}

// ── Formatters ──────────────────────────────────────────

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
    });
}

function statusBadge(status) {
    const cls = status.toLowerCase();
    return `<span class="status-badge ${cls}">${status}</span>`;
}
