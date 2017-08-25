// var Three = require("lib/three.js");
// var cam, scene, renderer;


var zine = { pages: 10, canvas: [], width: 100 + "px", height: 500 + "px" };


loadJSON("./test.json");

function buildCanvas() {
    var page = document.createElement('canvas');
    page.width = zine.width;
    page.height = zine.height;
    zine.canvas.push(page);
};


// function init() {
//     scene = new Three.Scene();
//     scene.background = new Three.Color(0xFFFFFF);

//     cam = new THREE.PerspectiveCamera(35, zine.width / zine.height, 0.1, 10000);

//     renderer = new THREE.WebGLRenderer({ antialias: true });
//     renderer.setSize(window.innerWidth, window.innerHeight);
//     document.body.appendChild(renderer.domElement);
// };
//------------------------
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
                        if (data['img'][img]['photo']) {
                            //if (data['img'][img]['dimensions'][0] > 250 && data['img'][img]['dimensions'][1] > 250) {
                            addImage(data['img'][img]['src'], img);
                        }
                    }
                }
                if (key === 'txt') {
                    for (var p in data['txt']) {
                        if (data['txt'][p] !== false && data['txt'][p]['quotes'] !== false) {
                            addText(data['txt'][p]['quotes'], p);
                            // } else if (data['txt'][p]['contains'] === true) {
                            //     addText(data['txt'][p]['text'], p);
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
//------------------------
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
};
//------------------------
function addLink(_href, _link) {
    var newA = document.createElement('a');
    newA.href = _href;
    newA.text = _link;
    document.body.appendChild(newA);
    document.body.appendChild(document.createElement('br'));
};
//------------------------
function addImage(_src, _name) {
    var img = document.createElement('img');
    img.src = _src;
    img.alt = _name;
    document.body.appendChild(img);
    document.body.appendChild(document.createElement('br'));
};
//------------------------
function addText(_text, _name) {
    var txt = document.createElement('p');
    txt.innerText = _text;
    txt.alt = _name;
    document.body.appendChild(txt);
    document.body.appendChild(document.createElement('br'));
};
//------------------------