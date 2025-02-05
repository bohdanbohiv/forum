<script>
    import Thread from"../lib/Thread.svelte"
    import { navigate } from "svelte-routing";

    function onSubmit() {
        navigate("/", { replace: true });
    }

    
</script>
<h1>Posts</h1>
<button on:click={onSubmit}>Logout</button>
<div class="card">
    <Thread />
    <Thread />
    <Thread />
</div>