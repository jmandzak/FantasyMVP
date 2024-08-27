let CURRENT_POSITION = "all";

function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// This function is called when a label inside the dropdown is clicked. Toggle the visibility of the column to match the checkbox
function selectColumn(index) {
    toggleColumn(index);
}

function changePosition(position) {
    CURRENT_POSITION = position;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", changePositionUrl, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            updatePlayersTable(response.players, response.headers);
            setSortListener();
        }
    };

    xhr.send("position=" + position);
}

function updatePlayersTable(players, headers) {
    const table = document.getElementById("playersTable");

    // Update headers
    const thead = table.getElementsByTagName("thead")[0];
    thead.innerHTML = ""; // Clear existing headers
    const headerRow = document.createElement("tr");
    headers.forEach(header => {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Update rows
    const tbody = table.getElementsByTagName("tbody")[0];
    tbody.innerHTML = ""; // Clear existing rows
    players.forEach(player => {
        const row = document.createElement("tr");
        player.forEach(cell => {
            const td = document.createElement("td");
            td.textContent = cell;
            row.appendChild(td);
        });
        row.onclick = function() {
            highlightRow(row);
        };
        tbody.appendChild(row);
    });
}

function sortTable(columnIndex, dataType) {
    let table = document.getElementById("playersTable");
    let rows = table.rows;
    let players = [];

    // Gather all player rows into an array
    for (let i = 1; i < rows.length; i++) {
        let player = [];
        let th_cells = rows[i].getElementsByTagName("th");
        let td_cells = rows[i].getElementsByTagName("td");
        if(td_cells.length < 0) {
            continue;
        }
        let cells = Array()
        for(let j = 0; j < th_cells.length; j++) {
            cells.push(th_cells[j]);
        }
        for(let j = 0; j < td_cells.length; j++) {
            cells.push(td_cells[j]);
        }
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
        let th_cells = rows[i + 1].getElementsByTagName("th");
        let td_cells = rows[i + 1].getElementsByTagName("td");
        let cells = Array()
        for(let j = 0; j < th_cells.length; j++) {
            cells.push(th_cells[j]);
        }
        for(let j = 0; j < td_cells.length; j++) {
            cells.push(td_cells[j]);
        }
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

function highlightRow(row) {
    // Check if row is already highlighted
    if (row.classList.contains('highlight')) {
        row.classList.remove('highlight');
        return;
    }
    
    // Remove highlight from all rows
    var rows = document.querySelectorAll('tr');
    rows.forEach(function(r) {
        r.classList.remove('highlight');
    });

    // Add highlight to the clicked row
    row.classList.add('highlight');
}

function draftPlayer() {
    // Find the highlighted row
    var rows = document.querySelectorAll('tr');
    var playerRow;
    rows.forEach(function(row) {
        if (row.classList.contains('highlight')) {
            playerRow = row;
        }
    });
    // Get the player name from the row, which is in the first cell
    var playerName = playerRow.getElementsByTagName('td')[0].innerHTML;
    // Send the player name to the server
    const xhr = new XMLHttpRequest();
    xhr.open("POST", draftPlayerUrl, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            updatePlayersTable(response.players, response.headers);
            setSortListener();
        }
    }

    // send playerName and current position
    xhr.send("player_name=" + playerName + "&position=" + CURRENT_POSITION);
}

function removePlayer() {
    // Find the highlighted row
    var rows = document.querySelectorAll('tr');
    var playerRow;
    rows.forEach(function(row) {
        if (row.classList.contains('highlight')) {
            playerRow = row;
        }
    });
    // Get the player name from the row, which is in the first cell
    var playerName = playerRow.getElementsByTagName('td')[0].innerHTML;
    // Send the player name to the server
    const xhr = new XMLHttpRequest();
    xhr.open("POST", removePlayerUrl, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            updatePlayersTable(response.players, response.headers);
            setSortListener();
        }
    }

    // send playerName and current position
    xhr.send("player_name=" + playerName + "&position=" + CURRENT_POSITION);
}

function setSortListener() {
    let headers = document.querySelectorAll("#playersTable tr:first-child th");
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
}

// // Set column headers as sortable on document ready
// document.addEventListener("DOMContentLoaded", function() {
//     let headers = document.querySelectorAll("#playersTable tr:first-child th");
//     headers.forEach(function(header, index) {
//         header.addEventListener("click", function() {
//             // Look at the first row to determine the data type of the column
//             let dataType = "string";
//             let cells = document.querySelectorAll("#playersTable tr:nth-child(2) td");
//             if (!isNaN(cells[index].innerHTML)) {
//                 dataType = "number";
//             }
//             sortTable(index, dataType);
//         });
//     });
// });

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