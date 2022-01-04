const 
 body = document.querySelector('body'),
 product = document.getElementById('product'),
 rating = document.getElementById('rating'),
 star = document.createElement('i'),
 star_I = document.getElementById('starI'),
 star_II = document.getElementById('starII'),
 star_III = document.getElementById('starIII'),
 star_IV = document.getElementById('starIV'),
 star_V = document.getElementById('starV')

 b = document.getElementById('breadCrumb');

 ;

console.log(b);

cat = document.createElement('li');
cat.className = 'breadcrumb-item';
cat.innerHTML = '<a href="#">Fashion</a>';
b.appendChild(cat);
console.log(cat);



// star.className = 'far fa-star';


// rating.appendChild(star);


// this part is working I have not been able to figure out how
// to update page without reload
body.addEventListener('click', rateProduct);

function rateProduct(e){
    // console.log('worked');
     if (e.target.classList.contains('fa-star') || e.target.classList.contains('fa-star-half-alt') ) {
    console.log(e.target);

    const xhr = new XMLHttpRequest()
        title = e.target.title;
        console.log(e.target.parentElement.firstElementChild.innerText);
      

    xhr.open('POST',`/rating/${product.innerText}/${title}/`,true)
    xhr.onload = function(){
        if(this.status === 200){
            console.log(22222);
            window.history.go(); //using this to imitate refresh for now
        }
    }
    xhr.send();

    }

}



//even this part

// const wishlistBtn = document.getElementById('wishlist');

// console.log(wishlistBtn);

// wishlistBtn.addEventListener('click', addWish);

// function addWish(){
//     const xhr = new XMLHttpRequest;
//     xhr.open('POST', `/<str:customer>/<str:product>/</str>` , true);
//     xhr.onload = function(){
//         if (this.status === 200){

//         }
//     }
//     xhr.send()
// }