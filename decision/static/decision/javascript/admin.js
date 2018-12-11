var addOptionBtn = document.getElementById('add-option');
var toDeleteConfirm = document.getElementById('to-delete-confirm');
var glass = document.getElementsByClassName('glass')[0];
var deleteConfirmForm = document.getElementsByClassName('delete')[0];


addOptionBtn.addEventListener('click', function(e){
    e.preventDefault();
    // create input div
    var newOptionDiv = document.createElement('div');
    newOptionDiv.classList.add('pure-control-group');
    // creat input label
    var newOptionLabel = document.createElement('label');
    newOptionLabel.textContent = 'Option: ';
    // create input input
    var newOptionInput = document.createElement('input');
    newOptionInput.setAttribute('name', 'option');
    newOptionInput.setAttribute('type', 'text');
    newOptionInput.setAttribute('placeholder', 'Option');
    // append
    newOptionDiv.appendChild(newOptionLabel);
    newOptionDiv.appendChild(newOptionInput);

    document.getElementsByClassName('options')[0].appendChild(newOptionDiv)
})

document.body.addEventListener('click', function(e){
    if (e.target == glass || e.target == document.getElementsByClassName('back-btn')[0]){
        glass.classList.add('hidden');
        deleteConfirmForm.classList.add('hidden')
    }
})

toDeleteConfirm.addEventListener('click', function(e){
    e.preventDefault();
    console.log(deleteConfirmForm)
    glass.classList.remove('hidden')
    deleteConfirmForm.classList.remove('hidden');
})