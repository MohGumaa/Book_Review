document.addEventListener("DOMContentLoaded", () => {
  // When form is submit create xml requests
  document.querySelector("#searchForm").onsubmit = (e) => {
    // Prevent actual
    e.preventDefault();
    let searchText = document.querySelector("#search");

    // Validate if user Enter value then create XML
    if (searchText.value == "") {
      showMessage("Please fill the field", "danger");
    } else {
      find_Books(searchText.value);
    }
  };
});

function showMessage(message, className) {
  document.querySelector("#book-list").innerHTML = "";
  const div = document.createElement("div");
  div.className = `alert alert-${className}`;
  div.appendChild(document.createTextNode(message));
  document.querySelector("#book-list").append(div);

  // Vanish in 3 seconds
  setTimeout(() => document.querySelector(".alert").remove(), 3000);
}

// Renders books list
function find_Books(searchText) {
  // Initialize XML request for books-list
  const request = new XMLHttpRequest();
  request.open("POST", "/search");

  // When request complete show result
  request.onload = () => {
    console.log(JSON.parse(request.responseText));
  };

  // Add searchText value to request data
  const data = new FormData();
  data.append("searchText", searchText);

  // Send request
  request.send(data);
}
