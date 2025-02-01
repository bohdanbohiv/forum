<script lang="ts">
    import Liked from "../assets/Like.svelte";
    import Comment from "../assets/Comment.svelte";

    interface Post {
        user: {
            name: string;
            photo: string; // URL to the user's photo
        };
        content: string;
        likes: number;
        comments: number;
    }

    let post: Post = {
        user: {
            name: "John Doe",
            photo: "https://picsum.photos/40/40", // Placeholder image URL
        },
        content:
            "This is the content of the post. It can be a longer text, even with multiple lines.",
        likes: 12,
        comments: 5,
    };

    let liked = false;
    let fill = "black"
    function handleLike() {
        liked = !liked;
        post.likes += liked ? 1 : -1;
        fill = liked? "red" : "black"
    }

    function handleComment() {
        // Handle comment logic here (e.g., open a comment section)
        console.log("Comment clicked");
    }
</script>

<div class="post-box">
    <div class="post-header">
        <div class="user-photo">
            <img src={post.user.photo} alt={post.user.name} />
        </div>
        <div class="user-name">
            {post.user.name}
        </div>
    </div>
    <div class="post-content">
        {post.content}
    </div>
    <div class="post-actions">
        <button class="like-button" on:click={handleLike}>
            <Liked {fill}/>
            {post.likes}
        </button>

        <button class="comment-button" on:click={handleComment}>
            <Comment />
            {post.comments}
        </button>
    </div>
</div>

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

    .like-button,
    .comment-button {
        background: none;
        border: none;
        padding: 5px 10px;
        margin-right: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
    }

    
</style>
