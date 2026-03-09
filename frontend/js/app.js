// Application State
let currentUser = null;
let taskTypes = [];
let tasks = [];
let currentFilters = {
    search_query: '',
    completed: null,
    task_date: null,
    task_type: null
};
let searchTimeout = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

// Check authentication status
async function checkAuth() {
    if (TokenManager.isAuthenticated()) {
        try {
            currentUser = await UserAPI.getProfile();
            showMainApp();
            loadTasks();
            loadTaskTypes();
        } catch (error) {
            console.error('Auth check failed:', error);
            showAuth();
        }
    } else {
        showAuth();
    }
}

// Show auth screens
function showAuth() {
    document.getElementById('auth-container').classList.remove('hidden');
    document.getElementById('main-container').classList.add('hidden');
}

// Show main app
function showMainApp() {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('main-container').classList.remove('hidden');
    document.getElementById('user-greeting').textContent = `Привет, ${currentUser.login}!`;
}

// Auth handlers
function showLogin() {
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('register-form').classList.add('hidden');
}

function showRegister() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
}

async function handleLogin(event) {
    event.preventDefault();
    const login = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        showToast('Вход...', 'info');
        const tokens = await AuthAPI.login(login, password);
        TokenManager.setTokens(tokens.access_token, tokens.refresh_token);
        currentUser = await UserAPI.getProfile();
        showMainApp();
        loadTasks();
        loadTaskTypes();
        showToast('Добро пожаловать!', 'success');
        document.getElementById('login-form').reset();
    } catch (error) {
        showToast(error.message || 'Ошибка входа', 'error');
    }
    return false;
}

async function handleRegister(event) {
    event.preventDefault();
    const login = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    try {
        showToast('Регистрация...', 'info');
        const tokens = await AuthAPI.register(login, password);
        TokenManager.setTokens(tokens.access_token, tokens.refresh_token);
        currentUser = await UserAPI.getProfile();
        showMainApp();
        loadTaskTypes();
        showToast('Аккаунт создан!', 'success');
        document.getElementById('register-form').reset();
    } catch (error) {
        showToast(error.message || 'Ошибка регистрации', 'error');
    }
    return false;
}

async function handleLogout() {
    try {
        await AuthAPI.logout();
    } catch (error) {
        console.error('Logout error:', error);
    }
    currentUser = null;
    tasks = [];
    taskTypes = [];
    TokenManager.clearTokens();
    showAuth();
    showToast('Вы вышли из системы', 'info');
}

// Navigation
function showSection(section) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    document.getElementById('tasks-section').classList.add('hidden');
    document.getElementById('types-section').classList.add('hidden');
    document.getElementById('profile-section').classList.add('hidden');

    if (section === 'tasks') {
        document.getElementById('tasks-section').classList.remove('hidden');
    } else if (section === 'types') {
        document.getElementById('types-section').classList.remove('hidden');
    } else if (section === 'profile') {
        document.getElementById('profile-section').classList.remove('hidden');
    }
}

// Tasks
async function loadTasks() {
    try {
        const params = {};
        if (currentFilters.search_query) params.search_query = currentFilters.search_query;
        if (currentFilters.completed !== null && currentFilters.completed !== '') {
            params.completed = currentFilters.completed;
        }
        if (currentFilters.task_date) params.task_date = currentFilters.task_date;
        if (currentFilters.task_type) params.task_type = [currentFilters.task_type];

        tasks = await TaskAPI.getAllTasks(params);
        renderTasks();
    } catch (error) {
        showToast('Ошибка загрузки задач', 'error');
    }
}

function renderTasks() {
    const container = document.getElementById('tasks-list');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>Нет задач</h3>
                <p>Создайте новую задачу</p>
            </div>
        `;
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="task-card ${task.completed ? 'completed' : ''}">
            <div class="task-header">
                <span class="task-title">${escapeHtml(task.title)}</span>
                <input type="checkbox" class="task-checkbox" 
                    ${task.completed ? 'checked' : ''} 
                    onchange="toggleTaskStatus(${task.id}, this.checked)">
            </div>
            ${task.description ? `<p class="task-description">${escapeHtml(task.description)}</p>` : ''}
            <div class="task-meta">
                <span class="task-type">${task.type ? escapeHtml(task.type.title) : 'Без типа'}</span>
                <span>${formatDate(task.task_date)}</span>
            </div>
            <div class="task-actions">
                <button onclick="editTask(${task.id})" class="btn btn-secondary btn-small">Редактировать</button>
                <button onclick="deleteTask(${task.id})" class="btn btn-danger btn-small">Удалить</button>
            </div>
        </div>
    `).join('');
}

async function toggleTaskStatus(taskId, completed) {
    try {
        await TaskAPI.updateTaskStatus(taskId, completed);
        loadTasks();
        showToast(completed ? 'Задача выполнена!' : 'Задача отмечена как невыполненная', 'success');
    } catch (error) {
        showToast('Ошибка обновления статуса', 'error');
        loadTasks(); // Reload to reset checkbox
    }
}

// Task Modal
function showCreateTaskModal() {
    document.getElementById('task-modal-title').textContent = 'Создать задачу';
    document.getElementById('task-id').value = '';
    document.getElementById('task-title').value = '';
    document.getElementById('task-description').value = '';
    document.getElementById('task-date').value = '';
    
    // Populate type dropdown
    populateTypeDropdown();
    
    document.getElementById('task-modal').classList.remove('hidden');
}

async function editTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    document.getElementById('task-modal-title').textContent = 'Редактировать задачу';
    document.getElementById('task-id').value = task.id;
    document.getElementById('task-title').value = task.title;
    document.getElementById('task-description').value = task.description || '';
    document.getElementById('task-date').value = task.task_date ? task.task_date.split('T')[0] : '';
    
    // Populate type dropdown
    await populateTypeDropdown();
    if (task.type) {
        document.getElementById('task-type-select').value = task.type.id;
    }
    
    document.getElementById('task-modal').classList.remove('hidden');
}

function closeTaskModal() {
    document.getElementById('task-modal').classList.add('hidden');
}

async function populateTypeDropdown() {
    await loadTaskTypes();
    const select = document.getElementById('task-type-select');
    select.innerHTML = taskTypes.map(type => 
        `<option value="${type.id}">${escapeHtml(type.title)}</option>`
    ).join('');
    
    if (taskTypes.length === 0) {
        select.innerHTML = '<option value="">Сначала создайте тип задачи</option>';
    }
}

async function handleTaskSubmit(event) {
    event.preventDefault();
    
    const taskId = document.getElementById('task-id').value;
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-description').value;
    const taskDate = document.getElementById('task-date').value;
    const typeId = document.getElementById('task-type-select').value;

    if (!typeId) {
        showToast('Выберите тип задачи', 'error');
        return false;
    }

    const data = {
        title,
        description: description || null,
        task_date: taskDate || null
    };

    try {
        if (taskId) {
            await TaskAPI.updateTask(parseInt(taskId), data);
            showToast('Задача обновлена', 'success');
        } else {
            await TaskAPI.createTask(parseInt(typeId), data);
            showToast('Задача создана', 'success');
        }
        closeTaskModal();
        loadTasks();
    } catch (error) {
        showToast(error.message || 'Ошибка сохранения задачи', 'error');
    }
    return false;
}

async function deleteTask(taskId) {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) return;

    try {
        await TaskAPI.deleteTask(taskId);
        showToast('Задача удалена', 'success');
        loadTasks();
    } catch (error) {
        showToast('Ошибка удаления задачи', 'error');
    }
}

// Filters
function debouncedSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        currentFilters.search_query = document.getElementById('search-input').value;
        loadTasks();
    }, 300);
}

function applyFilters() {
    const completed = document.getElementById('filter-completed').value;
    currentFilters.completed = completed === '' ? null : completed === 'true';
    currentFilters.task_date = document.getElementById('filter-date').value || null;
    loadTasks();
}

function clearFilters() {
    document.getElementById('search-input').value = '';
    document.getElementById('filter-completed').value = '';
    document.getElementById('filter-date').value = '';
    currentFilters = {
        search_query: '',
        completed: null,
        task_date: null,
        task_type: null
    };
    loadTasks();
}

// Task Types
async function loadTaskTypes() {
    try {
        taskTypes = await TypeAPI.getAllTypes();
        renderTypes();
    } catch (error) {
        console.error('Error loading types:', error);
    }
}

function renderTypes() {
    const container = document.getElementById('types-list');
    
    if (taskTypes.length === 0) {
        container.innerHTML = '<p class="empty-state">Нет типов задач</p>';
        return;
    }

    container.innerHTML = taskTypes.map(type => `
        <div class="type-tag">
            <span>${escapeHtml(type.title)}</span>
        </div>
    `).join('');
}

async function handleCreateType(event) {
    event.preventDefault();
    const title = document.getElementById('type-title').value;

    try {
        await TypeAPI.createType(title);
        showToast('Тип задачи создан', 'success');
        document.getElementById('type-title').value = '';
        loadTaskTypes();
    } catch (error) {
        showToast(error.message || 'Ошибка создания типа', 'error');
    }
    return false;
}

// Profile
async function showProfile() {
    try {
        const user = await UserAPI.getProfile();
        document.getElementById('profile-id').textContent = user.id;
        document.getElementById('profile-login').textContent = user.login;
        document.getElementById('modal-profile-id').textContent = user.id;
        document.getElementById('modal-profile-login').textContent = user.login;
        document.getElementById('profile-modal').classList.remove('hidden');
    } catch (error) {
        showToast('Ошибка загрузки профиля', 'error');
    }
}

function closeProfileModal() {
    document.getElementById('profile-modal').classList.add('hidden');
}

// Toast notifications
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
}

// Close modals on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.add('hidden');
    }
};

// Make functions globally available
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.handleLogout = handleLogout;
window.showRegister = showRegister;
window.showLogin = showLogin;
window.showSection = showSection;
window.showCreateTaskModal = showCreateTaskModal;
window.closeTaskModal = closeTaskModal;
window.handleTaskSubmit = handleTaskSubmit;
window.editTask = editTask;
window.deleteTask = deleteTask;
window.toggleTaskStatus = toggleTaskStatus;
window.debouncedSearch = debouncedSearch;
window.applyFilters = applyFilters;
window.clearFilters = clearFilters;
window.handleCreateType = handleCreateType;
window.showProfile = showProfile;
window.closeProfileModal = closeProfileModal;

