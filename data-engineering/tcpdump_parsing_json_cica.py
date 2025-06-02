import subprocess
import os
import glob

def convert_pcaps_to_json(pcap_directory, output_directory):
    """
    Converts multiple pcap files in a directory to JSON using tshark.

    Args:
        pcap_directory (str): The directory containing the pcap files.
        output_directory (str): The directory where the JSON files will be saved.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pcap_files = glob.glob(os.path.join(pcap_directory, "*.pcap"))
    pcap_files.extend(glob.glob(os.path.join(pcap_directory, "*.pcapng"))) # Include pcapng as well

    if not pcap_files:
        print(f"No .pcap or .pcapng files found in '{pcap_directory}'.")
        return

    for pcap_file in pcap_files:
        filename_without_ext = os.path.splitext(os.path.basename(pcap_file))[0]
        output_json_path = os.path.join(output_directory, f"{filename_without_ext}.json")

        tshark_command = [
            "tshark",
            "-r",
            pcap_file,
            "-T",
            "json",
            ">",
            output_json_path  # Note: Shell redirection will be handled by subprocess
        ]

        try:
            print(f"Processing: {pcap_file} -> {output_json_path}")
            # Use shell=True to handle the redirection, but be cautious with untrusted input
            subprocess.run(" ".join(tshark_command), shell=True, check=True, capture_output=True)
            print(f"Successfully converted: {output_json_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {pcap_file}:")
            print(e.stderr.decode())
        except FileNotFoundError:
            print("Error: tshark command not found. Make sure Wireshark is installed and tshark is in your PATH.")

if __name__ == "__main__":
    pcap_directory = "/home/LQL3227/phd/tcpdump" #("Enter the directory containing the pcap files: ")
    output_directory = "/home/LQL3227/phd/json" #("Enter the directory to save the JSON files: ")

    # Expand user paths if the user provides them
    pcap_directory = os.path.expanduser(pcap_directory)
    output_directory = os.path.expanduser(output_directory)

    convert_pcaps_to_json(pcap_directory, output_directory)