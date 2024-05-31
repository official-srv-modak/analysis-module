import subprocess

ollama_command = "ollama run llama3"  # Replace with the actual command to run Ollama
process = subprocess.Popen(ollama_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
input_data = "Hello, Ollama!\n"  # Replace with your desired input
process.stdin.write(input_data)
process.stdin.flush()  # Flush the input buffer
output_data = process.stdout.read()
print("Ollama's output:")
print(output_data)
process.stdin.close()
process.stdout.close()
process.stderr.close()
process.wait()  # Wait for the subprocess to finish
