# run_specific_examples_safe.py
import json
import subprocess
import shutil
import os

def run_and_merge_examples(example_ids):
    """
    Run evaluate.py on specific examples and merge with existing results
    """
    print(f"Running evaluation on examples: {example_ids}")
    
    output_file = 'gpt-5_validation_outputs.jsonl'
    
    # Step 1: Load existing results
    existing_results = {}
    if os.path.exists(output_file):
        print(f"\nLoading existing results from {output_file}")
        with open(output_file, 'r') as f:
            for line in f:
                result = json.loads(line)
                existing_results[result['id']] = result
        print(f"✓ Found {len(existing_results)} existing results")
        
        # Backup existing file
        shutil.copy(output_file, f'{output_file}.backup')
        print(f"✓ Backed up to {output_file}.backup")
    else:
        print(f"\nNo existing results found - will create new file")
    
    # Step 2: Load and filter dataset
    with open('i_am_a_strange_dataset.jsonl', 'r') as f:
        all_data = [json.loads(line) for line in f]
    
    selected_data = [d for d in all_data if d['id'] in example_ids]
    print(f"\n✓ Selected {len(selected_data)} examples from dataset")
    
    if len(selected_data) != len(example_ids):
        found_ids = [d['id'] for d in selected_data]
        missing = set(example_ids) - set(found_ids)
        print(f"⚠ Warning: Could not find IDs: {missing}")
    
    # Step 3: Backup and replace dataset
    if not os.path.exists('i_am_a_strange_dataset.jsonl.backup'):
        shutil.copy('i_am_a_strange_dataset.jsonl', 'i_am_a_strange_dataset.jsonl.backup')
    
    with open('i_am_a_strange_dataset.jsonl', 'w') as f:
        for d in selected_data:
            f.write(json.dumps(d) + '\n')
    print(f"✓ Created temporary dataset with {len(selected_data)} examples")
    
    # Step 4: Clear output file so evaluate.py starts fresh
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Step 5: Run evaluate.py
    print("\n" + "="*70)
    print("Running evaluate.py...")
    print("="*70 + "\n")
    
    result = subprocess.run([
        'python', 'evaluate.py',
        '--model', 'gpt-5',
        '--api_model'
    ])
    
    # Step 6: Restore original dataset
    print("\n" + "="*70)
    print("Cleaning up...")
    print("="*70)
    
    shutil.move('i_am_a_strange_dataset.jsonl.backup', 'i_am_a_strange_dataset.jsonl')
    print("✓ Original dataset restored")
    
    # Step 7: Load new results
    new_results = {}
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            for line in f:
                result = json.loads(line)
                new_results[result['id']] = result
        print(f"✓ Generated {len(new_results)} new results")
    else:
        print("✗ No new results generated")
        return False
    
    # Step 8: Merge existing + new results
    print("\n" + "="*70)
    print("Merging results...")
    print("="*70)
    
    merged_results = {**existing_results, **new_results}  # New overwrites existing
    
    print(f"Existing results: {len(existing_results)}")
    print(f"New results: {len(new_results)}")
    print(f"Total merged: {len(merged_results)}")
    
    # Step 9: Write merged results
    with open(output_file, 'w') as f:
        for id in sorted(merged_results.keys()):
            f.write(json.dumps(merged_results[id]) + '\n')
    
    print(f"\n✓ Merged results written to {output_file}")
    
    # Step 10: Show summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total results: {len(merged_results)}")
    print(f"Newly added IDs: {list(new_results.keys())}")
    print(f"Backup saved at: {output_file}.backup")
    
    return True

if __name__ == "__main__":
    # Specify which examples to run
    example_ids = [197, 198, 199]
    
    success = run_and_merge_examples(example_ids)
    
    if success:
        print("\n✓ Evaluation and merge completed successfully!")
        print("Your original results are preserved and new ones are added.")
    else:
        print("\n✗ Evaluation failed")
        print("Your original results are backed up at gpt-5_validation_outputs.jsonl.backup")