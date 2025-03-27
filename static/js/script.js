console.log("script.js loaded");
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".save-recipe").forEach(button => {
        button.addEventListener("click", async function () {
            const recipeId = this.dataset.recipeId;
            const originalText = this.innerText;
            this.innerText = "Processing...";
            this.disabled = true;
            
            try {
                const response = await fetch(`/recipes/${recipeId}/save/`, {
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
                    this.innerText = "Save to My Recipes";
                } else {
                    alert(data.message || "Operation failed. Please try again.");
                    this.innerText = originalText;
                }
            } catch (error) {
                console.error("Error processing save recipe:", error);
                alert("There was an error processing your request. Please try again later.");
                this.innerText = originalText;
            } finally {
                this.disabled = false;
            }
        });
    });
});

function getCSRFToken() {
    const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenElement ? tokenElement.value : "";
}
