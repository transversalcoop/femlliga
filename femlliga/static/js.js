function sanitize(s) { return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); }
function contains(a, b) { return a.indexOf(b) !== -1; }
function formatDateTime(s) { return new Date(s).toLocaleString(); }

function segmentsHaveOverlap(segments) {
    for (var i = 0; i < segments.length-1; i++) {
        var s1 = segments[i];
        var s2 = segments[i+1];
        if (s1[1] >= s2[0]) return true;
    }
    return false;
}

function joinSegments(segments) {
    var res = [];
    var i = 0;
    for (i = 0; i < segments.length; i++) {
        var s1 = segments[i];
        if (i < segments.length - 1) {
            var s2 = segments[i+1];
            if (s1[1] >= s2[0]) {
                res.push([s1[0], Math.max(s1[1], s2[1])]);
                i++;
            } else {
                res.push(s1);
            }
        } else {
            res.push(s1);
        }
    }
    return res;
}

function highlightSearch(nom, search) {
    const parts = sanitize(search).split(" ");
    var segments = [];
    for (var i = 0; i < parts.length; i++) {
        var part = parts[i];
        if (part.length > 0) {
            var index = sanitize(nom).indexOf(part);
            if (index !== -1) {
                segments.push([index, index+part.length]);
            }
        }
    }

    if (segments.length === 0) {
        return nom;
    }

    segments.sort(function(a, b) { return a[0]-b[0] })
    while (segmentsHaveOverlap(segments)) {
        segments = joinSegments(segments);
    }

    var res = "";
    var index = 0;
    for (var i = 0; i < segments.length; i++) {
        res += nom.slice(index, segments[i][0]);
        res += '<span class="highlight">';
        res += nom.slice(segments[i][0], segments[i][1]);
        res += '</span>';
        index = segments[i][1];
    }
    res += nom.slice(index);
    return res;
}

function addHttp(url) {
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        return "https://" + url;
    }
    return url;
}

function socialMediaUrl(baseUrl, value) {
    if (value.startsWith("http")) {
        return value;
    }
    return baseUrl + value;
}

function post(url, csrfToken, body) {
  return fetch(url, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "content-type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  }).then(response => response.json());
}

function get(url, csrfToken, body) {
  return fetch(url, {
    body: JSON.stringify(body),
    headers: {
      "content-type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  }).then(response => response.json());
}

function getJsonData() {
    return JSON.parse(document.getElementById('django-json-data').textContent);
}

var toastWrapper = document.getElementById("toastWrapper");

function showToast(message) {
    var el = document.createElement("div");
    el.setAttribute("class", "toast mb-2");
    el.setAttribute("role", "alert");
    el.setAttribute("aria-live", "assertive");
    el.setAttribute("aria-atomic", "true");
    var inner = document.createElement("div");
    inner.setAttribute("class", "toast-body");
    inner.innerHTML = message;
    el.appendChild(inner);
    toastWrapper.appendChild(el);
    var toast = new bootstrap.Toast(el);
    toast.show();
    setTimeout(() => {
        toast.hide();
        setTimeout(() => { el.remove() }, 1000);
    }, 5000);
}
