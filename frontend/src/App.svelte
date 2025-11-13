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

  let route = $derived($currentRoute);
  
  function getComponent(path) {
    if (!path || path === '/') return Home;
    if (path === '/about') return About;
    if (path === '/users') return Users;
    if (path === '/admin') return Admin;
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
</nav>

{#if CurrentComponent}
  <CurrentComponent />
{:else}
  <p>404 - Not Found</p>
{/if}
  <!-- <div>
    <a href="https://vite.dev" target="_blank" rel="noreferrer">
      <img src={viteLogo} class="logo" alt="Vite Logo" />
    </a>
    <a href="https://svelte.dev" target="_blank" rel="noreferrer">
      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    </a>
  </div>
  <h1>Vite + Svelte</h1>

  <div class="card">
    <Counter />
  </div>

  <p>
    Check out <a href="https://github.com/sveltejs/kit#readme" target="_blank" rel="noreferrer">SvelteKit</a>, the official Svelte app framework powered by Vite!
  </p>

  <p class="read-the-docs">
    Click on the Vite and Svelte logos to learn more
  </p> -->
</main>

<!-- <style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style> -->
