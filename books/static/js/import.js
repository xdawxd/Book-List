
var checkbox = {
    checkedBooks: {},
    ifChecked: function(checkbox){
        let bookData = checkbox.parentElement.dataset.book;

        if (checkbox.checked){
            checkbox.parentElement.dataset.action = 'added';
        }
        else {
            checkbox.parentElement.dataset.action = 'not-added';
        }

        let bookAction = checkbox.parentElement.dataset.action;

        this.checkedBooks[bookData] = bookAction;

        console.log(this.checkedBooks); // for debug
    }

}

var importFormConfirm = document.getElementById('ImportFormConfirm');

importFormConfirm.addEventListener('submit', function(e){
    e.preventDefault();

    const url = '/api/import-book/'
    const csrftoken = this.getElementsByTagName('input')[0].value;


    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(checkbox.checkedBooks),
    })
    .then(res => res.json())
    .then(console.log)
    .catch(console.log)
});