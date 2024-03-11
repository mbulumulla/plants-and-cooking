
recipesSelected.forEach(d => {
                        d3.select("#cart")
                            .append("p")
                            .text(d['Title'])
                            .attr("class", "recipes");
                    });
                    
plant_data_subset.forEach(d => {
    d3.select("#shopping")
        .append("button")
        .text(d['name1'])
        .attr("id", d['name1Lower'])
        .attr("class", "shopButtons:active")
        .on("click", function () {
            purchaseSeeds(selectedCrops, d['name1'], d['name1Lower']);
            d3.selectAll("button#" + d['name1Lower']).classed("active", function () {
                console.log(d['img'])
                return selectedCrops.includes(d['name1Lower']);

            })

        });
}
);


async function createTemp(selectedPlant) {
    let plant_data = await d3.csv("plant-clean.csv", d3.autoType);
    //////////////////// TEMP BAR ////////////////////
    const temp = d3.select("svg#temp");
    const tempMargin = {top: 10, right: 10, bottom: 10, left: 10};
    const tempChartWidth = temp.attr("width") - tempMargin.left - tempMargin.right;
    const tempChartHeight = temp.attr("height") - tempMargin.top - tempMargin.bottom;

    // linear gradient bar from https://stackoverflow.com/questions/39023154/how-to-make-a-color-gradient-bar-using-d3js
    var defs = temp.append('defs');
    var lg = defs.append('linearGradient')
        .attr('id', 'Gradient2')
        .attr('x1', 0)
        .attr('x2', 0)
        .attr('y1', 0)
        .attr('y2', 1);

    lg.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', 'lightcoral');
    lg.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', 'lightblue');

    // gradient bar
    temp.append('rect')
        .attr('x', 20)
        .attr('y', 0)
        .attr('width', tempChartWidth)
        .attr('height', tempChartHeight)
        .style("fill", "url(#Gradient2)");

    let tempAnnotations = temp.append("g").attr("id", "tempAnnotations");
    let tempChartArea = temp.append("g").attr("id", "temps")
        .attr("transform", "translate(" + tempMargin.left + "," + tempMargin.top + ")");

    // getting the actual min and max for the scale
    const maxMax = d3.max(plant_data, d => d['soilTempMaxF']);
    const minMin = d3.min(plant_data, d => d['soilTempMinF']);

    const tempScale = d3.scaleLinear().domain([minMin, maxMax]).range([tempChartHeight, 0]);

    // y axis
    let tempAxis = d3.axisLeft(tempScale);
    let tempGridlines = d3.axisLeft(tempScale)
        .tickSize(-tempChartWidth - 100);
    tempAnnotations.append("g")
        .attr("class", "yGridlines")
        .attr("transform", `translate(${tempMargin.left + 10},${tempMargin.top})`)
        .call(tempGridlines);

    // select data based on selectedPlant name
    let selectedData = plant_data.filter(function (d) {
        return d.name1Lower == selectedPlant
    })

    // adding mean of max, mean of min, max value for selected plant
    const tempLines = [
        {
            "color": "green",
            "lineWidth": 1,
            "temp": d3.mean(plant_data, d => d['soilTempMaxF'])
        },
        {
            "color": "green",
            "lineWidth": 1,
            "temp": d3.mean(plant_data, d => d['soilTempMinF'])
        },
        {
            "color": "sienna",
            "lineWidth": 4,
            "temp": d3.max(selectedData, d => d['soilTempMaxF'])
        },
        {
            "color": "sienna",
            "lineWidth": 4,
            "temp": d3.min(selectedData, d => d['soilTempMinF'])
        }];
    console.log(tempLines);
    removeElements(".temperatureLines");
    temp.selectAll("temperatureLines")
        .data(tempLines)
        .join("line")
        .attr("class", "temperatureLines")
        .style("stroke", d => d['color'])
        .style("stroke-width", d => d['lineWidth'])
        .attr("x1", 0)
        .attr("y1", d => tempScale(d['temp']))
        .attr("x2", 50)
        .attr("y2", d => tempScale(d['temp']))
}

