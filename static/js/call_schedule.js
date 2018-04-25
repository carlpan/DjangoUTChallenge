
$('#scheduleCallModal').on('shown.bs.modal', function() {
    dateTimePicker();
});

$('#addSingleTimeModal').on('shown.bs.modal', function(){
    dateTimePicker();
});

$(document.body).on("click", "#sendConferenceCallSchedulerForm", function() {
    var url = urlList.callScheduleUrl;
    isConferenceCallSchedulerFormValid(url);
});

$(document.body).on("click", "#sendConferenceCallSchedulerFormAddSingleTime", function() {
    var url = urlList.addSingleTimeSlotUrl;
    isConferenceCallAddSingleTimeFormValid(url);
});

$(document.body).on("click", ".accept-time-slot-button", function() {
    var url = urlList.acceptRemoveTimeSlotUrl,
        divId = $(this);
    acceptCallSchedule(url, divId);
});

$(document.body).on("click", ".remove-time-slot-button", function() {
    var url = urlList.acceptRemoveTimeSlotUrl,
        divId = $(this);
    removeSingleCallSchedule(url, divId);
});

function isConferenceCallSchedulerFormValid(url) {
    showLoading();
    var data = {};
    var form_id = "#conferenceCallSchedulerForm",
        modal_id = "#scheduleCallModal";
    $(form_id).serializeArray().map(function(x) {
        if (x.value != "") {
            data[x.name] = x.value;
        }
    });

    if (Object.keys(data).length != 6) {
        showConferenceCallSchedulerFormAlert("alertConferenceCallSchedulerForm");
        hideLoading();
        return;
    }

    data['identifier'] = $('#callScheduleIdentifier').val();
    $(modal_id).modal('hide');
    ajaxDeferred(url, "post", data)
        .done(function(response) {
            setTimeout(function() {
                $("#callSchedule").empty();
                $(".xdsoft_datetimepicker").remove();
                $("#callSchedule").html(response);
                hideLoading();
            }, 500);
        });
}

function isConferenceCallAddSingleTimeFormValid(url) {
    showLoading();
    var data = {};
    var form_id = "#conferenceCallSchedulerFormAddSingleTime",
        modal_id = "#addSingleTimeModal";
    $(form_id).serializeArray().map(function(x) {
        if (x.value != "") {
            data[x.name] = x.value;
        }
    });

    if (Object.keys(data).length != 2) {
        showConferenceCallSchedulerFormAlert("alertSingleConferenceCallSchedulerForm");
        hideLoading();
        return;
    }

    data['identifier'] = $('#callScheduleIdentifier').val();
    $(modal_id).modal('hide');
    ajaxDeferred(url, "post", data)
        .done(function(response) {
            setTimeout(function() {
                $("#callSchedule").empty();
                $(".xdsoft_datetimepicker").remove();
                $("#callSchedule").html(response);
                hideLoading();
            }, 500);
        });
}

function acceptCallSchedule(url, divId) {
    var data = {
        "identifier": $(divId).attr("data-identifier"),
        "order": $(divId).val(),
        "for_accept": 1
    };
    ajaxDeferred(url, "post", data)
        .done(function(response) {
            setTimeout(function() {
                $("#callSchedule").empty();
                $("#callSchedule").html(response);
            }, 500);
        });
}

function removeSingleCallSchedule(url, divId) {
    var data = {
        "identifier": $(divId).attr("data-identifier"),
        "order": $(divId).val(),
        "for_accept": 0
    };
    ajaxDeferred(url, "post", data)
        .done(function(response) {
            // $(divId).closest(".call-schedule").remove();
            $("#callSchedule").empty();
            $("#callSchedule").html(response);
        });
}


function showConferenceCallSchedulerFormAlert(divId) {
    $("#" + divId).show();
    setTimeout(function() {
        $("#" + divId).hide();
    }, 1000);
}


function dateTimePicker() {
    var startDate = new Date(new Date().getTime() + (24 * 60 * 60 * 1000));
    $(".date-time-picker").datetimepicker({
        step: 30,
        minDate: startDate,
        format: "m/d/Y H:i"
    });
}

function showLoading() {
    $(".bg_load").show();
    $(".wrapper").show();
}

function hideLoading() {
    $(".bg_load").hide();
    $(".wrapper").hide();
}