/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#id_date", {
        dateFormat: "d.m.Y",
        minDate: "today"
    });
    flatpickr("#id_time", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr:true,
        minTime: "15:00",
        maxTime: "20:00"
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Eventlistener to cancle buttons
    document.querySelectorAll('.cancel-btn').forEach(function (button) {
        button.addEventListener('click', function (event) {
            var reservationId = this.getAttribute('data-reservation-id');
            var reservationDate = this.getAttribute('data-reservation-date');
            var reservationTime = this.getAttribute('data-reservation-time');

            // Update modal content
            document.getElementById('reservationDate').textContent = reservationDate;
            document.getElementById('reservationTime').textContent = reservationTime;

            // Update confirm cancel link
            var confirmCancelLink = document.getElementById('confirmCancelLink');
            confirmCancelLink.href = "/cancel_reservation/" + reservationId + "/";

            //Show the modal
            var cancelModal = new bootstrap.Modal(document.getElementById('cancelConfirmationModal'));
            cancelModal.show();
        });
    });

});