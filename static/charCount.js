var textId = document.currentScript.getAttribute('textArea');
var textDisplay = document.currentScript.getAttribute('display');

const min = parseInt(document.currentScript.getAttribute('min')) 
const max = parseInt(document.currentScript.getAttribute('max'))

document.getElementById(textId).addEventListener('keyup', function () {
    var words = this.value;
    var errorText = "";
    var line = " ------ ";

    charLength = words.length;

    if (charLength < min) { errorText = line + "Required to be at least " + min + " characters long! ";}
    
    else if (count > max) {errorText = line + "Too many characters! ";}

    document.getElementById(textDisplay).innerText = count + "/" + max +" characters " + errorText;
});