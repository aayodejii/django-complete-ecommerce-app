// get necessary elements
const quantity = document.querySelectorAll('#orderQty');
const price = document.querySelectorAll('#orderPrice');
const totalPrice = document.querySelectorAll('#totalPrice');
const allTotal = document.querySelector('#allTotal');
const editQty = document.querySelector('#updateQty');
const editForm = document.querySelector('#updateQ');


const body = document.querySelector('body');

console.log(editQty);




// removes the selected item when the click event if fired
body.addEventListener('click', removeItem);
function removeItem(e) {
  if (e.target.classList.contains('remove')) {
    console.log(e.target);
    var reply = confirm('Are you sure?');
    if (reply == true) {
    } else {
      e.preventDefault();
    }
  }
}




//calculate the total price for unit(s) bought

// for (let i = 0; i < quantity.length; i++) {
//   const calc = parseInt(quantity[i].innerText) * parseInt(price[i].innerText);
//   // const calc = parseInt(quantity[i].innerText) * parseInt(price[i].innerText);
//   totalPrice[i].innerText = calc;
// }

// //calculate the sum total of all purchases

// let tCalc = 0;
// for (let i = 0; i < totalPrice.length; i++) {
//   tCalc = parseInt(tCalc) + parseInt(totalPrice[i].innerText);
//   allTotal.innerText = tCalc;
// }




// editQty.addEventListener('blur', updateQty);
// function updateQty(e) {
//   // if (e.target.classList.contains('container')) {
//     editForm.submit();
//   console.log('Yes');
// // }
// }