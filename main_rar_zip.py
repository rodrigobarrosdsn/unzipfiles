import os
import zipfile
import rarfile
import shutil
import tempfile


def extract_all_archives(directory, temp_directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_directory)
            elif file.endswith('.rar'):
                rar_path = os.path.join(root, file)
                with rarfile.RarFile(rar_path, 'r') as rar_ref:
                    rar_ref.extractall(temp_directory)


def collect_xml_files(directory, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.xml'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(
                        file_path, directory))


def main():
    current_directory = os.getcwd()

    # Cria um diretório temporário para a extração dos arquivos ZIP e RAR
    with tempfile.TemporaryDirectory() as temp_directory:
        # Step 1: Extract all ZIP and RAR files into the temporary directory
        extract_all_archives(current_directory, temp_directory)

        # Step 2: Collect all XML files from the temporary directory into a single ZIP
        output_zip_path = os.path.join(current_directory, 'all_xml_files.zip')
        collect_xml_files(temp_directory, output_zip_path)

        print(f"All XML files have been collected into {output_zip_path}")


if __name__ == "__main__":
    main()
