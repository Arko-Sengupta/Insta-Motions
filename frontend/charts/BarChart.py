import logging
import streamlit as st

def BarChart(data: list) -> None:
    """
    Bar Chart using D3.js within a Streamlit Application.
    """
    try:
        # HTML, CSS, and JavaScript
        html_code = f"""
        <html lang="en">
        <head>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                .chart-container {{
                    width: 250px;
                    height: 250px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #0E1117;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 1.4);
                    border-radius: 10px;
                    margin: auto;
                    position: relative;
                }}
                .legend {{
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                    color: white;
                }}
                .legend-item {{
                    margin: 0 10px;
                    display: flex;
                    align-items: center;
                }}
                .legend-color {{
                    width: 15px;
                    height: 15px;
                    margin-right: 5px;
                }}
                .bar {{
                    transition: height 0.3s ease;
                }}
            </style>
        </head>
        <body>
            <div class="chart-container">
                <svg id="bar-chart"></svg>
            </div>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #3897F0;"></div> Likes: {data[0]}
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #88C4FE;"></div> Comments: {data[1]}
                </div>
            </div>
            <script>
                const width = 200, height = 200;
                const data = [{data[0]}, {data[1]}];
                const labels = ['Likes', 'Comments'];
                const colors = d3.scaleOrdinal(['#3897F0', '#88C4FE']);
        
                const svg = d3.select("#bar-chart")
                    .attr("width", width)
                    .attr("height", height)
                    .append("g")
                    .attr("transform", `translate(0, 10)`);
        
                const xScale = d3.scaleBand()
                    .domain(labels)
                    .range([0, width])
                    .padding(0.4);
        
                const yScale = d3.scaleLinear()
                    .domain([0, d3.max(data)])
                    .range([height - 20, 0]);

                svg.append("g")
                    .attr("transform", `translate(0, ${{height - 20}})`)
                    .call(d3.axisBottom(xScale));
                    
                svg.append("g")
                    .call(d3.axisLeft(yScale).ticks(5));

                svg.selectAll(".bar")
                    .data(data)
                    .enter()
                    .append("rect")
                    .attr("class", "bar")
                    .attr("x", (d, i) => xScale(labels[i]))
                    .attr("y", height - 20)  // Start at the bottom of the chart for animation
                    .attr("width", xScale.bandwidth())
                    .attr("height", 0)  // Initial height is zero
                    .attr("fill", (d, i) => colors(i))
                    .transition()  // Apply the transition for animation
                    .duration(1000)
                    .attr("y", d => yScale(d))
                    .attr("height", d => height - 20 - yScale(d));
            </script>
        </body>
        </html>
        """
        
        st.components.v1.html(html_code, height=350)
    except Exception as e:
        logging.error("An Error Occurred: ", exc_info=e)
        raise e