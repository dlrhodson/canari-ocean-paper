# plot_styles.py

# Define colors for each line or plot element
spread_colour='lightgray'
mean_colour='olive'
obs_colour='k'

max_colour='red'
min_colour='blue'

total_26n_mean_color = 'blue'
total_26n_spread_color = 'lightblue'
rapid_line_color = 'orange'

# Define line styles
total_26n_mean_style = '-'
rapid_line_style = '--'

# Define line widths
total_26n_mean_width = 1.5
rapid_line_width = 2.0

# Define plot limits and title
plot_title = "Atlantic Heat Transport 26N PW 1σ Spread"
ylim = (0.9, 1.2)

# Labels
x_label = "Time"
y_label = "Heat Transport (PW)"
legend_labels = {
    "total_mean": "Total 26N Mean",
    "spread": "1σ Spread",
    "rapid": "RAPID"
}
