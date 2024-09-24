import logging
import streamlit as st

def PieChart(data: list) -> None:
    """
    Pie Chart using D3.js within a Streamlit Application.
    """
    try:
        # HTML, CSS and JavaScript
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
                .slice {{
                    stroke: #fff;
                    stroke-width: 2px;
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
            </style>
        </head>
        <body>
            <div class="chart-container">
                <svg id="pie-chart"></svg>
            </div>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #B3D9FE;"></div> Negative: {str((round(data[0], 2))*100) + "%"}
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #88C4FE;"></div> Neutral: {str((round(data[1], 2))*100) + "%"}
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #3897F0;"></div> Positive: {str((round(data[2], 2))*100) + "%"}
                </div>
            </div>
            <script>
                const width = 200, height = 200, radius = Math.min(width, height) / 2;
                const colors = d3.scaleOrdinal(['#B3D9FE', '#88C4FE', '#3897F0']);
        
                const svg = d3.select("#pie-chart")
                    .attr("width", width)
                    .attr("height", height)
                    .append("g")
                    .attr("transform", `translate(${{width / 2}}, ${{height / 2}})`);
        
                const pie = d3.pie();
                const arc = d3.arc().innerRadius(0).outerRadius(radius);
        
                const arcs = svg.selectAll(".arc")
                    .data(pie({data}))
                    .enter().append("g")
                    .attr("class", "arc");
        
                arcs.append("path")
                    .attr("class", "slice")
                    .attr("d", arc)
                    .attr("fill", d => colors(d.index))
                    .transition()
                    .duration(1000)
                    .attrTween("d", function(d) {{
                        const i = d3.interpolate({{startAngle: 0, endAngle: 0}}, d);
                        return function(t) {{ return arc(i(t)); }};
                    }});
            </script>
        </body>
        </html>
        """
        
        st.components.v1.html(html_code, height=350)
    except Exception as e:
        logging.error("An Error Occurred: ", exc_info=e)
        raise e