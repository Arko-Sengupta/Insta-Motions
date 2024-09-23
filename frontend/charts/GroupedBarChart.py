import logging
import streamlit as st

def GroupedBarChart(comments_label: dict) -> None:
    """
    Responsive Grouped Bar Chart using D3.js within a Streamlit Application.
    """
    try:
        # Extract Comments and Label Proportions
        data = [{"comment": comment, "Positive": label[0], "Neutral": label[1], "Negative": label[2]} 
                for comment, label in comments_label.items()]

        # Sort Data by Overall Sentiment
        data.sort(key=lambda x: x["Positive"], reverse=True)

        # HTML, CSS, and JavaScript
        html_code = f"""
        <html lang="en">
        <head>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                .chart-container {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #0E1117;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 1.4);
                    border-radius: 10px;
                    margin: auto;
                    width: 100%;
                    max-width: 100%;
                    height: 100%;
                    min-width: 250px;
                    min-height: 260px;
                }}
                svg {{
                    width: 100%;
                    height: 100%;
                    max-width: 600px;
                    max-height: 450px;
                }}
                .bar {{
                    transition: height 0.3s ease;
                }}
            </style>
        </head>
        <body>
            <div class="chart-container">
                <svg id="grouped-bar-chart" viewBox="0 0 600 450" preserveAspectRatio="xMidYMid meet"></svg>
            </div>
            <script>
                const margin = {{top: 10, right: 30, bottom: 30, left: 40}},
                      width = 600 - margin.left - margin.right,
                      height = 450 - margin.top - margin.bottom;

                const svg = d3.select("#grouped-bar-chart")
                    .append("g")
                    .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

                const data = {data};

                const subgroups = ['Positive', 'Neutral', 'Negative'];
                const groups = data.map((d, i) => i + 1);

                const x = d3.scaleBand()
                    .domain(groups)
                    .range([0, width])
                    .padding([0.2]);
                
                const y = d3.scaleLinear()
                    .domain([0, 1])
                    .range([height, 0]);

                svg.append("g")
                    .attr("transform", `translate(0,${{height}})`)
                    .call(d3.axisBottom(x).tickSize(0).tickFormat(() => ""));

                svg.append("g")
                    .call(d3.axisLeft(y).tickSize(0).tickFormat(() => ""));

                const xSubgroup = d3.scaleBand()
                    .domain(subgroups)
                    .range([0, x.bandwidth()])
                    .padding([0.05]);

                const color = d3.scaleOrdinal()
                    .domain(subgroups)
                    .range(['#3897F0', '#88C4FE', '#B3D9FE']);

                svg.append("g")
                    .selectAll("g")
                    .data(data)
                    .enter()
                    .append("g")
                    .attr("transform", (d, i) => `translate(${{x(i + 1)}},0)`)
                    .selectAll("rect")
                    .data(d => subgroups.map(key => ({{key, value: d[key]}})))
                    .enter().append("rect")
                    .attr("x", d => xSubgroup(d.key))
                    .attr("y", height)
                    .attr("width", xSubgroup.bandwidth())
                    .attr("height", 0)
                    .attr("fill", d => color(d.key))
                    .transition()
                    .duration(1000)
                    .attr("y", d => y(d.value))
                    .attr("height", d => height - y(d.value));

                svg.selectAll(".tick line").attr("stroke", "white");
                svg.selectAll(".tick text").attr("fill", "white");
                svg.select(".domain").attr("stroke", "white");
            </script>
        </body>
        </html>
        """
        
        st.components.v1.html(html_code, height=550)
    except Exception as e:
        logging.error("An Error Occurred: ", exc_info=e)
        raise e