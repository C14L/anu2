/**
 * Simple autocomplete for input[type=text] elements.
**/

(function(){

  var ul = document.createElement('ul');
  ul.classList.add('autocomplete-dropdown');

  function removeOptionsList() {
    var elms = document.getElementsByClassName('autocomplete-dropdown');
    for (var i=0; i<elms.length; i++) {
      elms[i].parentNode.removeChild(elms[i]);
    }
  }

  function emptyOptionsList(ulElm) {
    while (ulElm.firstChild) ulElm.removeChild(ulElm.firstChild);
  }

  function showOptionsList(optsList, elm) {
    var parentElm = elm.parentNode;
    emptyOptionsList(ul);
    for (var i=0, len=optsList.length; i<len; i++) {
      var li = document.createElement('li');
      li.appendChild(document.createTextNode(optsList[i]));
      li.addEventListener('click', function(event){ elm.value = event.target.innerHTML; removeOptionsList(); });
      ul.appendChild(li);
    }
    parentElm.insertBefore(ul, elm.nextSibling);
  }

  function findAllAutocompleteInputs() {
    var inputElms = document.getElementsByTagName('input');
    var inputList = [];

    for (var i=0, len=inputElms.length; i<len; i++) {
      if (inputElms[i].hasAttribute('type') &&
          inputElms[i].getAttribute('type') == 'text' &&
          inputElms[i].hasAttribute('autocomplete-url')) {
        inputList.push(inputElms[i]);
      }
    }
    return inputList;
  }

  var elms = findAllAutocompleteInputs();

  for (var i=0; i<elms.length; i++) {
    var acUrl = event.target.getAttribute('autocomplete-url');
    var acQry = event.target.getAttribute('autocomplete-query') || 'q';

    elms[i].addEventListener('keyup', function(event) {
      if (event.target.value.length < 3) return;
      event.target.classList.add('autocomplete-loading');

      var req = new XMLHttpRequest();
      req.open('GET', acUrl + '?' + acQry + '=' + event.target.value);
      req.addEventListener('load', function(){ if (this.status == 200 && this.response != null) { showOptionsList(JSON.parse(this.response), event.target) }});
      req.addEventListener('loadend', function(){ event.target.classList.remove('autocomplete-loading') });
      req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      req.send();
    });
  }

})();
