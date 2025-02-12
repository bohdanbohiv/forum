<script>
    import Thread from "../lib/Thread.svelte";
    import { navigate } from "svelte-routing";
    import { jwtDecode } from "jwt-decode";
    import CreatePost from "../lib/CreatePost.svelte";
    const verifyJWT = async () => {
        const token = localStorage.getItem("jwt_token");

        if (!token) {
            console.error("No token found! Redirect to login page");
            navigate("/login", { replace: true });
        }

        const decoded = jwtDecode(token);
        console.log(decoded);
        console.log(decoded.sub);

        const endpoint = "http://127.0.0.1:8000/posts/";
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": `Bearer ${token}`
            },
        };
        try {
            const response = await fetch(endpoint, requestOptions);
            if (response.status === 401) {
                console.error("Token invalid");
                navigate("/login", { replace: true });
            } else {
                return;
            }
        } catch (error) {
            console.error("Error occured", error);
        }
    };
    verifyJWT();
    const logout = async () => {
        localStorage.removeItem("jwt_token");
        navigate("/login", { replace: true });
    };

    let openModal = false;

    const openPostModal = () => {
        openModal = true;
    };
</script>

<h1>Posts</h1>
<button on:click={logout}>Logout</button>
<CreatePost {openModal} />
<div class="card">
    <Thread />
</div>
