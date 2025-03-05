document.addEventListener("DOMContentLoaded", function () {
    let searchInput = document.createElement("input");
    searchInput.setAttribute("type", "text");
    searchInput.setAttribute("placeholder", "Search by Name or Student ID...");
    searchInput.setAttribute("id", "inlineSearch");
    searchInput.style.marginBottom = "10px";
    searchInput.style.width = "100%";
    searchInput.style.padding = "5px";

    let inlineGroup = document.querySelector(".inline-group");
    if (inlineGroup) {
        inlineGroup.prepend(searchInput);
    } else {
        console.log("⚠️ Inline group not found!");
    }

    searchInput.addEventListener("keyup", function () {
        let filter = searchInput.value.toLowerCase();
        let rows = document.querySelectorAll("tr.form-row"); // Select all inline rows

        rows.forEach(function (row) {
            let nameColumn = row.querySelector("td.field-name p"); // Name field
            let studentIdColumn = row.querySelector("td.field-student_id p"); // Student ID field

            if (!nameColumn || !studentIdColumn) {
                console.log("⚠️ One or more columns not found in:", row);
                return;
            }

            let nameText = nameColumn.textContent.toLowerCase();
            let studentIdText = studentIdColumn.textContent.toLowerCase();
            console.log("🔍 Checking row:", nameText, studentIdText); // Debugging output

            if (nameText.includes(filter) || studentIdText.includes(filter)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});
