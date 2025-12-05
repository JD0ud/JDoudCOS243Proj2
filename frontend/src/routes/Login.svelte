<script lang="ts">
    import { authStore } from "../lib/stores/auth.svelte";

    interface Token {
        access_token: string;
        token_type: string;
    }

    interface LoginError {
        detail: string;
    }

    let {sendLogin} = $props();

    let isLoggedIn = $state(false);
    let username = $state('');
    let password = $state('');
    let loading = $state(false);
    let error = $state<string | null>(null);
    let token = $state<Token | null>(null);
    let isLogin = $state(true);
    let full_name = $state("");
    let email = $state("");
 
    const API_URL = 'http://localhost:8000/api/v1';

    $effect(() => {
        isLoggedIn = localStorage.getItem('access_token') != "" ? true : false;
    });

    async function handleSubmit(e: Event) {
        e.preventDefault();
        loading = true;
        error = null;
        token = null;

        try {
            // Create FormData for OAuth2PasswordRequestForm
            const formData = new FormData();
            formData.append('grant_type', "password");
            formData.append('username', username);
            formData.append('password', password);

            console.log("Calling function");

            const response = await fetch(`${API_URL}/users/token`, {
                method: 'POST',
                body: formData,
            });

            console.log(response);

            if (!response.ok) {
                const errorData: LoginError = await response.json();
                throw new Error(errorData.detail || 'Login failed');
            }

            const data: Token = await response.json();
            token = data;
      
            // Store token in authstore for future requests
            authStore.login(data.access_token, null);
            console.log(authStore.isAuthenticated);
            // Clear form
            username = '';
            password = '';
        } catch (err) {
            error = err instanceof Error ? err.message : 'An error occurred';
        } finally {
            loading = false;
        }
    }

    function logout() {
        token = null;
        authStore.logout()
    }

    function toggleMode() {
        isLogin = !isLogin;
        error = '';
    }
</script>

<br>
{#if token}
    <p>Token type: {token.token_type}</p>
    <p>Access token: {token.access_token}</p>
{:else}
    <h1>Login</h1>
    <form onsubmit={handleSubmit} >
        <div id="loginForm">
            <input type="text" id="username" name="username" disabled={loading} bind:value={username} placeholder="Username..." />
            <input type="password" id="password" name="password" disabled={loading} bind:value={password} placeholder="Password..." />
        </div>
        <button type="submit" disabled={loading}>Login</button>
    </form>
    {#if error}
        <p>ERROR: {error}</p>
    {/if}
{/if}