const sendForm = async () => {
    const form = document.getElementById("upload-form");
    const data = Object.fromEntries(new FormData(form));
    await fetch("http://localhost:8000/upload_translation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
}
