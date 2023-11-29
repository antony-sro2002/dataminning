const csvFilePath = '../assets/tables/resultados_modelo.csv';

// Función para cargar el archivo CSV y generar la tabla
function generateTableFromCSV(csv) {
    const lines = csv.split('\n');
    let html = ' <h5>Correlation Matrix</h5> <table>';

    lines.forEach(function (line) {
        html += '<tr>';
        const columns = line.split(',');
        columns.forEach(function (column) {
            html += `<td>${column}</td>`;
        });
        html += '</tr>';
    });

    html += '</table>';
    return html;
}

// Cargar el archivo CSV utilizando Fetch API
fetch(csvFilePath)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(csvData => {
        const table = generateTableFromCSV(csvData);
        document.getElementById('tableContainer').innerHTML = table;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });