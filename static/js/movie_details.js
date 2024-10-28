document.addEventListener('DOMContentLoaded', function () {

    var toggleElement = document.querySelector('.cast-toggle');
    var indicatorElement = toggleElement.querySelector('.indicator');
    var collapseElement = document.getElementById('castList');

    collapseElement.addEventListener('show.bs.collapse', function () {
        indicatorElement.textContent = '[-]';
    });

    collapseElement.addEventListener('hide.bs.collapse', function () {
        indicatorElement.textContent = '[+]';
    });
});