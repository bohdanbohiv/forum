<script>
import { navigate } from "svelte-routing";

function onSubmit() {
    navigate("/posts", { replace: true });
}
let email = '';
  let password = '';
  let confirmPassword = '';
  let errorMessage = '';
  let successMessage = '';

  async function handleSubmit() {
    errorMessage = '';
    successMessage = '';

    if (password !== confirmPassword) {
      errorMessage = "Passwords do not match.";
      return;
    }

    try {
      const response = await fetch('/register', { // Your FastAPI registration endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }), // Send email and password
      });

      if (response.ok) {
        successMessage = 'Registration successful! Please log in.';
        // Clear the form after successful registration
        email = '';
        password = '';
        confirmPassword = '';
        // Redirect after a delay (optional) or directly to the login page
        setTimeout(() => {
          // if using svelte-routing
          goto('/login'); // Or wherever you want to redirect
          // if not using it:
          // if (browser) {
          //   window.location.href = '/login';
          // }
        }, 2000); // 2-second delay (adjust as needed)
      } else {
        const errorData = await response.json();
        errorMessage = errorData.detail || 'Registration failed.';
      }
    } catch (error) {
      errorMessage = 'An error occurred.';
      console.error('Error:', error);
    }
  }
</script>

<h1>Login</h1>

<form on:submit|preventDefault={handleSubmit}>
    <label for="email">Email:</label>
    <input type="email" id="email" bind:value={email} required>
  
    <label for="password">Password:</label>
    <input type="password" id="password" bind:value={password} required>
  
    <label for="confirmPassword">Confirm Password:</label>
    <input type="password" id="confirmPassword" bind:value={confirmPassword} required>
  
    <button type="submit" on:click={onSubmit}>Register</button>
  
    {#if errorMessage}
      <div class="error-message">{errorMessage}</div>
    {/if}
  
    {#if successMessage}
      <div class="success-message">{successMessage}</div>
    {/if}
  </form>

<!-- <button on:click={onSubmit}>Click me</button> -->

<style>
    /* ... your CSS styles ... */
    .error-message {
      color: red;
      margin-top: 10px;
    }
  
    .success-message {
      color: green;
      margin-top: 10px;
    }
  
    label {
      display: block; /* Makes labels stack on top of inputs */
      margin-bottom: 5px;
    }
  
    input[type="email"],
    input[type="password"] {
      width: 100%;
      padding: 8px;
      margin-bottom: 10px;
      box-sizing: border-box; /* Prevents padding from increasing width */
    }
  </style>