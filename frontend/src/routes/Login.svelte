<script>
    let email = "";
    let password = "";
    let errorMessage = "";
    let successMessage = "";

   
    
    
    let handleLogin = () => {
        const endpoint = "http://127.0.0.1:8000/login/access-token";
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({username: email, password: password})
        };

        fetch(endpoint, requestOptions)
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
            });
    };
</script>

<h1>Login</h1>

<form on:submit|preventDefault={handleLogin} id="login">
    <label for="email">Email:</label>
    <input type="email" id="email" bind:value={email} required />

    <label for="password">Password:</label>
    <input type="password" id="password" bind:value={password} required />

    <button type="submit">Login</button>

    {#if errorMessage}
        <div class="error-message">{errorMessage}</div>
    {/if}

    {#if successMessage}
        <div class="success-message">{successMessage}</div>
    {/if}
</form>

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
