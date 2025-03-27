document.addEventListener("DOMContentLoaded", () => {
    // Like functionality
    document.querySelectorAll(".like-button").forEach(button => {
        button.addEventListener("click", async function () {
            const recipeId = this.dataset.recipeId;
            const likeCountElem = this.nextElementSibling; 

            try {
                const response = await fetch(`/like/${recipeId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    },
                    credentials: "same-origin"
                });
                const data = await response.json();
                if (data.liked) {
                    this.innerHTML = "❤️ Liked";
                } else {
                    this.innerHTML = "🤍 Like";
                }
                if (likeCountElem) {
                    likeCountElem.innerText = data.total_likes;
                }
            } catch (error) {
                console.error("Error:", error);
                alert("There was an error processing your like. Please try again later.");
            }
        });
    });

    // Save/Unsave recipe functionality
    document.querySelectorAll(".save-recipe").forEach(button => {
        button.addEventListener("click", async function () {
            const recipeId = this.dataset.recipeId;
            const originalText = this.innerText;
            this.innerText = "Processing...";

            try {
                const response = await fetch(`/save_recipe/`, {
                    method: "POST",  
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    },
                    credentials: "same-origin",
                    body: JSON.stringify({ recipe_id: recipeId })
                });
                const data = await response.json();

                if (data.saved) {
                    this.innerText = "Saved";
                } else if (data.unsaved) {
                    this.innerText = "Save Recipe";
                } else {
                    alert(data.message || "Operation failed. Please try again.");
                    this.innerText = originalText;
                }
            } catch (error) {
                console.error("Error:", error);
                alert("There was an error processing your request. Please try again later.");
                this.innerText = originalText;
            }
        });
    });
});

function getCSRFToken() {
    const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenElement ? tokenElement.value : "";
}
