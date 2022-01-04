const testBtn = document
  .getElementById('button')
  .addEventListener('click', findMe);

const xhr = new XMLHttpRequest();

function findMe() {
  console.log(1);
  xhr.open('GET', `/test/`, true);

  xhr.onload = function() {
    console.log(2);

    if (this.status === 200) {
      console.log('Yesss');

      const result = JSON.parse(this.responseText);
      console.log(result);
      let output = '';
      result.forEach(function(category) {
        output += `<li> ${category.name} | ${category.desc} </li> `;
      });
      obj = document.getElementById('output').innerHTML = `<ul>${output}</ul>`;
    } else {
      console.log('Nooo');
    }
  };
  xhr.send();
}
