<script lang="ts">
    let {name, id, onDelete} = $props();
</script>
<div class="user">
    <h2>{name}</h2>

    <button onclick={() => onDelete(id)}>Delete</button>
</div>