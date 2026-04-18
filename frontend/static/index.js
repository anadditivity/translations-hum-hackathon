const sendForm = async () => {
    const data = new URLSearchParams();
    for (const pair of new FormData(document.getElementById("query-form"))) {
        data.append(pair[0], pair[1]);
    }

    const response = await fetch(`http://localhost:8000/?${data}`, {method: 'GET'})
    const rdata = await response.json()
    console.log(rdata)
    const data_div = document.getElementById('response-data')
    for (let i = 0; i < rdata.response.length; i++) {
        const title = rdata.response[i].title
        data_div.innerHTML += `<p>${title}</p>`
    }
}
