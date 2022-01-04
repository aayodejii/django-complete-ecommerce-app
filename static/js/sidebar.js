const subMenu = document.querySelector('#subMenu');
document.querySelector('body').addEventListener('click', toggle);

        console.log(subMenu);

function toggle(e){
    if (e.target.classList.contains('menu')){
        // console.log(e.target);
        subMenu.style.display='block';

    }
}