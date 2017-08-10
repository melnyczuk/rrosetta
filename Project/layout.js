json = 'apocalypse'
loadJSON("citation_jsons/" + json + ".json");

function loadJSON(_path) {
    console.log('0');
    var request = new XMLHttpRequest();
    request.open("GET", _path, true);
    request.onload = function() {
        console.log('0');
        if (request.status >= 200 && request.status < 400) {
            var data = JSON.parse(request.responseText);
            for (var key in data) {
                if (key === 'img') {
                    for (var img in data['img']) {
                        //if (data['img'][img] != false) {
                        addImage(data['img'][img]['src'], img);
                        //}
                    }
                }
                if (key === 'txt') {
                    var c = 0;
                    for (var p in data['txt']) {
                        if (data['txt'][p] !== false && data['txt'][p]['quotes'] !== false) {
                            addText(data['txt'][p]['quotes'], p);
                            c++;
                            // } else if (data['txt'][p] !== false) {
                            //     addText(data['txt'][p]['text'], p);
                        }
                    }
                    if (c === 0) {
                        for (var p in data['txt']) {
                            addText(data['txt'][p]['text'], p);
                        }
                    }
                }
            }
        }
    };
    request.onerror = function() {
        console.log('nope');
    };
    request.send();
};

function shuffle(elems) {
    // https://j11y.io/snippets/shuffling-the-dom/

    // allElems = (function() {
    //     var ret = [],
    //         l = elems.length;
    //     while (l--) { ret[ret.length] = elems[l]; }
    //     return ret;
    // })();

    // var shuffled = (function() {
    //         var l = allElems.length,
    //             ret = [];
    //         while (l--) {
    //             var random = Math.floor(Math.random() * allElems.length),
    //                 randEl = allElems[random].cloneNode(true);
    //             allElems.splice(random, 1);
    //             ret[ret.length] = randEl;
    //         }
    //         return ret;
    //     })(),
    //     l = elems.length;

    // while (l--) {
    //     elems[l].parentNode.insertBefore(shuffled[l], elems[l].nextSibling);
    //     elems[l].parentNode.removeChild(elems[l]);
    // }
}

function addLink(_href, _link) {
    var newA = document.createElement('a');
    newA.href = _href;
    newA.text = _link;
    document.body.appendChild(newA);
    document.body.appendChild(document.createElement('br'));
}

function addImage(_src, _name) {
    var newImg = document.createElement('img');
    newImg.src = _src;
    newImg.alt = _name;
    newImg.className = 'shuffle';
    document.body.appendChild(newImg);
    document.body.appendChild(document.createElement('br'));
}

function addText(_text, _name) {
    var newText = document.createElement('p');
    newText.innerText = _text;
    newText.alt = _name;
    newText.className = 'shuffle';
    document.body.appendChild(newText);
    document.body.appendChild(document.createElement('br'));
}