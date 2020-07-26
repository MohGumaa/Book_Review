const bookList = document.querySelector("#book-list");
document.addEventListener("DOMContentLoaded", () => {
  // When form is submit create xml requests
  document.querySelector("#searchForm").onsubmit = (e) => {
    // Prevent actual
    e.preventDefault();
    let searchText = document.querySelector("#search");

    // Validate if user Enter value then create XML
    if (searchText.value == "") {
      showMessage("Please enter title, author or ISBN!", "danger");
    } else {
      find_Books(searchText.value);
    }
  };
});

function showMessage(message, className) {
  bookList.innerHTML = "";
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
    const books = JSON.parse(request.responseText);
    if (books.success) {
      bookList.innerHTML = `;
      <h1 class="font-weight-bold my-4">${books.books_list.length} book found</h1>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Year</th>
            <th></th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>`;
      books.books_list.forEach((book) => displayBook(book));
    } else {
      showMessage(books.msg, "danger");
      console.log(books.msg);
    }
  };

  // Add searchText value to request data
  const data = new FormData();
  data.append("searchText", searchText);

  // Send request
  request.send(data);
}

function displayBook(book) {
  const row = document.createElement("tr");

  row.innerHTML = `
    <td><a href="/book/${book.isbn}" class="text-primary text-decoration">${book.title}</a></td>
    <td>${book.author}</td>
    <td>${book.isbn}</td>
    <td>${book.year}</td>
    <td><a href="/book/${book.isbn}" class="text-primary text-decoration">Details</a></td>
    `;

  document.querySelector("tbody").append(row);
  document.querySelector("#search").value = "";
  console.log(book);
}

// Set year in footer
const year = new Date().getFullYear();
document.querySelector("#year").innerHTML = year;
