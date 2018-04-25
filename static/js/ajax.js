function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajaxDeferredNoContentType(url, data) {
    var that = this;
    this._csrftoken = getCookie("csrftoken");
    if (data) {
        return $.ajax({
            cache: false,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                }
            },
            url: url,
            type: "POST",
            processData: false,
            contentType: false,
            data: data
        });
    } else {
        return $.ajax({
            cache: false,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                }
            },
            url: url,
            type: "POST",
            processData: false,
            contentType: false
        });
    }
}

function ajaxDeferred(url, type, data, dataType) {
    var that = this;
    this._csrftoken = getCookie("csrftoken");
    if (type === "get") {
        if (dataType === "json") {
            return $.ajax({
                cache: false,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                    }
                },
                url: url,
                type: "GET",
                dataType: "json"
            });
        } else {
            return $.ajax({
                cache: false,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                    }
                },
                url: url,
                type: "GET"
            });
        }
    } else if (type === "post") {
        if (dataType === "json") {
            return $.ajax({
                cache: false,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                    }
                },
                url: url,
                type: "POST",
                data: data,
                dataType: "json"
            });
        } else {
            return $.ajax({
                cache: false,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                    }
                },
                url: url,
                type: "POST",
                data: data
            });
        }
    } else if (type === "put") {
        if (data) {
            return $.ajax({
                cache: false,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                    }
                },
                url: url,
                type: "PUT",
                data: data
            });
        } else {
            return $.ajax({
                cache: false,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", that._csrftoken);
                    }
                },
                url: url,
                type: "PUT"
            });
        }
    }
}
