var checkBoxes = document.getElementsByClassName("importCheckBox")

for (let i = 0; i < checkBoxes.length; ++i){
    checkBoxes[i].addEventListener('change', function(){
        let bookId = this.dataset.book;
        let action = this.dataset.action;
        console.log('bookId: ', bookId, ' Action: ', action);
    })
}