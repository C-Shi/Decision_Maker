var addOptionBtn = document.getElementById('add-option');

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