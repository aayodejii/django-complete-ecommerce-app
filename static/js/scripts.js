const msg = document.querySelector('#message');
const item = document.querySelector('#cartItem');



if (item.innerText ==='0'){
item.style.display ='none';
}

if (msg !== null){
  setTimeout(hideMsg, 6000);

}


function hideMsg() {
  msg.style.display ='none';
}




// this section is responsible for styling list items, find how to limit this

// const liOdd = document.querySelectorAll('li:nth-child(odd)');
// const liEven = document.querySelectorAll('li:nth-child(even)');

// for (let i = 0;  i < liEven.length; i++) {
// 	liEven[i].style.background = 'white' ;
// 	}

// for (let i = 0;  i < liOdd.length; i++) {
// 	liOdd[i].style.background = 'whitesmoke' ;
// 	}




// this section is responsible adding order to cart

// function addToLocal(order) {
// 	let orders;
// 	if(localStorage.getItem('orders') === null) {
// 		orders = [];
// 	} else {
// 		orders = JSON.parse(localStorage.getItem('orders'));
// 	}
// 	orders.push(order);
// 	localStorage.setItem('orders', JSON.stringify(orders));
// }

// console.log(product.innerText);
