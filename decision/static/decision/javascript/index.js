var token = document.getElementsByClassName('token')[0]
var admin = document.getElementsByClassName('admin')[0]
var voteInput = document.getElementById('activity-token')
var adminInput = document.getElementById('admin-token')
var activityTokenLink = document.getElementById('activity-token-link')
var adminTokenLink = document.getElementById('admin-token-link')
var voteBtn = document.getElementById('vote-btn');
var adminBtn = document.getElementById('admin-btn')
var glass = document.getElementsByClassName('glass')[0]

voteInput.addEventListener('input', function(e){
  activityTokenLink.setAttribute('href', `/show/${e.target.value}`)
})

adminInput.addEventListener('input', function(e){
  adminTokenLink.setAttribute('action', `/admin/${e.target.value}`)
})


voteBtn.addEventListener('click', function(e){
  e.preventDefault();
  // show glass
  glass.classList.remove('hidden')
  console.log(token)
  token.classList.remove('hidden')
})

adminBtn.addEventListener('click', function(e){
  e.preventDefault();
  // show glass
  glass.classList.remove('hidden')
  console.log(token)
  admin.classList.remove('hidden')
})



glass.addEventListener('click', function(e){
  this.classList.add('hidden');
  token.classList.add('hidden')
  admin.classList.add('hidden')
})