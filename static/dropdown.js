var slider = document.getElementById('slider');

    noUiSlider.create(slider, {
        start: [1000, 1700],
        step: 100,
        connect: true,
        range: {
            'min': 0800,
            'max': 2000
        }
    });

    var slider = document.getElementById("slider");
    var timestart = document.getElementById("timestart");
    var timeend = document.getElementById("timeend");
    var timestart_text = document.getElementById("timestart-text");
    var timeend_text = document.getElementById("timeend-text");

    function twentyfourhour(time) {
        if (time < 1000) {
            return "0" + String(Math.round(time));
        } else {
            return String(Math.round(time));
        }
    }

    slider.noUiSlider.on('update', function(values, handle) {
        timestart.value = values[0];
        timeend.value = values[1];

        timestart_text.innerHTML = "Start time: " + (twentyfourhour(values[0]));
        timeend_text.innerHTML = "End time: " + (twentyfourhour(values[1]));
    });