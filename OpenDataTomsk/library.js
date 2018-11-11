function CheckRepairPointsOnRoute(route, RepairPoints, YandexMap) {
    // try {
        for (var i = 0; i < RepairPoints.length; i++) {
            way = route.getPaths().get(0);
            segments = way.getSegments();
            for (var j = 0; j < segments.length; j++) {
                var prop = segments[j].properties.getAll();
                if (!EntryPointCheck(prop.boundedBy, RepairPoints[i])) {
                    addRectOnMap(YandexMap, prop.boundedBy);
                    addPointOnMap(YandexMap, RepairPoints[i]);
                }
            }
        }
    // } catch (e) {
    //     console.log(e, 'Дождись окончания загрузки');
    // }
}
function addRectOnMap(map, points) {
    var myRectangle = new ymaps.GeoObject({
        geometry: {
            type: "Rectangle",
            coordinates: points
        },
    });
    myRectangle.options.set(
        { fillColor: '#ef0404' }
    );
    map.geoObjects.add(myRectangle);
}
function addPointOnMap(map, point) {
    PointPint = new ymaps.GeoObject({
        // Описание геометрии.
        geometry: {
            type: "Point",
            coordinates: point
        },
        properties: {
            // Контент метки.
            iconContent: 'Ремонтные работы ',
            hintContent: 'Ведутся ремонтные работы'
        }
    }, {
            // Опции.
            // Иконка метки будет растягиваться под размер ее содержимого.
            preset: 'islands#blackStretchyIcon',
        });
    myMap.geoObjects.add(PointPint);
}
function EntryPointCheck(area, point) {
    if (point[0] > Math.min(area[0][0], area[1][0]) &&
        point[0] < Math.max(area[0][0], area[1][0]) &&
        point[1] > Math.min(area[0][1], area[1][1]) &&
        point[1] < Math.max(area[0][1], area[1][1])) {
        return true;
    }
    else {
        return false
    }
}

//  -------------------------  ЭТО ГЕОКОДЕР ОН преобразует строку в геоданные и в геообъект изи сделатть второй пункт

// Реализуем интерфейс IGeocodeProvider.
var randomPointProvider = {
    geocode: function (request, options) {
        var deferred = ymaps.vow.defer(),
            geoObjects = new ymaps.GeoObjectCollection(),
            results = options.results || 10;

        for (var i = 0; i < results; i++) {
            geoObjects.add(new ymaps.GeoObject({
                geometry: {
                    type: "Point",
                    coordinates: [(Math.random() - 0.5) * 180, (Math.random() - 0.5) * 360]
                },
                properties: {
                    name: request + ' ' + i,
                    description: request + '\'s description ' + i,
                    balloonContentBody: '<p>' + request + ' ' + i + '</p>'
                }
            }));
        }

        var response = {
            geoObjects: geoObjects, // Геообъекты поисковой выдачи.
            metaData: {
                geocoder: {
                    request: request, // Строка обработанного запроса.
                    found: results, // Количество найденных результатов.
                    results: results, // Количество результатов в ответе.
                    skip: options.skip || 0 // Количество пропущенных результатов.
                }
            }
        };

        setTimeout(function () {
            deferred.resolve(response);
        }, 0);

        return deferred.promise();
    }
}
// myGeocoder = ymaps.geocode("Москва", { provider: randomPointProvider });
// myGeocoder.then(
//     function (res) {
//         console.log(res.geoObjects);
//         // map.geoObjects.add(res.geoObjects);
//     },
//     function (err) {
//         // Обработка ошибки.
//     }
// );
