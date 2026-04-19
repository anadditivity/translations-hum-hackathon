const sendForm = async () => {
    const data = new URLSearchParams();
    for (const pair of new FormData(document.getElementById("query-form"))) {
        data.append(pair[0], pair[1]);
    }

    const response = await fetch(`http://localhost:8000/upload_translation`, {
        method: 'POST',
        body: data,
    })
}
