$(document).ready(function ()
{
    "use strict";

    var person = $('<div class="person"></div>');
    var adultTicketsCount = 0;
    var childTicketsCount = 0;
    var ticketPrice = 0;
    var promoTicketPrice = 0;
    var adultTicketPrice = 0;
    var childTicketPrice = 0;

    var geanre = '';
    var chosenMovie = '';
    var chosenCinema = '';
    var isPromo = false;

    $("#buy-tickets-button").jqxButton({ theme: 'metrodark', width: '100px', height: '25px', template: 'default', disabled: true });
    $('#buy-tickets-button').click(function ()
    {
        var rowindex = $('#movies-list-grid').jqxGrid('getselectedrowindex');
        var data = $('#movies-list-grid').jqxGrid('getrowdata', rowindex);
        isPromo = data.promo;
        chosenMovie = data.movie;
        chosenCinema = data.cinema;
        ticketPrice = data.price;
        adultTicketPrice = data.price;
        promoTicketPrice = Math.floor(data.price * 0.8);
        childTicketPrice = Math.round(data.price / 2);
        if (isPromo === true)
        {
            adultTicketPrice = promoTicketPrice;
        }
		document.body.style.overflow = "hidden";
        $('#buy-tickets-window').jqxWindow('open');
    });

    initializeFilterWidgets();
    var sourceMoviesList = {
        datatype: "json",
        datafields: [
               { name: 'movie', type: 'string' },
               { name: 'geanre', type: 'string' },
               { name: 'cinema', type: 'string' },
               { name: 'price', type: 'number' },
               { name: 'promo', type: 'bool' },
               { name: 'projectiondate', type: 'date' },
               { name: 'startsat', type: 'date' },
               { name: 'rating', type: 'string' }
        ],
        url: "data.php?reservation=movieslist"
    };
    var dataAdapterMoviesList = new $.jqx.dataAdapter(sourceMoviesList, {
        loadComplete: function (records)
        {
            var recordsLength = records.length;
            var geanreSource = [];
            var moviesSource = [];
            var cinemaSource = [];
            var timeInterval = ['12:00', '12:00'];
            for (var i = 0; i < recordsLength; i++)
            {
                if (!isInArray(records[i].geanre, geanreSource))
                {
                    geanreSource.push(records[i].geanre);
                }

                if (!isInArray(records[i].movie, moviesSource))
                {
                    moviesSource.push(records[i].movie);
                }

                if (!isInArray(records[i].cinema, cinemaSource))
                {
                    cinemaSource.push(records[i].cinema);
                }

                if (records[i].startsat < timeInterval[0])
                {
                    timeInterval[0] = records[i].startsat;
                } else if (records[i].startsat > timeInterval[1])
                {
                    timeInterval[1] = records[i].startsat;
                }
                timeInterval[0] = timeInterval[0].slice(0, -2) + "00";
                if (timeInterval[1] > timeInterval[1].slice(0, -2) + "00")
                {
                    timeInterval[1] = (parseInt(timeInterval[1].slice(0, -3), 10) + 1) + ":00";
                }
            }

            function isInArray(value, array)
            {
                return array.indexOf(value) > -1;
            }

            geanreSource.sort();
            $("#filter-geanre-combobox").jqxComboBox({ source: geanreSource });
            moviesSource.sort();
            $("#filter-movies-combobox").jqxComboBox({ source: moviesSource });
            cinemaSource.sort();
            $("#filter-cinema-combobox").jqxComboBox({ source: cinemaSource });
        }
    });

    $("#movies-list-grid").jqxGrid({
        width: '100%',
        source: dataAdapterMoviesList,
        sortable: true,
        pageable: true,
        columnsheight: 35,
        rowsheight: 35,
        localization: {
            emptydatastring: "No movies on this criteria"
        },
        theme: 'metrodark',
        autoheight: true,
        pagesize: 20,
        pagermode: "simple",
        ready: function ()
        {
            if ($(".grids-popover").length > 0) {
                $("#popover").jqxPopover({theme: 'metrodark', position: "right", offset: { left: -230, top: 0 }, title: "Movie image", showCloseButton: false, selector: ".grids-popover" });
                attachPopover();
            }
        },
        columns: [
            {
                text: 'Movie', datafield: 'movie', width: '30%',
                cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                {
                    var image = value.replace(/\s/g, '').toLowerCase() + '.png'
                    return '<div class="grids-popover" id="' + row + '" style="margin-left:5px; margin-top:10px; cursor: pointer;" data-image="' + image + '" data-image-name="' + value + '">' + value + ' <span class="glyphicon glyphicon-info-sign" style="color:lightblue"></span></div>';
                }
            },
            { text: 'Geanre', datafield: 'geanre', cellsformat: 'D', width: '10%' },
            { text: 'Cinema', datafield: 'cinema', width: '10%' },
            { text: 'Price', datafield: 'price', width: '8%', cellsalign: 'right', align: 'right' },
            { text: 'Promo', datafield: 'promo', width: '10%', columntype: 'checkbox', cellsalign: 'center', align: 'center' },
            { text: 'Date', datafield: 'projectiondate', width: '12%', cellsformat: 'd', cellsalign: 'right', align: 'right' },
            { text: 'Hour', datafield: 'startsat', width: '11%', cellsformat: 't', cellsalign: 'right', align: 'right' },
            {
                text: 'Rating', datafield: 'rating', width: '9%',
                createwidget: function (row, column, value, htmlElement)
                {
                    var rating = $("<div style='margin:3px 0px 0px 10px;'></div>");
                    $(htmlElement).append(rating);
                    rating.jqxRating({ itemWidth: 10, itemHeight: 10, width: 100, height: 10, count: 6, disabled: true, singleVote: true, value: value, theme: 'classic' });
                },
                initwidget: function (row, column, value, htmlElement)
                {
                }
            }]
    });

    $("#movies-list-grid").on('rowselect', function ()
    {
        $("#buy-tickets-button").jqxButton({ theme: 'metrodark', disabled: false });
    });

    $("#movies-list-grid").on('pagechanged', function ()
    {
        attachPopover();
    });

    function attachPopover()
    {
        $(".grids-popover").on("mouseenter", function ()
        {
            var id = $(this).attr('id');
            var image = $("#" + id).attr('data-image');
            var imageName = $("#" + id).attr('data-image-name');
            var img = '<img src="../../../images/' + image + '" style="margin-left:auto; margin-right:auto;" />';
            $("#movies").html(img);
            $("#popover").jqxPopover({ selector: "#" + id, title: imageName });
            $("#popover").jqxPopover("open");
        });
        $(".grids-popover").on("mouseleave", function ()
        {
            $("#popover").jqxPopover("close");
            $("#popover").jqxPopover({ selector: ".grids-popover" });
        });
    }

    var sourceReservedSeats = {
        datatype: "json",
        datafields: [
               { name: 'movie', type: 'string' },
               { name: 'geanre', type: 'string' }
        ],
        url: "data.php?reservation=seats"
    };
    var dataAdapterReservedSeats = new $.jqx.dataAdapter(sourceReservedSeats, {
        loadComplete: function (records)
        {
            var recordsLength = records.length;
            var seatNumber = 0;

            $('.seat').addClass("free");
            for (var i = 0; i < recordsLength; i++)
            {
                seatNumber = (records[i].row - 1) * 21 + records[i].seat;
                $('.seat:nth-of-type(' + seatNumber + ')').removeClass("free");
                $('.seat:nth-of-type(' + seatNumber + ')').addClass("occupied");
            }
        }
    });

    $('#buy-tickets-window').jqxWindow(
    {
        autoOpen: false,
        theme: 'metrodark',
        isModal: true,
		position: "center",
        resizable: false,
        height:530,
        width: 320,
        initContent: function ()
        {
            $("#buy-tickets-adult-numberinput").jqxNumberInput({ theme: 'metro', width: '50px', height: '20px', inputMode: 'simple', spinButtons: true, decimalDigits: 0, min: 0, max: 5 });
            $("#buy-tickets-children-numberinput").jqxNumberInput({ theme: 'metro', width: '50px', height: '20px', inputMode: 'simple', spinButtons: true, decimalDigits: 0, min: 0, max: 5 });
        }
    });

    $("#buy-tickets-window-button").jqxButton({ theme: 'metrodark', template: "default", width: "95%", height: "30px", disabled: true });
    $("#buy-tickets-window-button").on("click", function ()
    {
        $('#buy-tickets-window').jqxWindow("close");
        $('#buy-tickets-window-success').jqxWindow("open");

        setTimeout(function ()
        {
            $('#buy-tickets-window-success').jqxWindow("close");
        }, 1000);
    });

    $('#buy-tickets-window').on("open", function ()
    {

        $('.seat').removeClass("occupied");
        $('.seat').removeClass("free");
        $('.seat').find(".person").parent().css('background-color', 'white');
        $('.seat').find(".person").remove();


        $("#buy-tickets-adult-numberinput").jqxNumberInput("val", 0);
        $("#buy-tickets-children-numberinput").jqxNumberInput("val", 0);

        $("#window-label-movie").html("<b>" + chosenMovie + "</b>");
        $("#window-label-cinema").html("<b>" + chosenCinema + "</b>");
        $("#window-label-tickets").html("<b>0</b>+<b>0</b>");
        $("#window-label-peradult").html("<b>" + adultTicketPrice + "$</b>");
        $("#window-label-perchild").html("<b>" + childTicketPrice + "$</b>");
        $("#window-label-total").html("<b>0$</b>");

        if (isPromo)
        {
            $("#window-label-peradult").css({ color: "red" });
        }

        dataAdapterReservedSeats.dataBind();
  		document.body.style.overflow = "auto";
    });

    $("#buy-tickets-adult-numberinput").on('valueChanged', function (event)
    {
        var seats = findNewlyOccupiedSeats();
        var value = event.args.value - seats.adult;
        $('#adult-tickets .buy-tickets-placeholder').html("");
        if (value > 0)
        {
            if (value > 5)
            {
                value = 5;
            }
            for (var i = 0; i < value; i++)
            {
                $('#adult-tickets .buy-tickets-placeholder:nth-of-type(' + (i + 3) + ')').append(person.clone().addClass("adult"));
                $(".person").jqxDragDrop({
                    dropAction: 'default',
                    dropTarget: '.seat.free',
                    feedback: 'clone',
                    tolerance: 'intersect'
                });
            }
            $("#buy-tickets-window-button").jqxButton({ disabled: false });
        } else
        {
            if (childTicketsCount === 0)
            {
                $("#buy-tickets-window-button").jqxButton({ disabled: true });
            }
        }

        adultTicketsCount = value;
        changeValueLabels();
        var target = null;
        $('.person').on('dropTargetEnter', function (event)
        {
            $(event.args.target).css('background-color', 'yellow');
            target = $(event.args.target).attr('id');
        });
        $('.person').on('dropTargetLeave', function (event)
        {
            $(event.args.target).css('background-color', 'white');
        });
        $('.person').on('dragEnd', function (event)
        {
       //     $(event.args.target).css('background-color', 'white');
            $("#" + target).append($(this));
            $(this).css({ left: "0px", top: "0px" });
            $(this).width(18);
            $(this).height(18);
        });
        $('.person').on('dragStart', function ()
        {
            target = findFirstFreeSeat();
        });
    });

    $("#buy-tickets-children-numberinput").on('valueChanged', function (event)
    {
        var seats = findNewlyOccupiedSeats();
        var value = event.args.value - seats.child;
        $('#children-tickets .buy-tickets-placeholder').html("");
        if (value > 0)
        {
            if (value > 5)
            {
                value = 5;
            }

            for (var i = 0; i < value; i++)
            {
                $('#children-tickets .buy-tickets-placeholder:nth-of-type(' + (i + 3) + ')').append(person.clone().addClass("child"));
                $(".person").jqxDragDrop({
                    dropAction: 'default',
                    dropTarget: '.seat.free',
                    feedback: 'clone',
                    tolerance: 'intersect'
                });
            }
            $("#buy-tickets-window-button").jqxButton({ disabled: false });
        } else
        {
            if (adultTicketsCount === 0)
            {
                $("#buy-tickets-window-button").jqxButton({ disabled: true });
            }
        }

        childTicketsCount = value;
        changeValueLabels();
        var target = null;
        $('.person').on('dropTargetEnter', function (event)
        {
            $(event.args.target).css('background-color', 'yellow');
            target = $(event.args.target).attr('id');
        });
        $('.person').on('dropTargetLeave', function (event)
        {
            $(event.args.target).css('background-color', 'white');
        });
        $('.person').on('dragEnd', function (event)
        {
            $(event.args.target).css('background-color', 'white');
            $("#" + target).append($(this));
            $(this).css({ left: "0px", top: "0px" });
        });
        $('.person').on('dragStart', function ()
        {
            target = findFirstFreeSeat();
        });
    });

    function findNewlyOccupiedSeats()
    {
        var seats = {};

        var element = document.getElementById("seats");
        seats.child = element.getElementsByClassName('child').length;
        seats.adult = element.getElementsByClassName('adult').length;

        return seats;
    }

    function findFirstFreeSeat()
    {
        var firstFreeSeat;
        var element = document.getElementById("seats");
        var allSeats = element.getElementsByClassName('free');
        var allSeatsCount = allSeats.length;
        var i = 0;

        while ((i < allSeatsCount) && (allSeats[i].getElementsByClassName('person').length > 0))
        {
            i++;
        }

        firstFreeSeat = $(allSeats[i]).attr('id');

        return firstFreeSeat;
    }

    function changeValueLabels()
    {
        var total = adultTicketsCount * adultTicketPrice + childTicketsCount * childTicketPrice;
        $("#window-label-tickets").html("<b>" + adultTicketsCount + "</b>+<b>" + childTicketsCount + "</b>");
        $("#window-label-total").html("<b>" + total + "$</b>");
    }

    $('#buy-tickets-window-success').jqxWindow(
    {
        autoOpen: false,
        closeAnimationDuration: 1000,
        theme: 'metrodark',
        resizable: false,
        isModal: true,
        width: 320
    });

    $("#filter-geanre-combobox").on('change', function (event)
    {
        var emptyArgs = {};
        var args = event.args || emptyArgs;
        var item = args.item || emptyArgs;
        geanre = item.label || "";

        var sourceMoviesByGeanre = {
            datatype: "json",
            datafields: [
                   { name: 'movie', type: 'string' },
                   { name: 'image', type: 'string' },
                   { name: 'geanre', type: 'string' }
            ],
            url: "data.php?moviebygeanre=" + geanre
        };
        var dataAdapterMoviesByGeanre = new $.jqx.dataAdapter(sourceMoviesByGeanre, {
            loadComplete: function (records)
            {
                var recordsLength = records.length;
                var moviesSource = [];
                for (var i = 0; i < recordsLength; i++)
                {
                    if (!isInArray(records[i].movie, moviesSource))
                    {
                        moviesSource.push(records[i].movie);
                    }
                }

                function isInArray(value, array)
                {
                    return array.indexOf(value) > -1;
                }

                moviesSource.sort();
                $("#filter-movies-combobox").jqxComboBox({ source: moviesSource });
            }
        });

        dataAdapterMoviesByGeanre.dataBind();
    });

    function initializeFilterWidgets()
    {
        $("#filter-geanre-combobox").jqxComboBox({ theme: 'metrodark', width: '95%', height: '35px', autoDropDownHeight: true, placeHolder: "Select geanre ..." });
        $("#filter-movies-combobox").jqxComboBox({
            theme: 'metrodark',
            width: '95%',
            valueMember: 'movie',
            displayMember: 'movie',
            height: '35px',
            autoDropDownHeight: true,
            renderer: function (index, label, value)
            {
                var imgurl = '../../../images/' + label.replace(/\s/g, '').toLowerCase() + '.png';
                var img = '<img height="67" width="45" src="' + imgurl + '"/>';
                var table = '<table style="min-width: 150px;"><tr><td style="width: 55px;" rowspan="2">' + img + '</td><td><h5><i>Title</i></h5></td></tr><tr><td style="margin-top:0px; padding-top0px;">' + label + '</td></tr></table>';
                return table;
            },
            placeHolder: "Select movie ..."
        });
        $("#filter-cinema-combobox").jqxComboBox({ theme: 'metrodark', width: '95%', height: '35px', autoDropDownHeight: true, placeHolder: "Select cinema ..." });
        $("#filter-promo-checkbox").jqxCheckBox({ theme: 'metrodark', width: '95%', height: '35px' });
        $("#filter-date-dateinput").jqxDateTimeInput({ theme: 'metrodark', width: '95%', height: '35px' });
        $("#filter-price-rangeselector").jqxRangeSelector({
            theme: 'metrodark',
            width: '85%',
            height: '35px',
            min: 5,
            max: 15,
            minorTicksInterval: 1,
            majorTicksInterval: 1,
            labelsFormatFunction: function (value)
            {
                return "<span class='labels'>$" + value + "<span>";
            },
            labelsFormat: "c0",
            markersFormat: "c0",
            range: { from: 5, to: 15 }
        });
        $("#filter-filter-button").jqxButton({ theme: 'metrodark', width: '95%', height: '50px' });
        $("#filter-filter-remove-button").jqxButton({ theme: 'metrodark', width: '95%', height: '50px' });
    }

    $("#filter-filter-button").on('click', function ()
    {
        $('#movies-list-grid').jqxGrid('clearselection');
        $("#buy-tickets-button").jqxButton({ theme: 'metrodark', disabled: true });
        $("#movies-list-grid").jqxGrid('clearfilters');
        applyFilters();
    });

    $("#filter-filter-remove-button").on('click', function ()
    {
        $("#filter-geanre-combobox").jqxComboBox('val', '');
        $("#filter-geanre-combobox").trigger('change');
        $("#filter-movies-combobox").jqxComboBox('val', '');
        $("#filter-cinema-combobox").jqxComboBox('val', '');
        $("#filter-promo-checkbox").jqxCheckBox('val', false);
        $("#filter-price-rangeselector").jqxRangeSelector({ range: { from: 5, to: 15 } });
        $("#movies-list-grid").jqxGrid('clearfilters');
    });

    function applyFilters()
    {

        var filtergroupGeanre = new $.jqx.filter();
        var filtervalue = geanre;
        var datafield = 'geanre';
        var filtertype = 'stringfilter';
        var filter_or_operator = 1;
        var filtercondition = 'contains';
        var filterGeanre = filtergroupGeanre.createfilter(filtertype, filtervalue, filtercondition);
        filtergroupGeanre.addfilter(filter_or_operator, filterGeanre);
        $("#movies-list-grid").jqxGrid('addfilter', datafield, filtergroupGeanre);

        var filtergroupMovie = new $.jqx.filter();
        filtervalue = $("#filter-movies-combobox").jqxComboBox('val');
        datafield = 'movie';
        filtertype = 'stringfilter';
        filter_or_operator = 1;
        filtercondition = 'contains';
        var filterMovie = filtergroupMovie.createfilter(filtertype, filtervalue, filtercondition);
        filtergroupMovie.addfilter(filter_or_operator, filterMovie);
        $("#movies-list-grid").jqxGrid('addfilter', datafield, filtergroupMovie);

        var filtergroupCinema = new $.jqx.filter();
        filtervalue = $("#filter-cinema-combobox").jqxComboBox('val');
        datafield = 'cinema';
        filtertype = 'stringfilter';
        filter_or_operator = 1;
        filtercondition = 'contains';
        var filterCinema = filtergroupCinema.createfilter(filtertype, filtervalue, filtercondition);
        filtergroupCinema.addfilter(filter_or_operator, filterCinema);
        $("#movies-list-grid").jqxGrid('addfilter', datafield, filtergroupCinema);

        filtervalue = $("#filter-promo-checkbox").jqxCheckBox('val');
        if (filtervalue === true)
        {
            var filtergroupPromo = new $.jqx.filter();
            datafield = 'promo';
            filtertype = 'booleanfilter';
            filter_or_operator = 1;
            filtercondition = 'equal';
            var filterPromo = filtergroupPromo.createfilter(filtertype, filtervalue, filtercondition);
            filtergroupPromo.addfilter(filter_or_operator, filterPromo);
            $("#movies-list-grid").jqxGrid('addfilter', datafield, filtergroupPromo);
        }

        var filtergroupDate = new $.jqx.filter();
        filtervalue = $("#filter-date-dateinput").jqxDateTimeInput('getDate');
        datafield = 'projectiondate';
        filtertype = 'datefilter';
        filter_or_operator = 1;
        filtercondition = 'equal';
        var filterDate = filtergroupDate.createfilter(filtertype, filtervalue, filtercondition);
        filtergroupDate.addfilter(filter_or_operator, filterDate);
        $("#movies-list-grid").jqxGrid('addfilter', datafield, filtergroupDate);

        var filtergroupPrice = new $.jqx.filter();
        var filtervaluePrice = $("#filter-price-rangeselector").jqxRangeSelector('getRange');
        datafield = 'price';
        filtertype = 'numericfilter';
        filter_or_operator = 0;
        var filterconditionPriceFrom = 'greater_than_or_equal';
        var filterPriceFrom = filtergroupPrice.createfilter(filtertype, filtervaluePrice.from, filterconditionPriceFrom);
        filtergroupPrice.addfilter(filter_or_operator, filterPriceFrom);
        var filterconditionPriceTo = 'less_than_or_equal';
        var filterPriceTo = filtergroupPrice.createfilter(filtertype, filtervaluePrice.to, filterconditionPriceTo);
        filtergroupPrice.addfilter(filter_or_operator, filterPriceTo);
        $("#movies-list-grid").jqxGrid('addfilter', datafield, filtergroupPrice);

        $("#movies-list-grid").jqxGrid('applyfilters');
    }

});