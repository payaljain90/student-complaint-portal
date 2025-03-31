document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-title");
    const statusFilter = document.getElementById("status-filter");
    const sortDate = document.getElementById("sort-date");
    const complaintRows = document.querySelectorAll(".complaint-row");
    
    // Function to filter complaints
    function filterComplaints() {
        const searchText = searchInput.value.toLowerCase();
        const selectedStatus = statusFilter.value.toLowerCase();

        complaintRows.forEach(row => {
            const title = row.querySelector(".complaint-title").textContent.toLowerCase();
            const status = row.dataset.status.toLowerCase();

            // Show/hide rows based on search & filter
            if ((title.includes(searchText) || searchText === "") && 
                (status === selectedStatus || selectedStatus === "all")) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    // Function to sort complaints
    function sortComplaints() {
        const tbody = document.getElementById("complaint-table-body");
        const rows = Array.from(tbody.querySelectorAll(".complaint-row"));

        rows.sort((a, b) => {
            const dateA = new Date(a.dataset.date);
            const dateB = new Date(b.dataset.date);

            return sortDate.value === "newest" ? dateB - dateA : dateA - dateB;
        });

        // Append sorted rows back to table
        rows.forEach(row => tbody.appendChild(row));
    }

    // Attach event listeners
    searchInput.addEventListener("input", filterComplaints);
    statusFilter.addEventListener("change", filterComplaints);
    sortDate.addEventListener("change", sortComplaints);
});
