$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2018-10-29',
            PR_Created: 4,
            PR_Assigned: null
        }, {
            period: '2018-10-30',
            PR_Created: 3,
            PR_Assigned: 1
        }, {
            period: '2018-10-31',
            PR_Created: 3,
            PR_Assigned: null
        }, {
            period: '2018-11-01',
            PR_Created: 5,
            PR_Assigned: 2
        }, {
            period: '2018-11-02',
            PR_Created: 4,
            PR_Assigned: 1
        }, {
            period: '2018-11-05',
            PR_Created: 4,
            PR_Assigned: 2
        }, {
            period: '2018-11-06',
            PR_Created: 3,
            PR_Assigned: 1
        }, {
            period: '2018-11-07',
            PR_Created: 4,
            PR_Assigned: null
        }, {
            period: '2018-11-08',
            PR_Created: 2,
            PR_Assigned: null
        }, {
            period: '2018-11-09',
            PR_Created: 3,
            PR_Assigned: 1
        }],
        xkey: 'period',
        ykeys: ['PR_Created', 'PR_Assigned'],
        labels: ['PR_Created', 'PR_Assigned'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });


    Morris.Area({
        element: 'morris-area-chart2',
        data: [{
            PRNumber: '8251',
            LinesOfCode: 14
        }, {
            PRNumber: '8252',
            LinesOfCode: 150
        }, {
            PRNumber: '8253',
            LinesOfCode: 12
        }, {
            PRNumber: '8254',
            LinesOfCode: 62
        }, {
            PRNumber: '8255',
            LinesOfCode: 72
        }, {
            PRNumber: '8256',
            LinesOfCode: 18
        }, {
            PRNumber: '8257',
            LinesOfCode: 30
        }, {
            PRNumber: '8258',
            LinesOfCode: 4
        }, {
            PRNumber: '8259',
            LinesOfCode: 18
        }, {
            PRNumber: '8260',
            LinesOfCode: 90
        }],
        xkey: 'PRNumber',
        ykeys: ['LinesOfCode'],
        labels: ['LinesOfCode'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });


    Morris.Area({
        element: 'morris-area-chart3',
        data: [{
            period: '222',
            SprintCompletionPercent: 80,
            PR_Assigned: null
        }, {
            period: '223',
            SprintCompletionPercent: 60,
            PR_Assigned: 1
        }, {
            period: '224',
            SprintCompletionPercent: 65,
            PR_Assigned: 1
        }, {
            period: '225',
            SprintCompletionPercent: 26,
            PR_Assigned: 1
        }, {
            period: '226',
            SprintCompletionPercent: 67,
            PR_Assigned: 1
        }, {
            period: '227',
            SprintCompletionPercent: 80,
            PR_Assigned: 1
        }, {
            period: '228',
            SprintCompletionPercent: 95,
            PR_Assigned: 1
        }, {
            period: '229',
            SprintCompletionPercent: 76,
            PR_Assigned: 1
        }, {
            period: '230',
            SprintCompletionPercent: 77,
            PR_Assigned: 1
        }, {
            period: '231',
            SprintCompletionPercent: 45,
            PR_Assigned: 1
        }, {
            period: '232',
            SprintCompletionPercent: 80,
            PR_Assigned: 1
        }, {
            period: '233',
            SprintCompletionPercent: 88,
            PR_Assigned: 1
        }, {
            period: '234',
            SprintCompletionPercent: 81,
            PR_Assigned: 1
        }, {
            period: '235',
            SprintCompletionPercent: 95,
            PR_Assigned: 1
        }, {
            period: '236',
            SprintCompletionPercent: 90,
            PR_Assigned: 1
        }, {
            period: '237',
            SprintCompletionPercent: 70,
            PR_Assigned: 1
        }, {
            period: '238',
            SprintCompletionPercent: 78,
            PR_Assigned: 1
        }, {
            period: '239',
            SprintCompletionPercent: 70,
            PR_Assigned: 1
        }, {
            period: '240',
            SprintCompletionPercent: 60,
            PR_Assigned: null
        }, {
            period: '241',
            SprintCompletionPercent: 46,
            PR_Assigned: 2
        }, {
            period: '242',
            SprintCompletionPercent: 80,
            PR_Assigned: 1
        }, {
            period: '243',
            SprintCompletionPercent: 80,
            PR_Assigned: 2
        }, {
            period: '244',
            SprintCompletionPercent: 86,
            PR_Assigned: 1
        }, {
            period: '245',
            SprintCompletionPercent: 92,
            PR_Assigned: null
        }, {
            period: '246',
            SprintCompletionPercent: 71,
            PR_Assigned: null
        }, {
            period: '247',
            SprintCompletionPercent: 85,
            PR_Assigned: 1
        }],
        xkey: 'period',
        ykeys: ['SprintCompletionPercent'],
        labels: ['SprintCompletionPercent'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Download Sales",
            value: 12
        }, {
            label: "In-Store Sales",
            value: 30
        }, {
            label: "Mail-Order Sales",
            value: 20
        }],
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            y: '2006',
            a: 100,
            b: 90
        }, {
            y: '2007',
            a: 75,
            b: 65
        }, {
            y: '2008',
            a: 50,
            b: 40
        }, {
            y: '2009',
            a: 75,
            b: 65
        }, {
            y: '2010',
            a: 50,
            b: 40
        }, {
            y: '2011',
            a: 75,
            b: 65
        }, {
            y: '2012',
            a: 100,
            b: 90
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });
    
});
