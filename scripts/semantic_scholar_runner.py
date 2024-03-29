import os
from semantic_scholar import SemanticScholar
import datetime

# Run the article downloader

def process_paper_title(ss, title, directory_name="iclr"):
    """Fetch and store all data related to the given paper title."""
    paperID = ss.get_paper_id_by_title(title)
    if not paperID:
        print(f"Failed to find paperID for title: {title}")
        return

    bibtex, arxiv_id, publication_year, abstract, referenceCount, citationCount = ss.get_paper_details(paperID)

    references = ss.fetch_and_store_references(paperID)
    ss.add_to_papers_list(paperID, abstract, bibtex, references, referenceCount, citationCount)

    # Also add the paper to the master_list
    ss.add_to_master_list(title, paperID, arxiv_id, publication_year)

    # Create a directory named based on the publication year and download the ArXiv PDF
    if publication_year is not None:
        directory_name = f"{directory_name}_{publication_year}"
    else:
        directory_name = f"{directory_name}_no_year"
    if arxiv_id is not None:
        ss.download_arxiv_pdf(arxiv_id, directory_name)

def main():
    # Set the conference name
    conference = "icml"
    
    paper_list = "ood-papers.txt" # subset of 500 papers (10%) "icml2020-2023papers.txt" script broke on line 3004. Restart from 3k
    # paper_list = "icml2020-2023papers.txt" # 5000 papers

    # identifier for the file
    identifier = "ood"

    # Initialize the SemanticScholar class with debug mode turned on
    ss = SemanticScholar(debug=True)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # get parent directory
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    
    # Build the path to the data file
    file_path = os.path.join(parent_dir, 'data', paper_list)
    
    # Open the file for reading
    with open(file_path, "r", encoding='utf-8') as file:
        # Initialize a counter
        counter = 0
        
        # start timer
        start = datetime.datetime.now()

        # Iterate through each line in the file
        for line in file:
            # Strip leading and trailing whitespace (including newline characters)
            stripped_line = line.strip()

            # Check if the line is not blank and doesn't start with '#'
            if stripped_line and not stripped_line.startswith("#"):

                # Process the paper title with the counter
                process_paper_title(ss, stripped_line, conference)

                # Increment the counter
                counter += 1

                # Print the current time and counter
                now = datetime.datetime.now()
                print(f"***** [{now}] Processing paper {counter} *****")
                # print running time
                diff = now - start
                print(f"Running time: {str(diff).split('.')[0]}")

                # save the data to a pickle file every 1000 papers
                if counter % 1000 == 0:
                    # Save the data to a pickle file with a date, time, and counter suffix
                    now = datetime.datetime.now()
                    suffix = now.strftime("%Y-%m-%d_%H-%M-%S")
                    # print total running time
                    print(f"Saving 1000+ papers, total running time: {now - start}")

                    filename = f"semantic_data_{suffix}_{counter}_{identifier}_files.pkl"
                    ss.store_data_as_pickle(filename, "./saved_data")

    # Save the data to a pickle file with a date, time, and counter suffix
    now = datetime.datetime.now()
    suffix = now.strftime("%Y-%m-%d_%H-%M-%S")
    # print total running time
    print(f"Total running time: {now - start}")

    filename = f"semantic_data_{suffix}_{counter}_{identifier}_files.pkl"
    ss.store_data_as_pickle(filename, "./saved_data")

if __name__ == "__main__":
    main()
