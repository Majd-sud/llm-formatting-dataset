import os
import subprocess

# Paths
black_folder = os.path.join(os.getcwd(), "black")
output_file = os.path.join(os.getcwd(), "black_evaluation.txt")

with open(output_file, "w", encoding="utf-8") as out:
    out.write("===== Black File Evaluation Report =====\n\n")

    # --- FLAKE8 Evaluation ---
    out.write("FLAKE8 Style Violations\n\n")
    for filename in os.listdir(black_folder):
        if filename.endswith(".py"):
            file_path = os.path.join(black_folder, filename)
            out.write(f"File: {filename}\n")

            result = subprocess.run(
                ["python", "-m", "flake8", "--filename", filename, file_path],
                capture_output=True,
                text=True
            )

            # Replace full path with just filename in output
            output = result.stdout.replace(file_path, filename).strip() or "No violations found."
            out.write(output + "\n\n")

    # --- RADON Complexity Evaluation ---
    out.write("\nRadon Cyclomatic Complexity\n\n")

    result = subprocess.run(
        ["python", "-m", "radon", "cc", black_folder, "-a"],
        capture_output=True,
        text=True
    )

    radon_output = result.stdout
    # Remove full paths from radon output
    for filename in os.listdir(black_folder):
        if filename.endswith(".py"):
            full_path = os.path.join(black_folder, filename)
            radon_output = radon_output.replace(full_path, filename)

    out.write(radon_output)

print("✅ Flake8 and Radon evaluation complete. Check 'black_evaluation.txt'")
