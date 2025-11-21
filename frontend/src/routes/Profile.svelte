<script lang="ts">
    import { authStore } from "../lib/stores/auth.svelte";
    import { onMount } from "svelte";

    let user: any;

    onMount(() => {
        fetchUser();
    })

    async function fetchUser() {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/users/me/`, {
            headers: { 'Authorization': `Bearer ${authStore.getToken()}` }
        });
        user = await response.json();
    }
    
</script>

<h1>Profile</h1>
<h2>Welcome, {user.full_name}</h2>
<p>Username: {user.username}</p>
<p>Email: {user.email}</p>