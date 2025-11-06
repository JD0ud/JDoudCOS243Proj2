<script lang="ts">
    let {name, id/*, email*/, onDelete} = $props();
</script>
<h2>{name}</h2>
<!-- <p>{email}</p> -->

<button onclick={() => onDelete(id)}>Delete</button>