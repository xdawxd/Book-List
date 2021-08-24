
var checkbox = {
    checkedBooks: {},
    fixJSON: function(){
        for (let isbn of this.checkedBooks){
            if (this.checkedBooks[isbn] === 'not-added'){
                delete this.checkedBooks[isbn];
            }
        }
    },
    ifChecked: function(checkbox){
        let bookData = checkbox.parentElement.dataset.book;

        if (checkbox.checked){
            checkbox.parentElement.dataset.action = "added";
        }
        else {
            checkbox.parentElement.dataset.action = "not-added";
        }

        let bookAction = checkbox.parentElement.dataset.action;

        this.checkedBooks[bookData] = bookAction;

        console.log(this.checkedBooks);
    }

}

function fetchData(){
    let books = checkbox.checkedBooks;
    let url = "http://127.0.0.1:8000/"

    console.log(books);

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({books}),
        }
    )

    .then((response) => {
        return response.json();
    })
}
