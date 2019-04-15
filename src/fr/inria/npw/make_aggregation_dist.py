import click

from fr.inria.npw import input_analyser
from fr.inria.npw.errors import InputFileNotFoundError, OutputDirNotFoundError
from fr.inria.npw.output_maker import create_output_files


@click.command()
@click.argument('input_file')
@click.option('-o', '--output', 'output_dir', default='.', help="The directory in which the output HTML and PNG files "
                                                                "are going to be saved. The output directory must "
                                                                "already exist.")
@click.option('-n', '--name', 'name', default='unknown', help="The name of the graph. It will also be used to name "
                                                              "the generated output files.")
@click.option('-m', '--max', 'max_aggregation_to_be_shown', default=20, help="The value of the last aggregation strip "
                                                                             "on the graph.")
@click.option('-u', '--no-max', 'no_max', is_flag=True, default=False, help="Use this flag so there is no max "
                                                                            "aggregation shown on the outputted graph.")
def make_aggregation_dist(input_file, output_dir, name, max_aggregation_to_be_shown, no_max):
    """
    Program that computes the aggregation described by INPUT_FILE and generate an histogram under the HTML and the
    PNG formats. INPUT_FILE must either be a PCAP/PCAPNG or JSON file
    """

    if max_aggregation_to_be_shown < 1:
        print('The value of -m or --max should be greater than 0.')
        return

    try:

        if input_file.endswith('.json'):
            data = input_analyser.analyse_json_data(input_file)
        elif input_file.endswith('.pcapng') or input_file.endswith('.pcap'):
            data = input_analyser.analyse_pcap_data(input_file)
        else:
            print('Error: The file {} is not of a supported type. Supported types are .json and .pcapng/.pcap.'
                  .format(input_file))
            return

        if no_max:
            create_output_files(name, output_dir, data, None)
        else:
            create_output_files(name, output_dir, data, max_aggregation_to_be_shown)

    except InputFileNotFoundError:
        print('Error: The file {} was not found.'.format(input_file))
    except OutputDirNotFoundError:
        print('Error: The directory {} was not found.'.format(output_dir))


if __name__ == '__main__':
    make_aggregation_dist()
