//auth.svelte.js - Shared authentication state
export function createAuthStore() {
  let isAuthenticated = $state(false);
  let user = $state(null);

  // Check auth on initialization
  function init() {
    const token = localStorage.getItem('access_token');
    //For future use, if want to store some user data instaed of fetching it
    const userData = localStorage.getItem('user');
    
    if (token) {
      isAuthenticated = true;
      user = userData ? JSON.parse(userData) : null;
    }
  }

  function login(token, userData = null) {
    localStorage.setItem('access_token', token);
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData));
      user = userData;
    }
    isAuthenticated = true;
  }

  function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    isAuthenticated = false;
    user = null;
  }

  function getToken() {
    return localStorage.getItem('access_token');
  }

  // Initialize on creation
  init();

  return {
    get isAuthenticated() { return isAuthenticated; },
    get user() { return user; },
    login,
    logout,
    getToken
  };
}

// Create singleton instance
export const authStore = createAuthStore();