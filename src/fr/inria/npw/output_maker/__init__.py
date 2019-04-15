import sys
from os import path

import numpy as np
from bokeh.io import export_png
from bokeh.models import SingleIntervalTicker, FuncTickFormatter
from bokeh.plotting import figure, save, output_file

from fr.inria.npw.errors import OutputDirNotFoundError
from fr.inria.npw.input_analyser import InputData

DEFAULT_MAX_AGGREGATION_TO_BE_SHOWN = 20

HEIGHT_OF_OCCURRENCES_TEXTS_FOR_HEIGHT_OF_ONE_HUNDRED = 25
HEIGHT_OF_AVERAGE_TEXT_FOR_HEIGHT_OF_ONE_HUNDRED = 1140
HEIGHT_OF_NUMBER_OF_PACKETS_TEXT_FOR_HEIGHT_OF_ONE_HUNDRED = 1100

X_AXIS_TICK_FORMATTER_CODE = '''
    if (tick > {0}) {{
        return "{1}+";
    }} else {{
        return tick;
    }}
'''


def create_output_files(file_name, output_path, data, max_aggregation_to_be_shown=DEFAULT_MAX_AGGREGATION_TO_BE_SHOWN):
    """
    :type file_name: str
    :type output_path: str
    :type data: InputData
    :param max_aggregation_to_be_shown: Values of aggregation that are higher than this variable will be in the column
    "{max_aggregation_to_be_shown + 1}+". If None, there won't be any max aggregation to be shown on the graph.
    :type max_aggregation_to_be_shown: int or None
    """

    if max_aggregation_to_be_shown is not None:
        # We create columns for 1, 2, 3, ... to MAX_AGGREGATION_TO_BE_SHOWN.
        # The rest of the data enters the MAX_AGGREGATION_TO_BE_SHOWN+ column.
        bins = [edge + 0.5 for edge in range(max_aggregation_to_be_shown + 1)]
        bins.append(sys.maxsize)

        hist, bins = np.histogram(data.big_packets, bins=bins)

        edges = [edge + 0.5 for edge in range(max_aggregation_to_be_shown + 2)]

    else:
        bins = [edge + 0.5 for edge in range(max(data.big_packets) + 1)]

        hist, edges = np.histogram(data.big_packets, bins=bins)

    plot = _make_plot(file_name, hist, edges, data.average_aggregation,
                      data.number_of_small_packets, max_aggregation_to_be_shown)

    output_file(path.join(output_path, "{0}.html".format(file_name)), title=file_name)

    try:
        save(plot)
        print("Saved {0}".format(path.join(output_path, "{0}.html".format(file_name))))
        export_png(plot, path.join(output_path, "{0}.png".format(file_name)))
        print("Saved {0}".format(path.join(output_path, "{0}.png".format(file_name))))
    except FileNotFoundError as e:
        raise OutputDirNotFoundError(e)
    except RuntimeError:
        print("Warn: PhantomJS is not present in PATH. Skipping the export to PNG file.")


def _make_plot(title, hist, edges, average, number_of_packets, max_aggregation_to_be_shown):
    plot = figure(title=title, tools='', background_fill_color="#fafafa", x_range=[edges[0], edges[-1]])

    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
              fill_color="#304ffe", line_color="white", alpha=0.5)
    plot.text([x + 0.5 for x in edges[:-1]],
              [y + _convert_height(HEIGHT_OF_OCCURRENCES_TEXTS_FOR_HEIGHT_OF_ONE_HUNDRED, 1000, hist.max()) for y in
               hist],
              text=hist, text_baseline="middle",
              text_align="center")

    plot.text([1], [_convert_height(HEIGHT_OF_AVERAGE_TEXT_FOR_HEIGHT_OF_ONE_HUNDRED, 1000, hist.max())],
              text=["Average Aggregation: {}".format(round(average, 2))], text_baseline="middle",
              text_align="left")

    plot.text([1], [_convert_height(HEIGHT_OF_NUMBER_OF_PACKETS_TEXT_FOR_HEIGHT_OF_ONE_HUNDRED, 1000, hist.max())],
              text=["Number of Received Packets: {}".format(number_of_packets)], text_baseline="middle",
              text_align="left")

    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.sizing_mode = "stretch_both"

    plot.grid.grid_line_color = "white"

    plot.y_range.start = 0

    ticker = SingleIntervalTicker(interval=1)
    plot.xaxis.ticker = ticker
    plot.xaxis.axis_label = "Aggregation"
    plot.xaxis.minor_tick_line_color = None
    plot.yaxis.axis_label = "Number of Occurrences"

    if max_aggregation_to_be_shown is not None:
        formatter = FuncTickFormatter(code=_format_x_axis_tick_formatter_code(max_aggregation_to_be_shown))
        plot.xaxis.formatter = formatter

    return plot


def _convert_height(height_to_convert, base_height, current_height):
    return (current_height / base_height) * height_to_convert


def _format_x_axis_tick_formatter_code(max_aggregation_to_be_shown):
    return X_AXIS_TICK_FORMATTER_CODE.format(
        max_aggregation_to_be_shown,
        max_aggregation_to_be_shown + 1
    )
