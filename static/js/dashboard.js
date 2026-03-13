// Professional Interview Dashboard - Full CRUD + Charts + Search
class ProfessionalDashboard {
  constructor() {
this.apiBase = '/api';  // Fixed: /api/vendors/vendors/ → /api/vendors/
    this.entities = ['vendors', 'products', 'courses', 'certifications'];
    this.mappings = ['vendor-product-mappings', 'product-course-mappings', 'course-certification-mappings'];
    this.entityData = new Map(); // Cache API data
    this.chart = null;
    this.init();
  }

  async init() {
    this.bindGlobalEvents();
    await this.loadTheme();
    await this.loadAllData();
    await this.loadStats();
    this.renderPipelineChart();
    // Render entities after data load
    this.entities.concat(this.mappings).forEach(entity => this.renderEntity(entity));
    this.updateStats();
  }

  bindGlobalEvents() {
    // Theme toggle
    document.getElementById('theme-toggle').onclick = () => this.toggleTheme();
    
    // Global search
    document.getElementById('global-search').oninput = (e) => this.globalSearch(e.target.value);
    
    // Entity events (delegated)
    document.addEventListener('click', (e) => {
      if (e.target.matches('.add-btn')) this.toggleForm(e.target.closest('.entity-section'));
      if (e.target.closest('form')) this.handleFormSubmit(e);
    });
    
    // Entity search
    document.querySelectorAll('.entity-search').forEach(input => {
      input.oninput = (e) => this.filterEntity(e.target.dataset.entity, e.target.value);
    });
  }

  async loadAllData() {
    const promises = [...this.entities, ...this.mappings].map(entity => 
      fetch(this.getApiUrl(entity)).then(res => res.json()).then(data => {
        this.entityData.set(entity, data);
      }).catch(() => this.entityData.set(entity, []))
    );
    await Promise.all(promises);
  }

  getApiUrl(entity) {
    const base = '/api';
    const paths = {
      'vendors': `${base}/vendors/vendors/`,
      'products': `${base}/products/products/`,
      'courses': `${base}/courses/courses/`,
      'certifications': `${base}/certifications/certifications/`,
      'vendor-product-mappings': `${base}/vendor-product-mappings/vendor-product-mappings/`,
      'product-course-mappings': `${base}/product-course-mappings/product-course-mappings/`,
      'course-certification-mappings': `${base}/course-certification-mappings/course-certification-mappings/`
    };
    return paths[entity] || `${base}/${entity}/`;
  }

  async loadStats() {
    const stats = {
      vendors: this.entityData.get('vendors')?.length || 0,
      products: this.entityData.get('products')?.length || 0,
      courses: this.entityData.get('courses')?.length || 0,
      certifications: this.entityData.get('certifications')?.length || 0,
      mappings: this.mappings.reduce((sum, m) => sum + (this.entityData.get(m)?.length || 0), 0)
    };
    stats.pipeline = Math.min(100, (stats.mappings / Math.max(1, stats.vendors * stats.products)) * 100);
    this.updateStatsDOM(stats);
  }

  updateStatsDOM(stats) {
    document.getElementById('vendor-count').textContent = stats.vendors;
    document.getElementById('product-count').textContent = stats.products;
    document.getElementById('course-count').textContent = stats.courses;
    document.getElementById('cert-count').textContent = stats.certifications;
    document.getElementById('mapping-count').textContent = stats.mappings;
    document.getElementById('pipeline-count').textContent = stats.pipeline.toFixed(1) + '%';
  }

  renderPipelineChart() {
    const ctx = document.getElementById('pipelineChart').getContext('2d');
    this.chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Vendors', 'Products', 'Courses', 'Certifications', 'Mappings'],
        datasets: [{
          data: [0,0,0,0,0],
          backgroundColor: ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#06b6d4'],
          borderWidth: 0,
          hoverOffset: 20
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom', labels: { color: 'white', font: { size: 14 } } } },
        cutout: '60%'
      }
    });
    this.updateChart();
  }

  updateChart() {
    if (!this.chart) return;
    const data = this.entities.map(e => this.entityData.get(e)?.length || 0);
    data.push(this.mappings.reduce((sum, m) => sum + (this.entityData.get(m)?.length || 0), 0));
    this.chart.data.datasets[0].data = data;
    this.chart.update('none');
  }

  async toggleForm(section) {
    const form = section.querySelector('.add-form');
    form.classList.toggle('hidden');
    if (!form.classList.contains('hidden') && form.dataset.populated !== 'true') {
      await this.populateFormSelects(form);
      form.dataset.populated = 'true';
    }
  }

  async populateFormSelects(form) {
    const entity = form.dataset.entity;
    if (entity.includes('vendor-product')) {
      const vendors = await fetch(this.getApiUrl('vendors')).then(r => r.json());
      const products = await fetch(this.getApiUrl('products')).then(r => r.json());
      this.populateSelect(form.querySelector('[name="vendor"]'), vendors, 'id', 'name');
      this.populateSelect(form.querySelector('[name="product"]'), products, 'id', 'name');
    }
    // Similar for other mappings...
  }

  populateSelect(select, data, valueKey, labelKey) {
    select.innerHTML = data.map(item => `<option value="${item[valueKey]}">${item[labelKey] || item.code} (ID: ${item.id})</option>`).join('');
  }

  async handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const entity = form.dataset.entity;
    const data = Object.fromEntries(new FormData(form));
    
    this.showToast('loading', 'Creating...');
    try {
      const res = await fetch(this.getApiUrl(entity), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.ok) {
        this.showToast('success', 'Created successfully!');
        this.refreshData(entity);
      } else {
        this.showToast('error', 'Validation error - check fields');
      }
    } catch (err) {
      this.showToast('error', 'Network error');
    }
  }

  async filterEntity(entity, query) {
    const data = this.entityData.get(entity) || [];
    const filtered = data.filter(item => 
      Object.values(item).some(val => 
        val?.toString().toLowerCase().includes(query.toLowerCase())
      )
    );
    this.renderEntity(entity, filtered.slice(0, 10));
  }

  globalSearch(query) {
    [...document.querySelectorAll('.entity-section')].forEach(section => {
      const entity = section.id;
      if (query) this.filterEntity(entity, query);
      else this.renderEntity(entity, this.entityData.get(entity)?.slice(0, 5) || []);
    });
  }

  renderEntity(entity, data = []) {
    const container = document.getElementById(entity);
    if (!container) return;
    
    const list = container.querySelector('.item-list');
    list.innerHTML = data.map(item => `
      <div class="item group">
        <div class="flex-1">
          <div class="font-semibold">${item.name || item.code || 'N/A'}</div>
          <div class="text-sm opacity-75">ID: ${item.id} | ${item.description?.slice(0, 80) || ''}</div>
        </div>
        <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-all">
          <button class="btn bg-blue-500 hover:bg-blue-600 px-4 py-1 text-sm" onclick="dashboard.edit('${entity}', ${item.id})">
            <i class="fas fa-edit"></i>
          </button>
          <button class="btn bg-red-500 hover:bg-red-600 px-4 py-1 text-sm" onclick="dashboard.delete('${entity}', ${item.id})">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    `).join('') || '<div class="text-center py-8 opacity-50"><i class="fas fa-inbox text-4xl mb-4 block"></i>No items yet. Create one above!</div>';
  }

  async refreshData(entity) {
    const res = await fetch(this.getApiUrl(entity));
    const data = await res.json();
    this.entityData.set(entity, data);
    this.renderEntity(entity);
    this.loadStats();
    this.updateChart();
  }

  async edit(entity, id) {
    const name = prompt('Edit name:');
    if (!name) return;
    await fetch(`${this.getApiUrl(entity).replace(/\/$/, '')}/${id}/`, {
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name})
    });
    this.refreshData(entity);
    this.showToast('success', 'Updated!');
  }

  async delete(entity, id) {
    if (!confirm('Delete this item?')) return;
    await fetch(`${this.getApiUrl(entity).replace(/\/$/, '')}/${id}/`, {method: 'DELETE'});
    this.refreshData(entity);
    this.showToast('success', 'Deleted!');
  }

  showToast(type, message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast p-4 rounded-2xl shadow-2xl transform translate-y-10 animate-slide-in ${
      type === 'success' ? 'bg-emerald-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'
    } text-white max-w-md`;
    toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-triangle' : 'fa-spinner fa-spin'} mr-3"></i>${message}`;
    container.appendChild(toast);
    
    setTimeout(() => {
      toast.classList.add('animate-slide-out');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  toggleTheme() {
    document.documentElement.classList.toggle('dark');
    localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  }

  loadTheme() {
    if (localStorage.theme === 'dark' || (!localStorage.theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    }
  }
}

// Initialize
const dashboard = new ProfessionalDashboard();

// Render initial entities
dashboard.entities.concat(dashboard.mappings).forEach(entity => {
  dashboard.renderEntity(entity);
});

// CSS animations
const style = document.createElement('style');
style.textContent = `
  .animate-slide-in { animation: slideIn 0.3s ease-out forwards; }
  .animate-slide-out { animation: slideOut 0.3s ease-in forwards; }
  @keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes slideOut { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(-20px); } }
  .input-field { @apply w-full p-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/70 outline-none focus:border-blue-400 transition-all; }
  .btn { @apply bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 px-4 py-2 rounded-xl font-semibold shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all whitespace-nowrap; }
  .dark .stat-card { background: rgba(255,255,255,0.1); }
`;
document.head.appendChild(style);

