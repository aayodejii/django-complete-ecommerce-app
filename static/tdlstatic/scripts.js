// alert('add something');


const inputForm =  document.querySelector('#task-form');
const taskList = document.querySelector('.list-group');
const clearBtn = document.querySelector('.btn-success');
const filter = document.querySelector('#filter-input');
const taskInput = document.querySelector('#task-input');

//load events listeners
console.log(taskList);
loadEventListeners();

function loadEventListeners(){
    //add task
    inputForm.addEventListener('submit', addTask);
}



function addTask(e){
    if(taskInput.value === '') {
        alert('add something');
    }
    const li = document.createElement('li');
    li.className ='list-group-item';
    li.appendChild(document.createTextNode(taskInput.value));
    const link = document.createElement('a');
    link.className = 'you you';
    link.innerHTML = '<i class ="fa fa-remove"></li>';
    li.appendChild(link);
    taskList.appendChild(li);
    taskInput.value = '';
    console.log(taskInput);

    e.preventDefault();



}