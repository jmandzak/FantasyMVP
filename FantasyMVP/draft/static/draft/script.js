function sortTable(columnIndex, dataType) {
    var table = document.getElementById("playersTable");
    var rows = table.rows;
    var players = [];

    // Gather all player rows into an array
    for (var i = 1; i < rows.length; i++) {
        var player = [];
        var cells = rows[i].getElementsByTagName("td");
        for (var j = 0; j < cells.length; j++) {
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
    var sorted = table.rows[0].getElementsByTagName("th")[columnIndex].getAttribute("data-sorted");
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
    for (var i = 0; i < players.length; i++) {
        var cells = rows[i + 1].getElementsByTagName("td");
        for (var j = 0; j < cells.length; j++) {
            cells[j].innerHTML = players[i][j];
        }
    }
}

function toggleColumn(columnIndex) {
    // Toggle class for header
    var header = document.querySelector(`#playersTable th:nth-child(${columnIndex + 1})`);
    if (header) {
        header.classList.toggle('hidden-column');
    }
    // Toggle class for each cell in the column
    var rows = document.querySelectorAll(`#playersTable td:nth-child(${columnIndex + 1})`);
    rows.forEach(function(cell) {
        cell.classList.toggle('hidden-column');
    });
}

function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// Set column headers as sortable on document ready
document.addEventListener("DOMContentLoaded", function() {
    var headers = document.querySelectorAll("#playersTable th");
    headers.forEach(function(header, index) {
        header.addEventListener("click", function() {
            // Look at the first row to determine the data type of the column
            var dataType = "string";
            var cells = document.querySelectorAll("#playersTable tr:nth-child(2) td");
            if (!isNaN(cells[index].innerHTML)) {
                dataType = "number";
            }
            sortTable(index, dataType);
        });
    });
});