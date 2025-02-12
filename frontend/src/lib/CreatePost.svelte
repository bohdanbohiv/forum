<script>
    export let showModal = false;
    let postText = "";

    const openModal = () => {
        showModal = true;
    };

    const closeModal = () => {
        showModal = false;
    };

    const submitPost = async() => {
        const token = localStorage.getItem("jwt_token")
        // Logic to submit the post, for now, just log the post text
        const data = {
            "private": false, 
            "body": postText, 
        }
        const endpoint = "http://127.0.0.1:8000/posts/";
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(data)
        };
        try{
            const response = await fetch(endpoint, requestOptions);
            if (!response.ok) {
                console.error("Some trouble happened");
                return
            } else {
                const data = await response.json();
                
                console.log(data)
                window.location.reload()
            }
        } catch (error){
            console.log("Could submit a post", error)
        }
        console.log("New post submitted:", postText);
        closeModal(); // Close the modal after submission
    };
</script>

<!-- Modal button to open the modal -->
<button on:click={openModal}>Create Post</button>

<!-- Modal content -->
{#if showModal}
    <div class="modal-overlay" on:click={closeModal}>
        <div class="modal" on:click|stopPropagation>
            <h2>Write your post</h2>
            <textarea
                bind:value={postText}
                placeholder="What's on your mind?"
                rows="5"
                cols="30"
            ></textarea>
            <div class="modal-footer">
                <button on:click={closeModal}>Cancel</button>
                <button on:click={submitPost}>Submit</button>
            </div>
        </div>
    </div>
{/if}

<style>
    /* Modal overlay */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Modal box */
    .modal {
        background: white;
        padding: 20px;
        border-radius: 8px;
        width: 300px;
        text-align: center;
    }

    /* Modal footer for buttons */
    .modal-footer {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }

    /* Button styles */
    button {
        padding: 10px 15px;
        border: none;
        background-color: #4caf50;
        color: white;
        cursor: pointer;
        border-radius: 5px;
    }

    button:hover {
        background-color: #45a049;
    }

    button:focus {
        outline: none;
    }

    textarea {
        width: 100%;
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }

    textarea:focus {
        border-color: #4caf50;
    }
</style>
