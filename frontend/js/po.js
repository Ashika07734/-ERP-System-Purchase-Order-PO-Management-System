/**
 * ERP PO Management System — Purchase Order Logic
 * Dynamic row management, live total calculation, form submission.
 */

let itemRowIndex = 0;
let productsCache = [];

// ── Load Products ──────────────────────────────────────

async function loadProducts() {
    try {
        productsCache = await apiGet('/api/products');
    } catch (e) {
        showToast('Failed to load products', 'error');
    }
}

// ── Load Vendors into Dropdown ─────────────────────────

async function loadVendors() {
    try {
        const vendors = await apiGet('/api/vendors');
        const select = document.getElementById('vendorSelect');
        if (!select) return;

        select.innerHTML = '<option value="">— Select Vendor —</option>';
        vendors.forEach(v => {
            const opt = document.createElement('option');
            opt.value = v.vendor_id;
            opt.textContent = `${v.name} (★ ${v.rating})`;
            select.appendChild(opt);
        });
    } catch (e) {
        showToast('Failed to load vendors', 'error');
    }
}

// ── Dynamic Row Management ─────────────────────────────

function buildProductOptions() {
    let html = '<option value="">— Select Product —</option>';
    productsCache.forEach(p => {
        html += `<option value="${p.product_id}" data-price="${p.unit_price}">${p.name} (${p.sku})</option>`;
    });
    return html;
}

function addItemRow() {
    itemRowIndex++;
    const container = document.getElementById('itemsContainer');
    if (!container) return;

    const row = document.createElement('div');
    row.className = 'item-row';
    row.id = `item-row-${itemRowIndex}`;
    row.innerHTML = `
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Product</label>
            <select class="form-control product-select" onchange="onProductChange(this, ${itemRowIndex})" required>
                ${buildProductOptions()}
            </select>
        </div>
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Quantity</label>
            <input type="number" class="form-control item-qty" min="1" value="1"
                   oninput="updateRowTotal(${itemRowIndex})" required>
        </div>
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Unit Price ($)</label>
            <input type="number" class="form-control item-price" step="0.01" min="0" value="0.00"
                   oninput="updateRowTotal(${itemRowIndex})" required>
        </div>
        <button type="button" class="btn-icon" onclick="removeItemRow(${itemRowIndex})" title="Remove row"
                style="align-self:end; margin-bottom:4px;">
            <i class="fas fa-trash-alt"></i>
        </button>
    `;

    container.appendChild(row);
    recalcTotals();
}

function removeItemRow(index) {
    const row = document.getElementById(`item-row-${index}`);
    if (row) {
        row.style.animation = 'fadeInUp 0.3s ease reverse';
        setTimeout(() => { row.remove(); recalcTotals(); }, 300);
    }
}

function onProductChange(select, index) {
    const option = select.options[select.selectedIndex];
    const price = option.getAttribute('data-price') || '0.00';
    const row = document.getElementById(`item-row-${index}`);
    if (row) {
        row.querySelector('.item-price').value = parseFloat(price).toFixed(2);
        updateRowTotal(index);
    }
}

function updateRowTotal(index) {
    recalcTotals();
}

// ── Live Total Calculation ─────────────────────────────

function recalcTotals() {
    let subtotal = 0;
    document.querySelectorAll('.item-row').forEach(row => {
        const qty   = parseFloat(row.querySelector('.item-qty')?.value) || 0;
        const price = parseFloat(row.querySelector('.item-price')?.value) || 0;
        subtotal += qty * price;
    });

    const tax = subtotal * 0.05;
    const total = subtotal + tax;

    const subEl = document.getElementById('subtotalDisplay');
    const taxEl = document.getElementById('taxDisplay');
    const totEl = document.getElementById('totalDisplay');

    if (subEl) subEl.textContent = formatCurrency(subtotal);
    if (taxEl) taxEl.textContent = formatCurrency(tax);
    if (totEl) totEl.textContent = formatCurrency(total);
}

// ── Form Submission ────────────────────────────────────

async function submitPurchaseOrder(event) {
    event.preventDefault();

    const vendorId = document.getElementById('vendorSelect')?.value;
    const notes    = document.getElementById('poNotes')?.value || '';

    if (!vendorId) {
        showToast('Please select a vendor', 'warning');
        return;
    }

    // Collect items
    const items = [];
    const rows = document.querySelectorAll('.item-row');

    if (rows.length === 0) {
        showToast('Please add at least one product', 'warning');
        return;
    }

    let valid = true;
    rows.forEach(row => {
        const productId = row.querySelector('.product-select')?.value;
        const qty       = parseInt(row.querySelector('.item-qty')?.value) || 0;
        const price     = parseFloat(row.querySelector('.item-price')?.value) || 0;

        if (!productId || qty <= 0 || price <= 0) {
            valid = false;
            return;
        }

        items.push({
            product_id: parseInt(productId),
            quantity: qty,
            unit_price: price,
        });
    });

    if (!valid) {
        showToast('Please fill in all product fields correctly', 'warning');
        return;
    }

    try {
        showSpinner();
        const result = await apiPost('/api/purchase-orders', {
            vendor_id: parseInt(vendorId),
            notes: notes,
            items: items,
        });

        showToast(`Purchase Order ${result.reference_no} created!`, 'success');
        setTimeout(() => {
            window.location.href = '/static/index.html';
        }, 1200);
    } catch (error) {
        showToast('Failed to create PO: ' + error.message, 'error');
    } finally {
        hideSpinner();
    }
}

// ── PO Listing ─────────────────────────────────────────

let currentPage = 0;
const PAGE_SIZE = 10;

async function loadPurchaseOrders(page = 0, status = '', search = '') {
    try {
        const skip = page * PAGE_SIZE;
        let url = `/api/purchase-orders?skip=${skip}&limit=${PAGE_SIZE}`;
        if (status) url += `&status=${status}`;
        if (search) url += `&search=${encodeURIComponent(search)}`;

        const orders = await apiGet(url);
        renderPOTable(orders);
        currentPage = page;
    } catch (e) {
        showToast('Failed to load purchase orders', 'error');
    }
}

function renderPOTable(orders) {
    const tbody = document.getElementById('poTableBody');
    if (!tbody) return;

    if (!orders || orders.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6">
                    <div class="empty-state">
                        <i class="fas fa-inbox"></i>
                        <h4>No purchase orders found</h4>
                        <p>Create your first purchase order to get started.</p>
                    </div>
                </td>
            </tr>`;
        return;
    }

    tbody.innerHTML = orders.map(po => `
        <tr onclick="window.location.href='/static/index.html?po=${po.po_id}'" style="cursor:pointer">
            <td><span class="font-mono" style="font-weight:600; color:var(--primary)">${po.reference_no}</span></td>
            <td>${po.vendor ? po.vendor.name : '—'}</td>
            <td style="font-weight:600">${formatCurrency(po.total_amount)}</td>
            <td>${statusBadge(po.status)}</td>
            <td>${formatDate(po.created_at)}</td>
            <td>
                <div style="display:flex; gap:6px;">
                    <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); updateStatus(${po.po_id}, 'Approved')" title="Approve">
                        <i class="fas fa-check"></i>
                    </button>
                    <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); updateStatus(${po.po_id}, 'Rejected')" title="Reject" style="border-color:var(--danger); color:var(--danger);">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

async function updateStatus(poId, status) {
    try {
        await apiPut(`/api/purchase-orders/${poId}/status`, { status });
        showToast(`PO status updated to ${status}`, 'success');
        loadPurchaseOrders(currentPage);
    } catch (e) {
        showToast('Failed to update status: ' + e.message, 'error');
    }
}

// ── Dashboard Stats ────────────────────────────────────

async function loadDashboardStats() {
    try {
        const stats = await apiGet('/api/purchase-orders/stats');
        const setVal = (id, val) => {
            const el = document.getElementById(id);
            if (el) el.textContent = val;
        };

        setVal('statTotal', stats.total_pos);
        setVal('statPending', stats.pending_pos);
        setVal('statApproved', stats.approved_pos);
        setVal('statRejected', stats.rejected_pos);
        setVal('statTotalValue', formatCurrency(stats.total_value));
        setVal('statVendors', stats.total_vendors);
        setVal('statProducts', stats.total_products);
    } catch (e) {
        showToast('Failed to load dashboard stats', 'error');
    }
}

async function loadRecentOrders() {
    try {
        const orders = await apiGet('/api/purchase-orders?limit=5');
        const tbody = document.getElementById('recentOrdersBody');
        if (!tbody) return;

        if (!orders || orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No orders yet</td></tr>';
            return;
        }

        tbody.innerHTML = orders.map(po => `
            <tr>
                <td><span class="font-mono" style="font-weight:600; color:var(--primary)">${po.reference_no}</span></td>
                <td>${po.vendor ? po.vendor.name : '—'}</td>
                <td style="font-weight:600">${formatCurrency(po.total_amount)}</td>
                <td>${statusBadge(po.status)}</td>
                <td>${formatDate(po.created_at)}</td>
            </tr>
        `).join('');
    } catch (e) {
        console.error('Recent orders load failed', e);
    }
}

// ── AI Description ─────────────────────────────────────

async function generateAIDescription(productName, category) {
    try {
        const result = await apiPost('/api/products/ai-description', {
            product_name: productName,
            category: category || 'General',
        });
        return result.description;
    } catch (e) {
        showToast('AI generation failed', 'error');
        return null;
    }
}
