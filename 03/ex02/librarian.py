import sys, os
import subprocess
import shutil, tarfile, gzip


def check_env():
    virtual_env_path = os.getenv('VIRTUAL_ENV')
    virtual_env_name = None
    if virtual_env_path:
        virtual_env_name = os.path.basename(virtual_env_path)
    return virtual_env_path, virtual_env_name

def install_libraries():
    try:
        if virtual_env_name == "shylaisa_env":
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            raise ValueError("Script should be run inside a virtual environment")
        return result.returncode
    
    except Exception as error:
        print(f"Error! {error}")
        sys.exit(1)

def list_and_save_installed_libraries():
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE, text=True)
    if result.returncode == 0:
        with open("requirements.txt", "w") as output_file:
            output_file.write(result.stdout)
    return result.stdout

def archive_env(path, name):
    tarball_path = "virtual_env_archive.tar"
    with tarfile.open(tarball_path, "w") as tar_file:
        tar_file.add(path, arcname=name)

    gzip_path = "virtual_env_archive.tar.gz"
    with open(tarball_path, "rb") as tar_file:
        with gzip.open(gzip_path,"wb") as gz_file:
            shutil.copyfileobj(tar_file, gz_file)

    os.remove(tarball_path)
        

if __name__ == '__main__':
    virtual_env_path, virtual_env_name  = check_env()
    result = install_libraries()
    if result == 0:
        archive_env(virtual_env_path, virtual_env_name)
        print(list_and_save_installed_libraries())
        ##print("Installation via requirements.txt is successfull")
    ##else:
        ##print(f"Installation isn't successfull {result}")


##source ../ex00/shylaisa/shylaisa_env/bin/activate