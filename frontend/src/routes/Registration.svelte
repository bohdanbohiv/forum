<script>
  import { navigate } from "svelte-routing";


  let name = "";
  let email = "";
  let password = "";
  let confirmPassword = "";
  let errorMessage = "";
  let successMessage = "";


  const handleSubmit = () => {
    const endpoint = "http://127.0.0.1:8000/users"
    const requestOptions = {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        name: name,
        email: email,
        password: password 
      })
    }
    if (password!==confirmPassword){
      errorMessage = "Passwords doesn't match"
      return; 
    }
    try {
      const response =  fetch(endpoint, requestOptions);
      const data =  response.json();

      if (response.status === 201){
        navigate("/login", { replace: true });
      } else {
        errorMessage = data.detail 
        console.log(data)
      }
    } catch (error){
      console.error("Error submitting form", error);
      errorMessage = "Something went wrong, please try again";
    }
    
  }
  
  
</script>

<h1>Registration</h1>

<form on:submit|preventDefault={handleSubmit} id="registration">
  <label for="name">Name:</label>
  <input type="name" id="name" bind:value={name} required />

  <label for="email">Email:</label>
  <input type="email" id="email" bind:value={email} required />

  <label for="password">Password:</label>
  <input type="password" id="password" bind:value={password} required />

  <label for="confirmPassword">Confirm Password:</label>
  <input
    type="password"
    id="confirmPassword"
    bind:value={confirmPassword}
    required
  />

  <button type="submit">Register</button>

  {#if errorMessage}
    <div class="error-message">{errorMessage}</div>
  {/if}

  {#if successMessage}
    <div class="success-message">{successMessage}</div>
  {/if}
</form>
<p>Already have an account? Proceed to login <a target="_blank" rel="noreferrer" on:click={() => navigate("/login", {replace: true})}>here</a></p>
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
  input[type="password"],
  input[type="name"] {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    box-sizing: border-box; /* Prevents padding from increasing width */
  }
</style>
