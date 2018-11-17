var model = {
    Repair_Point: [
        [56.444885, 84.925622],
        [56.343107, 84.852134],
        [66.343107, 94.852134]],
    StartAdress: undefined,
    DestinationAdress: undefined,
    addlisteners: function () {
        // set listeners for elements //
    },
    setRepairPoint(coords) {
        try {
            this.Repair_Point.push(coords);
        } catch (e) {
            alert(e, 'Write repair points mistake');
        }
    },
    setStartAdress(value) {
        try {
            this.StartAdress = value;
        } catch (e) {
            alert(e, 'Write StartAdress mistake');
        }
    },
    setDestinationAdress() {
        try {
            this.DestinationAdress = value;
        } catch (e) {
            alert(e, 'Write DestinationAdress mistake');
        }
    },
    getRepairPoint() {
        return this.Repair_Point;
    },
}
var App = {
    YandexMap: undefined,
    route: undefined,
    init: function () {
        ymaps.route([
            model.StartAdress,
            model.DestinationAdress
        ]).then(function (route) {
            App.route = route;
            App.YandexMap.geoObjects.add(App.route);
            var points = App.route.getWayPoints(),
                lastPoint = points.getLength() - 1;
            points.options.set('preset', 'islands#redStretchyIcon');
            points.get(0).properties.set('iconContent', 'Точка отправления');
            points.get(lastPoint).properties.set('iconContent', 'Точка прибытия');
            var way, segments;
        }, function (error) {
            alert('Возникла ошибка: ' + error.message);
        });
        App.YandexMap = new ymaps.Map('map', {
            center: [55.750625, 37.626],
            zoom: 7,
        });
    },
    
    getRoute: function () { return this.route; },
    getYandexMap: function () { return this.YandexMap; }
}
// should be by click on button.



