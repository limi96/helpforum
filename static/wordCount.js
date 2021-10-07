var textId = document.currentScript.getAttribute('questionArea');
var textDisplay = document.currentScript.getAttribute('questionDisplay');

const questionMin = parseInt(document.currentScript.getAttribute('questionMin')) 
const questionMax = parseInt(document.currentScript.getAttribute('questionMax'))

document.getElementById(textId).addEventListener('keyup', function () {
    var words = this.value;
    var errorText = "";
    var line = " ------ ";
    
    count = words.trim().replace(/\s/g, ' ').split(' ').length;
    charLength = words.length;
    
    if (count == 1 && charLength == 0) {count = 0; }

    if (count < questionMin && charLength < 1500) { errorText = line + "Required to have at least " + questionMin + " words! ";}
    
    else if (count > questionMax) {errorText = line + "Too many words! ";}

    if (charLength >= 1500) {errorText = line + "Too many characters! Max 1500";}

    document.getElementById(textDisplay).innerText = count + "/" + questionMax +" words " + errorText;
});
