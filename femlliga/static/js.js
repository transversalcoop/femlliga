function sanitize(s) { return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); }
function contains(a, b) { return a.indexOf(b) !== -1; }

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
            segments.push([index, index+part.length]);
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

