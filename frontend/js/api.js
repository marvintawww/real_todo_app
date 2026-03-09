// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Token management
const TokenManager = {
    getAccessToken() {
        return localStorage.getItem('access_token');
    },

    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    },

    setTokens(accessToken, refreshToken) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
    },

    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    isAuthenticated() {
        return !!this.getAccessToken();
    }
};

// API Client
class APIClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        const token = TokenManager.getAccessToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);
            
            // Handle 401 - try to refresh token
            if (response.status === 401) {
                const refreshed = await this.tryRefreshToken();
                if (refreshed) {
                    // Retry the request with new token
                    config.headers['Authorization'] = `Bearer ${TokenManager.getAccessToken()}`;
                    const retryResponse = await fetch(url, config);
                    return this.handleResponse(retryResponse);
                } else {
                    // Refresh failed, redirect to login
                    handleLogout();
                    throw new Error('Сессия истекла');
                }
            }
            
            return this.handleResponse(response);
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async handleResponse(response) {
        const data = await response.json();
        
        if (!response.ok) {
            const error = new Error(data.detail || 'Произошла ошибка');
            error.status = response.status;
            error.data = data;
            throw error;
        }
        
        return data;
    }

    async tryRefreshToken() {
        const refreshToken = TokenManager.getRefreshToken();
        if (!refreshToken) return false;

        try {
            const response = await fetch(`${this.baseUrl}/refresh`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                TokenManager.setTokens(data.access_token, data.refresh_token);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
        }
        
        return false;
    }

    // GET request
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url, { method: 'GET' });
    }

    // POST request
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // PATCH request
    async patch(endpoint, data) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }

    // DELETE request
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Create API instance
const api = new APIClient(API_BASE_URL);

// Auth API
const AuthAPI = {
    async register(login, password) {
        return api.post('/register', { login, password });
    },

    async login(login, password) {
        return api.post('/login', { login, password });
    },

    async logout() {
        const refreshToken = TokenManager.getRefreshToken();
        if (refreshToken) {
            try {
                await api.post('/logout', { refresh_token: refreshToken });
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
        TokenManager.clearTokens();
    },

    async refreshToken() {
        return api.post('/refresh', { refresh_token: TokenManager.getRefreshToken() });
    }
};

// User API
const UserAPI = {
    async getProfile() {
        return api.get('/profile');
    }
};

// Task Types API
const TypeAPI = {
    async createType(title) {
        return api.post('/type', { title });
    },

    async getType(typeId) {
        return api.get(`/type/${typeId}`);
    },

    async getAllTypes() {
        return api.get('/types', { limit: 1000 });
    }
};

// Tasks API
const TaskAPI = {
    async createTask(typeId, data) {
        return api.post(`/tasks/create/${typeId}`, data);
    },

    async getTask(taskId) {
        return api.get(`/tasks/${taskId}`);
    },

    async getAllTasks(params = {}) {
        return api.get('/tasks', params);
    },

    async updateTask(taskId, data) {
        return api.patch(`/tasks/${taskId}`, data);
    },

    async updateTaskStatus(taskId, completed) {
        return api.patch(`/tasks/${taskId}/status`, { completed });
    },

    async deleteTask(taskId) {
        return api.delete(`/tasks/${taskId}`);
    }
};

// Export for use in app.js
window.TokenManager = TokenManager;
window.AuthAPI = AuthAPI;
window.UserAPI = UserAPI;
window.TypeAPI = TypeAPI;
window.TaskAPI = TaskAPI;

