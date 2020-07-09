const search = document.querySelector("#search");
const bookList = document.querySelector("#book-list");

//   Add Event to submit form
document.querySelector("#searchForm").addEventListener("submit", (e) => {
  e.preventDefault();

  // Validate if user Enter value then create XML
  if (search.value == "") {
    showMessage("Please fill the field", "danger");
  } else {
    find_Books(search.value);
  }
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
function find_Books(search) {
  // Initialize XML request for books-list
  const request = new XMLHttpRequest();
  request.open("POST", "/search");

  // When request complete show result
  request.onload = () => {
    const results = JSON.parse(request.responseText);

    // Check request result
    if (results.success) {
      document.querySelector("#book-list").innerHTML = `
        <h1 class="mt-5">List of books found ${results.book_list_len}</h1>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
              <th></th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>`;
      results.books.forEach((book) => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${book.title}</td>
          <td>${book.author}</td>
          <td>${book.isbn}</td>
          <td><a href="/bookpage/${book.isbn}" class="text-primary text-decoration">Details</a></td>
          `;

        document.querySelector("tbody").append(row);
        document.querySelector("#search").value = "";
      });
    } else {
      showMessage(results.error, "warning");
    }
  };

  // Add searchText value to request data
  const data = new FormData();
  data.append("searchText", search);

  // Send request
  request.send(data);
}
