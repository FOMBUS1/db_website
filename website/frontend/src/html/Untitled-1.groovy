document.getElementById("saveEditActionTagBtn").addEventListener("click", async () => {
            const moodTagId = document.getElementById("editActionTagId").value;
            const title = document.getElementById("editActionTagTitle").value;
            if (!title) {
                alert("Заполните поле!");
                return;
            }
            try {
                const response = await fetch(`${moodTagsURL}/${moodTagID}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ActionTag_Title: title
                })
            });
            if (response.ok) {
                    fetchAlbums();
                    // Закрываем модальное окно
                    bootstrap.Modal.getInstance(document.getElementById("editActionTagModal")).hide();
                } else {
                    alert("Ошибка при обновлении жанра.");
                }
            } catch (error) {
                console.error("Ошибка:", error);
            }
        })