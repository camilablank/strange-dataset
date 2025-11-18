import json

# Load Llama Instruct results
with open('evaluation_results/Llama-3.1-8B-Instruct_validation_outputs.jsonl') as f:
    first_result = json.loads(f.readline())

# Check what fields exist
print("Fields in results:")
for key in first_result.keys():
    print(f"  - {key}")

# Specifically check CoT
if 'generated_text_true_statement_cot' in first_result:
    print("\n✓ CoT data EXISTS!")
    print("Sample:", first_result['generated_text_true_statement_cot'][:100])
else:
    print("\n✗ CoT data MISSING - needs to be re-run")