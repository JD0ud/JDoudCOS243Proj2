<script lang="ts">
    import { onMount } from 'svelte';
    import User from './User.svelte'; //Import our user component
    import { preprocess } from 'svelte/compiler';

    let loading = $state(false); //Controls whether or not the loading message is dispalyed or not
    let error = $state(null); //Controls if error message displayed
    
    let users: any[];
    let userCount = $state("0");

    let perPage = $state("10");
    let perPageResults = $derived(parseInt(perPage));
    let totalPages = $derived(Math.ceil(parseInt(userCount) / perPageResults));
    let currentPage = $state("1");

    let userSearchText = $state("");

    //When our page loads call fetch users
    onMount(() => {
        fetchUsers();
    });
    
    async function fetchUsers() {
        loading = true; //Tell user we're loading! Notice that this will automatically update on becaause it's reactive.
        error = null;

        try {
            //Your url may be different than mine
            const response = await fetch(`http://127.0.0.1:8000/api/v1/users/?perPage=${perPage}&curPage=${currentPage}&searchText=${userSearchText}`);

            if (!response.ok) throw new Error('Failed to fetch');
                // let headers = await response;
            
                response.headers.forEach((value, key) => {
                    console.log(`${key}: ${value}`);
                });
                userCount = response.headers.get('X-Total-Count');
                users = await response.json();
                // userCount = response.headers.get('X-Total-Count');
                // console.log("|" + userCount + "|");
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
                if (parseInt(currentPage) > totalPages) currentPage = totalPages.toString();
                refresh();
            }
        }
    }

    function goToPage(event: MouseEvent, page: number) {
        event.preventDefault();
        currentPage = page.toString();
        refresh();
    }

    function userSearch() {
        currentPage = "1";
        refresh();
    }
</script>

{#if loading}
    <p>Loading...</p>
{:else if error}
    <p>ERROR: {error}</p>
{:else}
    <div id="userSearchDiv">
        <input type="text" id="userSearch" bind:value={userSearchText} oninput={userSearch} placeholder="Search..." />
        <div>
            <label for="perPage">Showing</label>
            <select id="perPage" bind:value={perPage} onchange={refresh}>
                <option value="5">5</option>
                <option value="10" selected>10</option>
                <option value="20">20</option>
                <option value="50">50</option>
                <option value="100">100</option>
            </select>
            <label for="perPage">of {userCount} results</label>
        </div>
        <button onclick={refresh}>Refresh</button>
    </div>

    <div id="userPages">
        {#if currentPage <= "1"}
            <button disabled>Prev</button>
        {:else}
            <button onclick={(e) => goToPage(e, parseInt(currentPage) - 1)}>Prev</button>
        {/if}
        {#each Array(totalPages).fill(0) as _, i}
            {#if i + 1 == parseInt(currentPage)}
                <button style="margin: 0 8px" onclick={(e) => goToPage(e, i + 1)} disabled>{i + 1}</button>
            {:else}
                <button style="margin: 0 8px" onclick={(e) => goToPage(e, i + 1)}>{i + 1}</button>
            {/if}
        {/each}
        {#if currentPage >= totalPages.toString()}
            <button disabled>Next</button>
        {:else}
            <button onclick={(e) => goToPage(e, parseInt(currentPage) + 1)}>Next</button>
        {/if}
    </div>

    {#each users as user}
        <User id={user.id} name={user.username} onDelete={deleteUser} />
    {/each}
{/if}