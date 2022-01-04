const addToggler = document.querySelector('#addToggler');
const productForm = document.querySelector('#productForm');
const product = document.querySelectorAll('#rowItem');
const body = document.querySelector('body');
const btn = document.getElementById('formBtn');
console.log(productForm);
console.log(btn);

loadEventListeners();

function loadEventListeners() {
  addToggler.addEventListener('click', addProduct);
  body.addEventListener('click', doAction);
  // body.addEventListener('click', update);
}

function addProduct(e) {
  if (e.target.classList.contains('visibility')) {
    if (productForm.style.display === 'block') {
      productForm.style.display = 'none';
      addToggler.innerText = 'Show Form';
    } else if (productForm.style.display === 'none') {
      productForm.style.display = 'block';
      addToggler.innerText = 'Hide Form';

    }
  }
}


function doAction(e) {
  const xhr = new XMLHttpRequest();

  if (e.target.classList.contains('delete')) {
    e.preventDefault();
    const productText =
    e.target.parentNode.parentNode.parentNode.firstElementChild.innerText;
    if (confirm(`Are you sure you want to remove ${productText} from stock?`)) {
    
      xhr.open('DELETE', `/admin/product/${productText}/delete`, true);

      xhr.onload = function() {
        if (this.status === 200) {
          console.log(this.status);
          e.target.parentNode.parentNode.parentNode.remove();
        } else {
          console.log('nooo'); //catch err here
        }
      };

      xhr.send();
    }
  }
}
//   } else if (e.target.classList.contains('edit')) {
//     e.preventDefault();
//     const productText =
//     e.target.parentNode.parentNode.parentNode.firstElementChild.innerText;
    
//       xhr.open('GET', `/admin/product/${productText}/edit`, true);

//       xhr.onload = function() {
//         if (this.status === 200) {
//           btn.classList.add('submit');
//           console.log(btn);
//          const response = JSON.parse(this.responseText);



//           response.forEach(function(product){
//           console.log(product.picture);
  
//           document.getElementById('id_name').value = product.name;
//           document.getElementById('id_price').value = product.price;
//           document.getElementById('id_quantity').value = product.quantity;
//           document.getElementById('id_percent_off').value = product.percent_off;
         
          
//           document.getElementById('id_description').value = product.desc;
//           document.getElementById('id_brand').value = product.brand;
//           document.getElementById('id_color').value = product.color;
//           document.getElementById('id_size').value = product.size;
//         });
//           // picture =  document.getElementById('id_picture').;
//           // picture = Array.from(picture);
//           // console.log(picture)
       
//           // document.getElementById('id_picture').nodeValues = product.picture;
      
//           productForm.style.display = 'block';
//           addToggler.innerText = 'Hide Form';
//           // productForm.action = `/admin/phone/view-products/`
//           // productForm.action = `/admin/product/${productText}/edit`

          

          
      

//         } else {
//           console.log('nooo'); //catch err here
//           // productForm.action = `/admin/product/${productText}/edit`
//           // productForm.submit();

//         }
//       };

//       xhr.send();

//   }
// }


// function update(e) {
//   console.log("TESTTTTTTTTTTTTTTTTTTTTTTTTTT")

//   if (e.target.classList.contains('submit')) {
//     e.preventDefault();
//     // const productText =
//     // e.target.parentNode.parentNode.parentNode.firstElementChild.innerText;
//   const xhr = new XMLHttpRequest();

    
//       // xhr.open('DELETE', `/admin/product/${productText}/delete`, true);
//       xhr.open('POST', `admin/phone/view-products/edit/`, true);

//       xhr.onload = function() {
//         if (this.status === 200) {
//           console.log(this.status);
//           console.log("WORKED");
//           // productForm.action = `/admin/product/${productText}/edit`
//           productForm.submit();

//           // e.target.parentNode.parentNode.parentNode.remove();
//         } else {
//           console.log('nooo update'); //catch err here
//         }
//       };

//       xhr.send();
//     }
//   }