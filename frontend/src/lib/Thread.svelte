<script lang="ts">
    import { onMount } from "svelte";
    import { jwtDecode } from "jwt-decode";
    
    import Liked from "../assets/Like.svelte";

    let fill = "black";

    let posts = [];
    let users = [];
    

    const token = localStorage.getItem("jwt_token");
    const decoded = jwtDecode(token);
    const currentUser = parseInt(decoded.sub);
    
    let liked = "red"
    let notLiked = "black"
    const fetchPosts = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/posts"); // Adjust API URL
            if (!response.ok) {
                throw new Error(
                    `Error ${response.status}: ${response.statusText}`,
                );
            }
            posts = await response.json();
            
            for (let post of posts) {
                if (!users[post.owner_id]) {
                    const userResponse = await fetch(
                        `http://127.0.0.1:8000/users/${post.owner_id}`,
                    );
                    if (userResponse.ok) {
                        const userData = await userResponse.json();
                        users[post.owner_id] = userData.name; // Store the name by ID
                    }
                }
            }
        } catch (error) {
            console.error("Failed to fetch posts:", error.message);
        }
    };
    onMount(fetchPosts);

    const fetchRandomImage = () => {
        return `https://picsum.photos/40/40?random=${Math.random()}`;
    };

    const deletePost = async (postId: number) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/posts/${postId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`, 
                },
            });

            if (!response.ok) {
                throw new Error("Failed to delete post");
            }

            posts = posts.filter(post => post.id !== postId);
        } catch (error) {
            console.error("Error deleting post:", error);
        }
    };

    

    const toggleVote = async (postId, isVoted) => {
        try {
            const direction = isVoted ? 0 : 1; // 0 is for removing vote, 1 is for adding vote
            const response = await fetch(`http://127.0.0.1:8000/vote/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`, 
                },
                body: JSON.stringify({
                    post_id: postId,
                    direction: direction,
                }),
            });

            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }

            
            fetchPosts();
        } catch (error) {
            console.error("Failed to vote:", error.message);
        }
    };
    
</script>

{#if posts.length > 0}
    <ul>
        {#each posts as post}
            <div class="post-box">
                <div class="post-header">
                    <div class="user-photo">
                        <img src={fetchRandomImage()} />
                    </div>
                    <div class="user-name">
                        {users[post.owner_id] || "Loading owner..."}
                    </div>
                </div>
                <div class="post-content">
                    {post.body}
                </div>
                <div class="post-actions">
                    

                    {#if post.voters.some(voter => voter.id === currentUser)}
                        <button
                            class="like-button"
                            
                            on:click={() => toggleVote(post.id, true)}
                        >
                            <Liked fill="red" /> {post.voters.length}
                        </button>
                    {:else}
                        <button
                            class="like-button"
                            
                            on:click={() => toggleVote(post.id, false)}
                        >
                            <Liked fill="black" /> {post.voters.length}
                        </button>
                    {/if}

                    {#if post.owner_id === currentUser}
                        <button class = "del-button" on:click={() => deletePost(post.id)}>Del</button>
                    {/if}
                </div>
            </div>
        {/each}
    </ul>
{:else}
    <p>Loading posts...</p>
{/if}

<style>
    .post-box {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px; /* Space between posts */
        background-color: #f8f8f8; /* Light background color */
    }

    .post-header {
        display: flex;
        align-items: center; /* Vertically align items */
        margin-bottom: 10px;
    }

    .user-photo {
        width: 40px;
        height: 40px;
        border-radius: 50%; /* Make it a circle */
        overflow: hidden; /* Hide image overflow */
        margin-right: 10px;
    }

    .user-photo img {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Ensure image covers the circle */
    }

    .user-name {
        font-weight: bold;
    }

    .post-content {
        margin-bottom: 10px;
    }

    .post-actions {
        display: flex;
    }

    .like-button
    {
        background: none;
        border: none;
        padding: 5px 10px;
        margin-right: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
    }

    .del-button{
        color: rgb(232, 37, 37)
    }
    .upd-button{
        color: rgb(84, 84, 255)
    }
</style>
