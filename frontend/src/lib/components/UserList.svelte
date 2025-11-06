<script lang="ts">
    import { onMount } from 'svelte';
    import User from './User.svelte'; //Import our user component

    let loading = $state(false); //Controls whether or not the loading message is dispalyed or not
    let error = $state(null); //Controls if error message displayed
    
    let users: any[];

    //When our page loads call fetch users
    onMount(() => {
        fetchUsers();
    });
    
    async function fetchUsers() {
        loading = true; //Tell user we're loading! Notice that this will automatically update on becaause it's reactive.
        error = null;
        
        try {
            //Your url may be different than mine
            const response = await fetch('http://127.0.0.1:8000/api/v1/users');

            if (!response.ok) throw new Error('Failed to fetch');
                users = await response.json();
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    }

    function refresh() {
        fetchUsers();
    }

    async function deleteUser(id) {
        if (confirm("Are you sure you want to delete?") == true) {
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/v1/users/${id}`, {method:'DELETE'});
            } catch (e) {
                console.log("ERROR: " + e);
            } finally {
                refresh();
            }
        }
    }
</script>

<h1>Users</h1>

{#if loading}
    <p>Loading...</p>
{:else if error}
    <p>ERROR: {error}</p>
{:else}
    {#each users as user}
        <User id={user.id} name={user.name} onDelete={deleteUser} />
    {/each}
    <br><br>
    <button onclick={refresh}>Refresh</button>
{/if}