<script lang="ts">
  import svelteLogo from './assets/svelte.svg'
  import viteLogo from '/vite.svg'
  import Counter from './lib/Counter.svelte'
  import UserList from './lib/components/UserList.svelte';
  import {currentRoute} from '../router.js';
  import Home from './routes/Home.svelte';
  import About from './routes/About.svelte';
  import Users from './routes/Users.svelte';
  import Admin from './routes/Admin.svelte';
  import Login from './routes/Login.svelte';
  import Profile from './routes/Profile.svelte';
  import {authStore} from './lib/stores/auth.svelte.js'

  let route = $derived($currentRoute);
  
  function getComponent(path) {
    if (!path || path === '/') return Home;
    if (path === '/about') return About;
    if (path === '/users') return Users;
    if (path === '/admin') return Admin;
    if (path === '/login') return Login;
    if (path === '/profile') return Profile;
    return null;
  }

  let CurrentComponent = $derived(getComponent(route));
</script>

<main>
  <nav>
  <a href="#/">Home</a>
  <a href="#/users">Users</a>
  <a href="#/about">About</a>
  <a href="#/admin">Admin</a>
  {#if authStore.isAuthenticated}
    <a href="#/profile">Profile</a>
    <button onclick={() => authStore.logout()} class="btn-logout">Logout</button>
  {:else}
    <a href="#/login">Login</a>
  {/if}
</nav>

{#if CurrentComponent}
  <div id="currentComponent">
    <CurrentComponent />
  </div>
{:else}
  <p>404 - Not Found</p>
{/if}

<footer>
  <a href="#/about">About</a>
  <a href="#/admin">Admin Page (admins only (obviously))</a>
</footer>

</main>