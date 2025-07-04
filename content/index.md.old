---
title: "Today's Prayer"
date: 2022-01-28T07:00:37-05:00
draft: false
---
{{< the-date >}}  

{{< todays-verse >}}

{{< memory-verse >}}

{{< todays-country >}}

{{< prayer-timer >}}

{{< category-menu >}}  

{{< prayer-requests >}}

{{< todays-vov >}}

{{< todays-psalm >}}

<script>
    function showSelectedPrayer(request) {
        if (request != 'Select Prayer Category') {//then get the prayer category
            $('#selectedPrayer').text(request);
        } else {//the "Select Prayer Category" option was selected
            $('#selectedPrayer').text("Select a Prayer Category");
        }
    };

    Number.prototype.toHHMMSS = function () {
	var sec_num = parseInt(this, 10); // don't forget the second param
	var hours   = Math.floor(sec_num / 3600);
	var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
	var seconds = sec_num - (hours * 3600) - (minutes * 60);

	//set as string
        if (hours   < 10) {hours   = ""+hours;}
        if (minutes < 10) {minutes = ""+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}

        if(hours > 0){
            return hours+':'+minutes+':'+seconds;
        }else{
            return minutes+':'+seconds;
        }
    }

    var timer = 0;
    function showCount() {
        timer--;
        if (timer >= 0){
            // console.log(timer);
            document.getElementById("prayerTimer").innerHTML = "Time to Pray: " + timer.toHHMMSS();
            setTimeout(showCount, 1000); /* replicate wait 1 second */
        }
    }

    function startTimer() {
        var minutesToPray = document.querySelector('input[name="minutesToPray"]:checked').value;
        timer = 60 * minutesToPray;
        showCount();
    }

    function clearTimer() {
        timer = 0;
        document.getElementById("prayerTimer").innerHTML = "Prayer Time (Minutes)";
        //uncheck minutes radio buttons
        var minuteRadioButtons = document.getElementsByName("minutesToPray");
        for(var i=0;i<minuteRadioButtons.length;i++){
            minuteRadioButtons[i].checked = false;
        }
    }
</script>
