

var JSONINPUT = '{ "name":"John", "surname":"   ", "diag":"Melanoma"}';


let dictionary = ['bcc', 'bkl', 'mel', 'nv']
let dropArea = document.getElementById('drop__area');

// dropArea.addEventListener('dragenter', handlerFunction, false)
// dropArea.addEventListener('dragleave', handlerFunction, false)
// dropArea.addEventListener('dragover', handlerFunction, false)
// dropArea.addEventListener('drop', handlerFunction, false)

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
})

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
};

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
})

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files

    handleFiles(files)
}


function previewFile(file) {
    let reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = function () {
        let img = document.createElement('img')
        img.src = reader.result
        var gallery = document.getElementById('gallery')
        while (gallery.firstChild) {
            gallery.removeChild(gallery.firstChild);
        }
        document.getElementById('gallery').appendChild(img)
    }
}
function handleFiles(files) {
    files = [...files]
    files.forEach(uploadFile)
    files.forEach(previewFile)
}
function pMaker(_text){
    var pBlock = document.createElement("p");
    pBlock.textContent = _text;
    return pBlock;
}
function showResult(data){
    var result = document.getElementById('result__area');
    while (result.firstChild) {
        result.removeChild(result.firstChild);
    }
    result.appendChild(pMaker('Name: ' + data.name));
    result.appendChild(pMaker('surname: ' + data.surname));
    result.appendChild(pMaker('Diagnoses: ' + data.diag));
}

function uploadFile(file) {
    var url = 'image-recog';
    var xhr = new XMLHttpRequest()
    var formData = new FormData()
    xhr.open('POST', url, true)

    xhr.addEventListener('readystatechange', function (e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.response);

            var response = JSON.parse(xhr.response);
            var predict_result = response["shape"];
            for (var i =0; i< predict_result[0].length; i++){
                if ( predict_result[0][i] == 1){
                    console.log(predict_result,dictionary[i]);
                }
            }
            // debug mode 
            // var result = document.getElementById('result__area');
            // result.innerHTML = xhr.response;

            document.getElementById('loader').style.display = 'none'; 
        }
        else if (xhr.readyState == 4 && xhr.status != 200) {
            console.log(xhr.response);
        }
    })

    formData.append('file', file)
    xhr.send(formData)
    document.getElementById('loader').style.display = 'block';
}
