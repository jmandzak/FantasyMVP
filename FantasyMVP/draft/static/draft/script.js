$(document).ready(function() {
    // Function to sort table by column using merge sort
    function mergeSort(arr, columnIndex, dataType) {
        if (arr.length <= 1) {
            return arr;
        }
        
        const mid = Math.floor(arr.length / 2);
        const left = mergeSort(arr.slice(0, mid), columnIndex, dataType);
        const right = mergeSort(arr.slice(mid), columnIndex, dataType);
        
        return merge(left, right, columnIndex, dataType);
    }
    
    function merge(left, right, columnIndex, dataType) {
        let result = [];
        let i = 0, j = 0;
        
        while (i < left.length && j < right.length) {
            if (dataType === 'string') {
                if (left[i][columnIndex].toLowerCase() <= right[j][columnIndex].toLowerCase()) {
                    result.push(left[i++]);
                } else {
                    result.push(right[j++]);
                }
            } else if (dataType === 'number') {
                if (parseFloat(left[i][columnIndex]) <= parseFloat(right[j][columnIndex])) {
                    result.push(left[i++]);
                } else {
                    result.push(right[j++]);
                }
            }
        }
        
        while (i < left.length) {
            result.push(left[i++]);
        }
        
        while (j < right.length) {
            result.push(right[j++]);
        }
        
        return result;
    }
    
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
        
        // Sort the players array based on the selected column
        var sortedPlayers = mergeSort(players, columnIndex, dataType);
        
        // Re-render the table with sorted data
        var tbody = table.getElementsByTagName("tbody")[0];
        while (tbody.firstChild) {
            tbody.removeChild(tbody.firstChild);
        }
        
        for (var i = 0; i < sortedPlayers.length; i++) {
            var row = document.createElement("tr");
            for (var j = 0; j < sortedPlayers[i].length; j++) {
                var cell = document.createElement("td");
                cell.innerHTML = sortedPlayers[i][j];
                row.appendChild(cell);
            }
            tbody.appendChild(row);
        }
    }
    
    // Event listeners for each table header (column) to trigger sorting
    $("th").click(function() {
        var index = $(this).index(); // Get column index of clicked header
        var dataType = $(this).data("type"); // Get data type (string or number) from data-type attribute
        sortTable(index, dataType);
    });
});
