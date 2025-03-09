import subprocess

subprocess.Popen(["/usr/local/bin/ngrok", "http", "8765"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def restart_ngrok():
    """ Restart the Ngrok tunnel if the URL is not valid """
    print("Restarting Ngrok...")
    subprocess.Popen(["/usr/local/bin/ngrok", "http", "8765"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return

