const wishLink = document.querySelectorAll('#wishLink');
const body = document.querySelector('body');

console.log(wishLink);

body.addEventListener('click', removeWish);

function removeWish(e){
    const customer = document.getElementById('customerEmail').innerText;

    const xhr = new XMLHttpRequest;
    if (e.target.classList.contains('remove')) {
        e.preventDefault();
    const product = e.target.parentElement.previousElementSibling.firstElementChild.innerText;
// console.log(e.target.parentElement.previousElementSibling.firstElementChild);
console.log(e.target);

    xhr.open('POST', `/remove-wish/${product}/${customer}/` , true);
    xhr.onload = function(){
        if (this.status === 200){
            e.target.offsetParent.remove();
        }
    }
    xhr.send()
}
}