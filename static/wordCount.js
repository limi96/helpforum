var textId = document.currentScript.getAttribute('textArea');
var textDisplay = document.currentScript.getAttribute('display');

const min = parseInt(document.currentScript.getAttribute('min')) 
const max = parseInt(document.currentScript.getAttribute('max'))

document.getElementById(textId).addEventListener('keyup', function () {
    var words = this.value;
    var errorText = "";
    var line = " ------ ";
    
    count = words.trim().replace(/\s/g, ' ').split(' ').length;
    charLength = words.length;
    
    if (count == 1 && charLength == 0) {count = 0; }

    if (count < min) { errorText = line + "Required to have at least " + min + " words! ";}
    
    else if (count > max) {errorText = line + "Too many words! ";}

    document.getElementById(textDisplay).innerText = count + "/" + max +" words " + errorText;
});