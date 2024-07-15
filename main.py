import os
import zipfile
import shutil

def extract_all_zips(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(root)

def collect_xml_files(directory, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.xml'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory))

def main():
    current_directory = os.getcwd()
    
    # Step 1: Extract all ZIP files in the current directory and subdirectories
    extract_all_zips(current_directory)
    
    # Step 2: Collect all XML files into a single ZIP
    output_zip_path = os.path.join(current_directory, 'all_xml_files.zip')
    collect_xml_files(current_directory, output_zip_path)

    print(f"All XML files have been collected into {output_zip_path}")

if __name__ == "__main__":
    main()
