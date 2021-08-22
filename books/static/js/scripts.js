function ifImport(){
    const checkBoxes = new Map();
    for (let bookCheckBox of document.getElementsByName("importCheckBox")){
        checkBoxes.set(bookCheckBox, false);
    }

    for (let [key, value] of checkBoxes.entries()){
        value = !!key.checked;
    }
}