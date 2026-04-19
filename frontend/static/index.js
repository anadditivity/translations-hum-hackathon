const sendForm = async () => {
    const data = new URLSearchParams();
    for (const pair of new FormData(document.getElementById("query-form"))) {
        data.append(pair[0], pair[1]);
    }

    const data_div = document.getElementById('response-data');
    data_div.innerHTML = '<p class="loading">Searching…</p>';

    let rdata;
    try {
        const response = await fetch(`http://localhost:8000/query_translation?${data}`, { method: 'GET' });
        rdata = await response.json();
    } catch (err) {
        data_div.innerHTML = '<p class="error">Could not reach the server. Please try again.</p>';
        return;
    }

    const results = rdata.response ?? rdata;
    data_div.innerHTML = '';

    if (!results || results.length === 0) {
        data_div.innerHTML = '<p class="no-results">No results found for this query.</p>';
        return;
    }

    const count = document.createElement('p');
    count.className = 'result-count';
    count.textContent = `${results.length} result${results.length !== 1 ? 's' : ''} found`;
    data_div.appendChild(count);

    for (const book of results) {
        const card = document.createElement('div');
        card.className = 'result-card';

        const row = (label, value) => {
            if (!value && value !== 0) return '';
            return `
                <div class="card-row">
                    <span class="card-label">${label}</span>
                    <span class="card-value">${value}</span>
                </div>`;
        };

        card.innerHTML = `
            <div class="card-header">
                <span class="card-title">${book.title ?? '—'}</span>
                ${book.publication_year ? `<span class="card-year">${book.publication_year}</span>` : ''}
            </div>
            <div class="card-body">
                ${row('Author',              book.author)}
                ${row('Original title',      book.title_original)}
                ${row('Translator',          book.translator)}
                ${row('Source language',     book.source_language)}
                ${row('Source literature',   book.source_literature)}
                ${row('Publisher',           book.publisher)}
                ${row('Location',            book.publication_location)}
                ${row('Series',              book.series)}
                ${row('Genre',               book.genre)}
                ${row('Edition',             book.edition)}
                ${row('Fore/afterword by',   book.fore_afterword_author)}
                ${row('Publication type',    book.publication_type)}
                ${row('Target audience',     book.target_audience)}
                ${row('Entry language',      book.entry_lang)}
            </div>`;

        data_div.appendChild(card);
    }
};
