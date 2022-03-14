import os
import argparse
import time
from pprint import pprint


def main():
    """
    Main function for determining the number of files that a directory contains in total, thus, by considering all its
    subdirectories
    :return:
    """
    # Retrieve the variables from the arguments passed by the user
    in_dir = os.path.normpath(args.in_dir[0])
    count_threshold = args.count_threshold
    if count_threshold is None:
        count_threshold = 0
    elif not isinstance(count_threshold, int):
        raise ValueError('***ERROR!!! You passed an argument that is neither None nor an integer value. Please check '
                         'the requirements regarding the input variables.')

    # Initialize important variables
    in_dir_levels = in_dir.count('\\')
    total_files = 0
    total_dirs = 0
    deepest_level = 0
    all_dir_information = dict()

    # Loop 1: Loop through all subdirectories of the passed directory. By this, determine the level depth (compared to
    # the root directory) and the total number of files for each directory and put this into a dictionary.
    for root, dirs, files in os.walk(in_dir):
        print('Searching in: ', root)
        num_of_files_in_root = 0

        root_levels = root.count('\\') - in_dir_levels
        if root_levels > deepest_level:
            deepest_level = root_levels

        for directory_i in dirs:
            total_dirs += 1

        # Loop through the files and add them to the total number of files while omitting shortcuts
        for file_i in files:
            if '.lnk' not in file_i:
                num_of_files_in_root += 1
                total_files += 1

        print('---> {} files found here.'.format(num_of_files_in_root))
        all_dir_information[root] = {'files': num_of_files_in_root,
                                     'levels': root_levels}
        print('')

    # Print the results of the first loop
    print('----------------------------')
    print('Total number of files', total_files)
    print('Total Number of directories', total_dirs)
    print('Total:', (total_dirs + total_files))
    print('----------------------------')
    print('')
    pprint(all_dir_information)
    print('----------------------------')
    print('')

    # Loop 2: Loop though the dictionary with the retrieved information. In addition, conduct a second loop that starts
    # on the deepest children level and then goes up towards the root level. For each level and for each directory of
    # the same branch, determine the cumulative number of files.
    cumulative_dict = dict()
    for i in reversed(range(deepest_level)):
        for k, v in all_dir_information.items():
            
            # If we find an entry from the child level we are iterating through, determine the parent directory and 
            # retrieve the number of files at the current level (which should be written in the current dictionary at 
            # the same level we are right now).
            if v['levels'] == i:
                parent_dir = os.path.dirname(k)
                add_file_number_from_current_level = v['files']

                # Determine the cumulative number of files from the lower levels. If an entry for a directory does not 
                # exist yet, start with one. 
                add_cumulative_number_from_lower_levels = 0
                if k in cumulative_dict:
                    add_cumulative_number_from_lower_levels = cumulative_dict[k]

                # Sum up both values: Those of the current level and those of the lower levels
                add_to_upper_level = add_file_number_from_current_level + add_cumulative_number_from_lower_levels

                # Add the value to the directory, if it does not exist yet. If a value exist, retrieve the existing and
                # add the additional value
                if parent_dir in cumulative_dict:
                    existing_number_in_dict = cumulative_dict[parent_dir]
                    cumulative_dict[parent_dir] = existing_number_in_dict + add_to_upper_level
                else:
                    cumulative_dict[parent_dir] = add_to_upper_level

    # Loop 3: Refine the dictionary by considering only the folders that contain at least the given number of files
    # (including the children directories)
    refined_dict = dict()
    for k, v in cumulative_dict.items():
        if v > count_threshold:
            refined_dict[k] = v

    # Print the results of the final analysis, including considering the threshold filter
    print('')
    pprint(refined_dict)
    print('----------------------------')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time0 = time.time()

    # Define a parser, write the help function, and parse the arguments
    parser = argparse.ArgumentParser(
        description='This is the main function that conducts an analysis of the number of files that are contained in '
                    'a directory. The function also considers all its subdirectories and sums the number of files up '
                    'to the uppoermost parent directory.',
        epilog='Please provide the required arguments for the path to the directory that should be analyzed and the '
               'number of files each directory must contain (including its subfolders) in order to be listed in the '
               'results.'
    )
    parser.add_argument('in_dir', type=str, default='', nargs=1,
                        help='The path to the input directory that should be analyzed (including its children)')
    parser.add_argument('--count_threshold', type=int, default=None,
                        help='[ None (default) | any integer value (1, 2, 3, ...) that represents the number of files '
                             'listed in the corresponding directory or in all its subdirectories, which acts as a '
                             'filter for showing all directories that contain at least the given number of files. ]')
    args = parser.parse_args()

    # Pass the dictionaries to the main function and run it
    main()

    # Show the time needed to run the function
    # if const.working_device == ('pc' or 'platform_server'):
    print('')
    print('Done.')
    print('The process took ' + str(round(time.time() - time0, 3)) + ' seconds.')