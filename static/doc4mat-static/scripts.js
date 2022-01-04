const textArea = document.getElementById('doc'),
     bold = document.getElementById('docBold'),
     italic = document.getElementById('docItalic'),
     st = document.getElementById('docDelete'),
     paragraph = document.getElementById('docParagraph'),
     heading = document.getElementById('docHeading');
console.log(window.document.getSelection());


textArea.addEventListener('select', format);
// 
document.querySelector('body').addEventListener('click', function(e){
console.log(e.target);
alert(document.textArea.getSelection());
})

function selection(){
    if (document.selection)
           return document.selection.createRange().text;;
    }
selection();

function format(e){
document.getElementById('output').innerHTML= document.getElementById('doc').value
console.log(textArea.value)
    // alert(window.getSelection());
    // document.getElementById('doc').select ='<b>Yess</b>';


  
  

};








