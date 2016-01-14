function generatedata(rowscount, hasNullValues) {
    // prepare the data
    var data = new Array();
    if (rowscount == undefined) rowscount = 100;
    var firstNames =
    [
        "Andrew", "Nancy", "Shelley", "Regina", "Yoshi", "Antoni", "Mayumi", "Ian", "Peter", "Lars", "Petra", "Martin", "Sven", "Elio", "Beate", "Cheryl", "Michael", "Guylene"
    ];

    var lastNames =
    [
        "Fuller", "Davolio", "Burke", "Murphy", "Nagase", "Saavedra", "Ohno", "Devling", "Wilson", "Peterson", "Winkler", "Bein", "Petersen", "Rossi", "Vileid", "Saylor", "Bjorn", "Nodier"
    ];

    var productNames =
    [
        "Black Tea", "Green Tea", "Caffe Espresso", "Doubleshot Espresso", "Caffe Latte", "White Chocolate Mocha", "Caramel Latte", "Caffe Americano", "Cappuccino", "Espresso Truffle", "Espresso con Panna", "Peppermint Mocha Twist"
    ];

    var priceValues =
    [
         "2.25", "1.5", "3.0", "3.3", "4.5", "3.6", "3.8", "2.5", "5.0", "1.75", "3.25", "4.0"
    ];

    for (var i = 0; i < rowscount; i++) {
        var row = {};
        var productindex = Math.floor(Math.random() * productNames.length);
        var price = parseFloat(priceValues[productindex]);
        var quantity = 1 + Math.round(Math.random() * 10);

        row["id"] = i;
        row["reportsto"] = Math.floor(Math.random() * firstNames.length);
        if (i % Math.floor(Math.random() * firstNames.length) === 0) {
            row["reportsto"] = null;
        }

        row["available"] = productindex % 2 == 0;
        if (hasNullValues == true) {
            if (productindex % 2 != 0) {
                var random = Math.floor(Math.random() * rowscount);
                row["available"] = i % random == 0 ? null : false;
            }
        }
        row["firstname"] = firstNames[Math.floor(Math.random() * firstNames.length)];
        row["lastname"] = lastNames[Math.floor(Math.random() * lastNames.length)];
        row["name"] = row["firstname"] + " " + row["lastname"]; 
        row["productname"] = productNames[productindex];
        row["price"] = price;
        row["quantity"] = quantity;
        row["total"] = price * quantity;

        var date = new Date();
        date.setFullYear(2015, Math.floor(Math.random() * 11), Math.floor(Math.random() * 27));
        date.setHours(0, 0, 0, 0);
        row["date"] = date;
       
        data[i] = row;
    }

    return data;
}
function generateordersdata(rowscount) {
    // prepare the data
    var data = new Array();
    if (rowscount == undefined) rowscount = 10;
    var firstNames =
    [
        "Andrew", "Nancy", "Shelley", "Regina", "Yoshi", "Antoni", "Mayumi", "Ian", "Peter", "Lars", "Petra", "Martin", "Sven", "Elio", "Beate", "Cheryl", "Michael", "Guylene"
    ];

    var lastNames =
    [
        "Fuller", "Davolio", "Burke", "Murphy", "Nagase", "Saavedra", "Ohno", "Devling", "Wilson", "Peterson", "Winkler", "Bein", "Petersen", "Rossi", "Vileid", "Saylor", "Bjorn", "Nodier"
    ];

    var productNames =
    [
        "Black Tea", "Green Tea", "Caffe Espresso", "Doubleshot Espresso", "Caffe Latte", "White Chocolate Mocha", "Caramel Latte", "Caffe Americano", "Cappuccino", "Espresso Truffle", "Espresso con Panna", "Peppermint Mocha Twist"
    ];

    var priceValues =
    [
         "2.25", "1.5", "3.0", "3.3", "4.5", "3.6", "3.8", "2.5", "5.0", "1.75", "3.25", "4.0"
    ];

    var companyNames = ["Dolor Foundation", "Vivamus Non Lorem LLP", "Vel Ltd", "Turpis Incorporated", "Egestas Nunc PC", "At Pretium Aliquet Associates", "Feugiat Inc.", "Lacus Industries", "Senectus Et Foundation", "Sed LLC", "Maecenas Mi Felis LLC", "Pede Blandit Ltd", "Pellentesque Habitant Morbi Institute"
		, "Mollis Vitae Industries", "Malesuada Vel Convallis LLP", "Risus Duis Corp.", "Convallis LLP", "Lobortis Augue LLC", "Auctor LLP", "Neque Inc.", "Lorem Eu Corporation"];
		
    for (var i = 0; i < rowscount; i++) {
        var row = {};
        var productindex = Math.floor(Math.random() * productNames.length);
        var price = parseFloat(priceValues[productindex]);
        var quantity = 2 + Math.round(Math.random() * 10);
       
        row["id"] = i;
        row["parentid"] = null;
        row["name"] = "Order " + i;
        row["firstname"] = firstNames[Math.floor(Math.random() * firstNames.length)];
        row["lastname"] = lastNames[Math.floor(Math.random() * lastNames.length)];
        row["customer"] = companyNames[Math.floor(Math.random() * companyNames.length)];
        var date = new Date();
        var month = Math.floor(Math.random() * 11);
        var day = Math.floor(Math.random() * 27);
        date.setFullYear(2014, month, day);
        date.setHours(0, 0, 0, 0);
        row["date"] = date;
        row["price"] = "";
        row["quantity"] = "";
        data.push(row);

        var subRowsCount = 1+Math.round(Math.random() * 8);
        var t = 0;
        var q = 0;
        for (var j = 0; j < subRowsCount; j++) {
            var subRow = {};
            var productindex = Math.floor(Math.random() * productNames.length);
            var price = parseFloat(priceValues[productindex]);
            var quantity = 1;
            subRow["name"] = productNames[productindex];
            subRow["id"] = "" + i + "." + (1 + j);
            subRow["parentid"] = i;
            subRow["price"] = price;
            subRow["quantity"] = 1;
            var date = new Date();
            date.setFullYear(2014, month, day);
            date.setHours(Math.floor(Math.random() * 23), Math.floor(Math.random() * 59), 0, 0);
            subRow["date"] = date;
            row["firstname"] = firstNames[Math.floor(Math.random() * firstNames.length)];
            row["lastname"] = lastNames[Math.floor(Math.random() * lastNames.length)];
            subRow["customer"] = row["firstname"] + " " + row["lastname"];
            t += quantity * price;
            data.push(subRow);
            q += quantity;
        }
        row["price"] = t;
        row["quantity"] = 1;
    }

    return data;
}
function generatecarsdata() {
    var makes = [{ value:"", label: "Any"}, 
       {value:"140", label: "Abarth"},      
       {value:"375", label: "Acura"},      
       {value:"800", label: "Aixam"},      
       {value:"900", label: "Alfa Romeo"},      
       {value:"1100", label: "Alpina"},      
       {value:"121", label: "Artega"},      
       {value:"1750", label: "Asia Motors"},      
       {value:"1700", label: "Aston Martin"},      
       {value:"1900", label: "Audi"},      
       {value:"2000", label: "Austin"},      
       {value:"1950", label: "Austin Healey"},      
       {value:"3100", label: "Bentley"},      
       {value:"3500", label: "BMW"},      
       {value:"3850", label: "Borgward"},      
       {value:"4025", label: "Brilliance"},      
       {value:"4350", label: "Bugatti"},      
       {value:"4400", label: "Buick"},      
       {value:"4700", label: "Cadillac"},      
       {value:"112", label: "Casalini"},      
       {value:"5300", label: "Caterham"},      
       {value:"5600", label: "Chevrolet"},      
       {value:"5700", label: "Chrysler"},      
       {value:"5900", label: "Citroën"},      
       {value:"6200", label: "Cobra"},      
       {value:"6325", label: "Corvette"},      
       {value:"6600", label: "Dacia"},      
       {value:"6800", label: "Daewoo"},      
       {value:"7000", label: "Daihatsu"},      
       {value:"7400", label: "DeTomaso"},      
       {value:"7700", label: "Dodge"},      
       {value:"8600", label: "Ferrari"},      
       {value:"8800", label: "Fiat"},      
       {value:"172", label: "Fisker"},      
       {value:"9000", label: "Ford"},      
       {value:"9900", label: "GMC"},      
       {value:"122", label: "Grecav"},      
       {value:"10850", label: "Holden"},      
       {value:"11000", label: "Honda"},      
       {value:"11050", label: "Hummer"},      
       {value:"11600", label: "Hyundai"},      
       {value:"11650", label: "Infiniti"},      
       {value:"11900", label: "Isuzu"},      
       {value:"12100", label: "Iveco"},      
       {value:"12400", label: "Jaguar"},      
       {value:"12600", label: "Jeep"},      
       {value:"13200", label: "Kia"},      
       {value:"13450", label: "Königsegg"},      
       {value:"13900", label: "KTM"},      
       {value:"14400", label: "Lada"},      
       {value:"14600", label: "Lamborghini"},      
       {value:"14700", label: "Lancia"},      
       {value:"14800", label: "Land Rover"},      
       {value:"14845", label: "Landwind"},      
       {value:"15200", label: "Lexus"},      
       {value:"15400", label: "Ligier"},      
       {value:"15500", label: "Lincoln"},      
       {value:"15900", label: "Lotus"},      
       {value:"16200", label: "Mahindra"},      
       {value:"16600", label: "Maserati"},      
       {value:"16700", label: "Maybach"},      
       {value:"16800", label: "Mazda"},      
       {value:"137", label: "McLaren"},      
       {value:"17200", label: "Mercedes-Benz"},      
       {value:"17300", label: "MG"},      
       {value:"30011", label: "Microcar"},      
       {value:"17500", label: "MINI"},      
       {value:"17700", label: "Mitsubishi"},      
       {value:"17900", label: "Morgan"},      
       {value:"18700", label: "Nissan"},      
       {value:"18875", label: "NSU"},      
       {value:"18975", label: "Oldsmobile"},      
       {value:"19000", label: "Opel"},      
       {value:"149", label: "Pagani"},      
       {value:"19300", label: "Peugeot"},      
       {value:"19600", label: "Piaggio"},      
       {value:"19800", label: "Plymouth"},      
       {value:"20000", label: "Pontiac"},      
       {value:"20100", label: "Porsche"},      
       {value:"20200", label: "Proton"},      
       {value:"20700", label: "Renault"},      
       {value:"21600", label: "Rolls Royce"},      
       {value:"21700", label: "Rover"},      
       {value:"125", label: "Ruf"},      
       {value:"21800", label: "Saab"},      
       {value:"22000", label: "Santana"},      
       {value:"22500", label: "Seat"},      
       {value:"22900", label: "Skoda"},      
       {value:"23000", label: "Smart"},      
       {value:"100", label: "Spyker"},      
       {value:"23100", label: "Ssangyong"},      
       {value:"23500", label: "Subaru"},      
       {value:"23600", label: "Suzuki"},      
       {value:"23800", label: "Talbot"},      
       {value:"23825", label: "Tata"},      
       {value:"135", label: "Tesla"},      
       {value:"24100", label: "Toyota"},      
       {value:"24200", label: "Trabant"},      
       {value:"24400", label: "Triumph"},      
       {value:"24500", label: "TVR"},      
       {value:"25200", label: "Volkswagen"},      
       {value:"25100", label: "Volvo"},      
       {value:"25300", label: "Wartburg"},      
       {value:"113", label: "Westfield"},      
       { value: "25650", label: "Wiesmann" }];

    var fuelType = ["Any", "Diesel", "Electric", "Ethanol (FFV, E85, etc.)", "Gas", "LPG", "Natural Gas", "Hybrid", "Hydrogen", "Petrol"];
    var vehicleType = ["Saloon", "Small Car", "Estate Car", "Van / Minibus", "Off-road Vehicle/Pickup Truck", "Cabriolet / Roadster", "Sports Car/Coupe"];
    var power =
    [
      {value:"24", label: "24 kW (33 PS)"},
      {value:"36", label: "36 kW (49 PS)"},
      {value:"43", label: "43 kW (58 PS)"},
      {value:"54", label: "54 kW (73 PS)"},
      {value:"65", label: "65 kW (88 PS)"},
      {value:"73", label: "73 kW (99 PS)"},
      {value:"86", label: "86 kW (117 PS)"},
      {value:"95", label: "95 kW (129 PS)"},
      {value:"109", label: "109 kW (148 PS)"},
      {value:"146", label: "146 kW (199 PS)"},
      {value:"184", label: "184 kW (250 PS)"},
      {value:"222", label: "222 kW (302 PS)"},
      {value:"262", label: "262 kW (356 PS)"},
      {value:"295", label: "295 kW (401 PS)"},
      {value:"333", label: "333 kW (453 PS)"}
    ];

    var data = new Array();
    for (var i = 0; i < makes.length; i++) {
        var row = {};
        row.make = makes[i].label;
        row.fuelType = fuelType[Math.floor(Math.random() * fuelType.length)];
        row.vehicleType = vehicleType[Math.floor(Math.random() * vehicleType.length)];
        var powerIndex = Math.floor(Math.random() * power.length);
        if (powerIndex == power.length - 1) powerIndex --;
        row.powerFrom = power[powerIndex];
        row.powerTo = power[powerIndex + 1];
        data.push(row);
    }
    return data;
}
function generateappointments() {
  
}