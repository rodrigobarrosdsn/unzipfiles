import os
import zipfile
import subprocess
import tempfile


def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def extract_rar(rar_path, extract_to):
    subprocess.run(['unrar', 'x', '-y', rar_path, extract_to], check=True)


def extract_all_archives(directory, temp_directory):
    # Filtra arquivos compactados e diretórios
    archives = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.zip') or file.endswith('.rar'):
                archives.append(file_path)
    
    while archives:
        archive = archives.pop(0)
        # Diretório para extrair o arquivo atual
        extract_to = os.path.join(temp_directory, os.path.splitext(os.path.basename(archive))[0])
        os.makedirs(extract_to, exist_ok=True)

        if archive.endswith('.zip'):
            extract_zip(archive, extract_to)
        elif archive.endswith('.rar'):
            extract_rar(archive, extract_to)

        # Adiciona novos arquivos compactados encontrados na extração para processamento futuro
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.zip') or file.endswith('.rar'):
                    archives.append(file_path)


def collect_xml_files(directory, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.xml'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory))


def main():
    current_directory = os.getcwd()

    with tempfile.TemporaryDirectory() as temp_directory:
        extract_all_archives(current_directory, temp_directory)

        output_zip_path = os.path.join(current_directory, 'all_xml_files.zip')
        collect_xml_files(temp_directory, output_zip_path)

        print(f"All XML files have been collected into {output_zip_path}")


if __name__ == "__main__":
    main()

