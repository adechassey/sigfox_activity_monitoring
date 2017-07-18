window.onload = function() {
    // Variables
    var tracking = [];
    var time = [];
    var socket = io.connect('http://localhost:3000');

    socket.on('newMessage', function (newMessage) {
        //console.log(newMessage);
        tracking.push(newMessage.data);
        time.push(new Date(newMessage.time).toLocaleString());
        trackingChart.update();
    });

    //console.log(messages);

    for (var message of messages){
        tracking.push(message.data);
        time.push(new Date(message.time).toLocaleString());
    }

    if(typeof activity !== 'undefined'){
        var dailyWorkingHours = activity.work/(3600*1000); // working time in hours
        $('#dailyWorkingHours').text('Today: ' + dailyWorkingHours.toFixed(2) + " h");
    }

// Tracking Chart
    var tracking_id = $("#tracking");
    var data_tracking = {
        labels: time,
        datasets: [{
            label: "Work efficiency",
            backgroundColor: "rgba(63, 115, 211, 0.3)",
            borderColor: "rgba(63, 115, 211, 0.7)",
            pointBorderColor: "rgba(8, 90, 172, 0.7)",
            pointBackgroundColor: "rgba(8, 90, 103, 0.3)",
            pointHoverBackgroundColor: "#203691",
            pointHoverBorderColor: "rgba(255, 255, 255, 0.5)",
            pointHoverRadius: 8,
            pointBorderWidth: 5,
            data: tracking
        }]
    };

    trackingChart = new Chart(tracking_id, {
        type: 'line',
        data: data_tracking,
        options: {
            hover: {
                mode: 'nearest'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    },
                    ticks: {
                        maxTicksLimit: 20
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Efficiency (%)'
                    },
                    ticks: {
                     beginAtZero: true,
                     steps: 10,
                     stepValue: 5,
                     min: 0,
                     max: 100,
                     maxTicksLimit: 5
                     }
                }]
            }
        }
    });
}