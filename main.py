import os
import subprocess
import sys

def run_script(script_name):
    script_path = os.path.join("scripts", script_name)
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found.")
        return False
    
    print(f"\n{'='*50}")
    print(f"Running: {script_name}")
    print(f"{'='*50}\n")
    
    try:
        # Run the script using the current python interpreter
        result = subprocess.run([sys.executable, script_path], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\nError occurred while running {script_name}: {e}")
        return False

def main():
    # Sequence of steps for the pipeline
    steps = [
        "step1_extract_pdf.py",
        "consolidate_ai_data.py",
        "step2_query_enhanced_dict.py",
        "step2_build_phonetics.py",
        "step3_merge_all.py",
        "step4_export_missing_sentences.py",
        "step5_cleanup_intermediate.py",
        "step6_quality_check.py"
    ]
    
    for step in steps:
        success = run_script(step)
        if not success:
            print(f"\nPipeline stopped at step: {step}")
            sys.exit(1)
            
    print(f"\n{'='*50}")
    print("Project Execution Complete!")
    print("Final JSON files are located in the 'output/' directory.")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
