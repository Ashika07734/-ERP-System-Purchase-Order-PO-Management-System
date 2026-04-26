/**
 * ERP PO Management System — Purchase Order Logic
 * Dynamic row management, live total calculation, form submission.
 */

let itemRowIndex = 0;
let productsCache = [];

const FMCG_CATEGORIES = [
    'Rice',
    'Flour',
    'Oil',
    'Snacks',
    'Beverages',
    'Dairy',
    'Spices',
    'Frozen Foods',
    'Cleaning Products',
];

const UNIT_TYPES = [
    'Kg',
    'Gram',
    'Liter',
    'Packet',
    'Box',
    'Carton',
    'Bottle',
    'Bag',
];

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
        html += `<option
            value="${p.product_id}"
            data-price="${p.unit_price}"
            data-category="${p.category || ''}"
            data-brand="${p.brand || ''}"
            data-unit="${p.unit_type || ''}"
            data-expiry="${p.expiry_date || ''}"
            data-batch="${p.batch_number || ''}"
            data-min-stock="${p.minimum_stock || 10}"
            data-gst="${p.gst_rate || 5}"
        >${p.name} (${p.sku})</option>`;
    });
    return html;
}

function buildSelectOptions(options, selected = '') {
    let html = '<option value="">— Select —</option>';
    options.forEach(opt => {
        const isSelected = selected && selected === opt ? 'selected' : '';
        html += `<option value="${opt}" ${isSelected}>${opt}</option>`;
    });
    return html;
}

function buildGstOptions(selected = '5') {
    const gstOptions = ['5', '12', '18'];
    let html = '';
    gstOptions.forEach(opt => {
        const isSelected = `${selected}` === opt ? 'selected' : '';
        html += `<option value="${opt}" ${isSelected}>${opt}%</option>`;
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
            <label class="form-label">Category</label>
            <select class="form-control item-category">
                ${buildSelectOptions(FMCG_CATEGORIES)}
            </select>
        </div>
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Brand</label>
            <input type="text" class="form-control item-brand" placeholder="Brand name">
        </div>
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Unit Type</label>
            <select class="form-control item-unit-type">
                ${buildSelectOptions(UNIT_TYPES)}
            </select>
        </div>
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Expiry Date</label>
            <input type="date" class="form-control item-expiry-date">
        </div>
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Batch No.</label>
            <input type="text" class="form-control item-batch-number" placeholder="Batch number">
        </div>
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">Minimum Stock</label>
            <input type="number" class="form-control item-min-stock" min="0" value="10">
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
        <div class="form-group" style="margin-bottom:0">
            <label class="form-label">GST</label>
            <select class="form-control item-gst" onchange="updateRowTotal(${itemRowIndex})">
                ${buildGstOptions()}
            </select>
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
        row.querySelector('.item-brand').value = option.getAttribute('data-brand') || '';
        row.querySelector('.item-expiry-date').value = option.getAttribute('data-expiry') || '';
        row.querySelector('.item-batch-number').value = option.getAttribute('data-batch') || '';
        row.querySelector('.item-min-stock').value = option.getAttribute('data-min-stock') || 10;

        const categoryValue = option.getAttribute('data-category') || '';
        const categorySelect = row.querySelector('.item-category');
        if (categorySelect) categorySelect.value = categoryValue;

        const unitValue = option.getAttribute('data-unit') || '';
        const unitSelect = row.querySelector('.item-unit-type');
        if (unitSelect) unitSelect.value = unitValue;

        const gstValue = option.getAttribute('data-gst') || '5';
        const gstSelect = row.querySelector('.item-gst');
        if (gstSelect) gstSelect.value = `${parseInt(gstValue, 10) || 5}`;

        updateRowTotal(index);
    }
}

function updateRowTotal(index) {
    recalcTotals();
}

// ── Live Total Calculation ─────────────────────────────

function recalcTotals() {
    let subtotal = 0;
    let gstTotal = 0;
    document.querySelectorAll('.item-row').forEach(row => {
        const qty   = parseFloat(row.querySelector('.item-qty')?.value) || 0;
        const price = parseFloat(row.querySelector('.item-price')?.value) || 0;
        const gstRate = parseFloat(row.querySelector('.item-gst')?.value) || 0;
        const line = qty * price;
        subtotal += line;
        gstTotal += (line * gstRate) / 100;
    });

    const total = subtotal + gstTotal;

    const subEl = document.getElementById('subtotalDisplay');
    const taxEl = document.getElementById('taxDisplay');
    const totEl = document.getElementById('totalDisplay');

    if (subEl) subEl.textContent = formatCurrency(subtotal);
    if (taxEl) taxEl.textContent = formatCurrency(gstTotal);
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
            gst_rate: parseFloat(row.querySelector('.item-gst')?.value) || 5,
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
                    <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); updateStatus(${po.po_id}, 'Received')" title="Mark Received" style="border-color:var(--success); color:var(--success);">
                        <i class="fas fa-truck"></i>
                    </button>
                    <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); printPurchaseOrder(${po.po_id}, '${po.reference_no}')" title="Print PDF">
                        <i class="fas fa-print"></i>
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

async function printPurchaseOrder(poId, referenceNo) {
    const token = getToken();
    if (!token) {
        showToast('Authentication required', 'error');
        return;
    }

    try {
        showSpinner();
        const response = await fetch(`/api/purchase-orders/${poId}/print`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to print PO (${response.status})`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${referenceNo || `PO-${poId}`}.pdf`;
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        showToast(`Print failed: ${e.message}`, 'error');
    } finally {
        hideSpinner();
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
        renderLowStockAlerts(stats.low_stock_products || []);
    } catch (e) {
        showToast('Failed to load dashboard stats', 'error');
    }
}

function renderLowStockAlerts(products) {
    const body = document.getElementById('lowStockBody');
    const count = document.getElementById('lowStockCount');

    if (count) count.textContent = products.length;
    if (!body) return;

    if (!products.length) {
        body.innerHTML = '<tr><td colspan="5" class="text-center">No low stock alerts</td></tr>';
        return;
    }

    body.innerHTML = products.map(p => `
        <tr style="background: rgba(239, 68, 68, 0.08);">
            <td style="font-weight:600">${p.name}</td>
            <td>${p.category || '—'}</td>
            <td>${p.brand || '—'}</td>
            <td style="color: var(--danger); font-weight:700;">${p.stock_level}</td>
            <td>${p.minimum_stock ?? 0}</td>
        </tr>
    `).join('');
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


// ── Product Catalog Filters (Category / Brand / Expiry) ──

function buildProductFilterQuery() {
    const category = document.getElementById('filterCategory')?.value || '';
    const brand = document.getElementById('filterBrand')?.value || '';
    const expiryBefore = document.getElementById('filterExpiry')?.value || '';
    const search = document.getElementById('productSearch')?.value || '';

    const params = new URLSearchParams();
    if (category) params.set('category', category);
    if (brand) params.set('brand', brand);
    if (expiryBefore) params.set('expiry_before', expiryBefore);
    if (search) params.set('search', search);

    return params.toString();
}

async function loadProductCatalogWithFilters() {
    const tbody = document.getElementById('productTableBody');
    if (!tbody) return;

    try {
        const query = buildProductFilterQuery();
        const endpoint = query ? `/api/products?${query}` : '/api/products';
        const products = await apiGet(endpoint);

        if (!products.length) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No products found</td></tr>';
            return;
        }

        tbody.innerHTML = products.map(p => `
            <tr>
                <td><span class="font-mono text-sm">${p.sku}</span></td>
                <td style="font-weight:600">${p.name}</td>
                <td>${p.category || '—'}</td>
                <td>${p.brand || '—'}</td>
                <td>${p.unit_type || '—'}</td>
                <td>${p.expiry_date || '—'}</td>
                <td>${p.batch_number || '—'}</td>
                <td>${formatCurrency(p.unit_price)}</td>
                <td>${p.stock_level ?? 0}</td>
            </tr>
        `).join('');
    } catch (e) {
        showToast('Failed to load products', 'error');
    }
}
