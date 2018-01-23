var acc = document.getElementsByClassName("accordion");
    for (var i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.maxHeight){
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
            for (var k = 0; k < acc.length; k++) {
                if ((acc[k] != this) && (acc[k].nextElementSibling.style.maxHeight)) {
                    acc[k].classList.toggle("active")
                    acc[k].nextElementSibling.style.maxHeight = null;
                }
            }
        });
    }
