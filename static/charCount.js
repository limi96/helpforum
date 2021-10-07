var titleId = document.currentScript.getAttribute('titleArea');
var titleDisplay = document.currentScript.getAttribute('titleDisplay');

const titleMin = parseInt(document.currentScript.getAttribute('titleMin')) 
const titleMax = parseInt(document.currentScript.getAttribute('titleMax'))

document.getElementById(titleId).addEventListener('keyup', function () {
    var words = this.value;
    var errorText = "";
    var line = " ------ ";

    charLength = words.length;

    if (charLength < titleMin) { errorText = line + "Required to be at least " + titleMin + " characters long! ";}
    
    else if (charLength > titleMax) { errorText = line + "Too many characters! ";}

    document.getElementById(titleDisplay).innerText = charLength + "/" + titleMax +" characters " + errorText;
});