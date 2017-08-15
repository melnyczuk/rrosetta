json = 'interface';
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
                        addImage(data['img'][img]['src'], img);
                    }
                }
                if (key === 'txt') {
                    for (var p in data['txt']) {
                        if (data['txt'][p] !== false && data['txt'][p]['quotes'] !== false) {
                            addText(data['txt'][p]['quotes'], p);
                        } else if (data['txt'][p]['contains'] === true) {
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
    https: //j11y.io/snippets/shuffling-the-dom/

        allElems = (function() {
        var ret = [],
            l = elems.length;
        while (l--) { ret[ret.length] = elems[l]; }
        return ret;
    })();

    var shuffled = (function() {
            var l = allElems.length,
                ret = [];
            while (l--) {
                var random = Math.floor(Math.random() * allElems.length),
                    randEl = allElems[random].cloneNode(true);
                allElems.splice(random, 1);
                ret[ret.length] = randEl;
            }
            return ret;
        })(),
        l = elems.length;

    while (l--) {
        elems[l].parentNode.insertBefore(shuffled[l], elems[l].nextSibling);
        elems[l].parentNode.removeChild(elems[l]);
    }
}

function addLink(_href, _link) {
    var newA = document.createElement('a');
    newA.href = _href;
    newA.text = _link;
    document.body.appendChild(newA);
    document.body.appendChild(document.createElement('br'));
}

function addImage(_src, _name) {
    var img = document.createElement('img');
    img.src = _src;
    img.alt = _name;
    document.body.appendChild(img);
    document.body.appendChild(document.createElement('br'));
}

function addText(_text, _name) {
    var txt = document.createElement('p');
    txt.innerText = _text;
    txt.alt = _name;
    document.body.appendChild(txt);
    document.body.appendChild(document.createElement('br'));
}