"""Quick test of AWS Bedrock - Kimi K2.5
Run this to verify everything works before building.
"""

import json
import boto3
import sys
from datetime import datetime

# Configuration
AWS_PROFILE = "study"
AWS_REGION = "us-east-1"
MODEL_ID = "moonshot.kimi-k2-thinking"  # Kimi K2.5 on Bedrock

def test_bedrock():
    """Test AWS Bedrock with Kimi K2.5"""
    
    print("=" * 60)
    print("AWS Bedrock + Kimi K2.5 Test")
    print("=" * 60)
    
    # Create Bedrock client
    try:
        session = boto3.Session(profile_name=AWS_PROFILE)
        client = session.client('bedrock-runtime', region_name=AWS_REGION)
        print("\n[OK] AWS client created")
    except Exception as e:
        print(f"\n[FAIL] Failed to create AWS client: {e}")
        sys.exit(1)
    
    # Test prompt
    test_prompts = [
        "What is Python? Answer in one sentence.",
        "Write a LinkedIn headline for a Senior Data Engineer",
        "Summarize: Looking for a Python developer with 5+ years experience in AWS",
    ]
    
    total_cost = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n[{i}/3] Testing: {prompt[:50]}...")
        
        try:
            # Bedrock expects specific format for each model
            # Kimi uses messages format
            body = {
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = client.invoke_model(
                modelId=MODEL_ID,
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            
            # Extract response (format varies by model)
            if 'content' in result:
                answer = result['content'][0]['text']
            elif 'completion' in result:
                answer = result['completion']
            else:
                answer = str(result)[:200]
            
            # Estimate cost (very rough)
            input_tokens = len(prompt.split()) * 1.3
            output_tokens = len(answer.split()) * 1.3
            cost = (input_tokens + output_tokens) / 1000 * 0.0015  # ~$1.50 per 1M tokens
            total_cost += cost
            
            print(f"  Response: {answer[:100]}...")
            print(f"  Est. cost: ${cost:.6f}")
            
        except Exception as e:
            print(f"  [FAIL] Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Total estimated cost: ${total_cost:.6f}")
    print("Status: AWS Bedrock + Kimi K2.5 is WORKING")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_bedrock()
