<script lang="ts">
  import wsizLogo from '/wsiz.svg'
  import viteLogo from '/vite.svg'
  import Thread from './lib/Thread.svelte'
</script>

<main>
  <div>
    <a href="https://wsiz.edu.pl" target="_blank" rel="noreferrer">
      <img src={wsizLogo} class="logo" alt="Wsiz Logo" />
    </a>
    
  </div>
  <h1>Forum</h1>

  <div class="card">
    <Thread />
    <Thread />
    <Thread />
  </div>

  <p>
    Check out <a href="https://github.com/bohdanbohiv/forum" target="_blank" rel="noreferrer">Source code</a> made by Daniyar and Bohdan!
  </p>

</main>

<style>
  .logo {
    height: 10em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #3a3a3aaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
