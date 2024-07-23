function sortTable(columnIndex, dataType) {
    let table = document.getElementById("playersTable");
    let rows = table.rows;
    let players = [];

    // Gather all player rows into an array
    for (let i = 1; i < rows.length; i++) {
        let player = [];
        let cells = rows[i].getElementsByTagName("td");
        for (let j = 0; j < cells.length; j++) {
            player.push(cells[j].innerHTML.trim());
        }
        players.push(player);
    }
    
    // Sort the array based on the data type of the column
    players.sort(function(a, b) {
        if (dataType === "number") {
            return a[columnIndex] - b[columnIndex];
        }
        else {
            return a[columnIndex].localeCompare(b[columnIndex]);
        }
    });

    // See if the column has already been sorted by using the data-sorted attribute
    let sorted = table.rows[0].getElementsByTagName("th")[columnIndex].getAttribute("data-sorted");
    if (sorted === "ascending") {
        // Reverse the array if it was already sorted in ascending order
        players.reverse();
        table.rows[0].getElementsByTagName("th")[columnIndex].setAttribute("data-sorted", "descending");
    }
    else {
        // Sort the array in ascending order
        table.rows[0].getElementsByTagName("th")[columnIndex].setAttribute("data-sorted", "ascending");
    }

    // Re-render the table with sorted data by simply replacing the value of each cell in the table
    for (let i = 0; i < players.length; i++) {
        let cells = rows[i + 1].getElementsByTagName("td");
        for (let j = 0; j < cells.length; j++) {
            cells[j].innerHTML = players[i][j];
        }
    }
}

function toggleColumn(columnIndex) {
    // Toggle class for header
    let header = document.querySelector(`#playersTable th:nth-child(${columnIndex + 1})`);
    if (header) {
        header.classList.toggle('hidden-column');
    }
    // Toggle class for each cell in the column
    let rows = document.querySelectorAll(`#playersTable td:nth-child(${columnIndex + 1})`);
    rows.forEach(function(cell) {
        cell.classList.toggle('hidden-column');
    });
}

function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    let isClickInsideDropdown = event.target.closest('.dropdown-content');
    if (!event.target.matches('.dropbtn') && !isClickInsideDropdown) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// This function is called when a label inside the dropdown is clicked. Toggle the visibility of the column to match the checkbox
function selectColumn(event, index) {
    toggleColumn(index);
}

function downloadTable() {
    // download the visible aspects of the table as a CSV file on the user computer with the name {position}_statistics.csv
    let table = document.getElementById("playersTable");
    let rows = table.rows;
    let csv = "";
    for (let i = 0; i < rows.length; i++) {
        // Get all th or td elements in the row
        if((rows[i].getElementsByTagName("th")).length > 0) {
            var cells = rows[i].getElementsByTagName("th");
        }
        else {
            var cells = rows[i].getElementsByTagName("td");
        }
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].classList.contains("hidden-column")) {
                continue;
            }
            csv += cells[j].innerHTML.trim();
            if (j < cells.length - 1) {
                csv += ",";
            }
        }
        csv += "\n";
    }

    let url = document.URL.toString();
    console.log(url)
    url = url.split("/");
    url.pop();
    let filename = url.pop() + ".csv";
    let blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    }
    else {
        let link = document.createElement("a");
        if (link.download !== undefined) {
            let url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = "hidden";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

function getPPRVersion() {
    // Get the current URL and add the query parameter to it
    let url = document.URL.toString();
    // Check and see if QB, DEF, or K is in the URL
    let position = "";
    if (url.includes("ppr")) {
        return;
    }
    else {
        // Prepend the last part of the url with PPR
        url = url.split("/");
        url.pop();
        position = url.pop();
        new_position = "ppr-" + position;
    }
    // Redirect to the PPR version of the page
    window.location.pathname = new_position;
}

function getStandardVersion() {
    // Get the current URL and add the query parameter to it
    let url = document.URL.toString();
    if (!url.includes("ppr")) {
        return;
    }
    else {
        // Remove PPR from the URL
        url = url.replace("ppr-", "");
    }
    // Redirect to the standard version of the page
    window.location.href = url;
}

function changePosition(position) {
    let has_ppr = false;
    let url = document.URL.toString();
    if (url.includes("ppr")) {
        has_ppr = true;
    }
    // Redirect to the new position
    window.location.pathname = (has_ppr ? "ppr-" : "") + position + "-statistics/";
}

// Set column headers as sortable on document ready
document.addEventListener("DOMContentLoaded", function() {
    let headers = document.querySelectorAll("#playersTable th");
    headers.forEach(function(header, index) {
        header.addEventListener("click", function() {
            // Look at the first row to determine the data type of the column
            let dataType = "string";
            let cells = document.querySelectorAll("#playersTable tr:nth-child(2) td");
            if (!isNaN(cells[index].innerHTML)) {
                dataType = "number";
            }
            sortTable(index, dataType);
        });
    });
});