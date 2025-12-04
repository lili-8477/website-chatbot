#!/usr/bin/env python3
"""
Deployment script for ai-builders.space platform
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def deploy_service():
    """Deploy the service to ai-builders.space"""
    
    # Get API key from environment
    api_key = os.getenv('AI_BUILDER_TOKEN') or os.getenv('AI_BUILDER_TOKEN') or os.getenv('SPACE_API_KEY')
    
    if not api_key:
        print("❌ Error: API key not found in environment variables.")
        print("Please set one of: AI_BUILDER_TOKEN, AI_BUILDER_API_KEY, or SPACE_API_KEY")
        return False
    
    # Read environment variables to pass to deployment
    env_vars = {}
    
    
    # Optional: Other environment variables
    optional_vars = ['DEFAULT_WEBSITE_URL', 'OPENAI_MODEL', 'HOST', 'MAX_RETRIES', 'REQUEST_TIMEOUT']
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            env_vars[var] = value
    
    # Deployment configuration
    deployment_config = {
        "repo_url": "https://github.com/lili-8477/website-chatbot",
        "service_name": "website-chatbot",
        "branch": "main",
        "port": 8000
    }
    
    # Add environment variables if any are found
    if env_vars:
        deployment_config["env_vars"] = env_vars
    
    # API endpoint
    base_url = "https://space.ai-builders.com/backend"
    endpoint = f"{base_url}/v1/deployments"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🚀 Starting deployment to ai-builders.space...")
    print(f"📦 Repository: {deployment_config['repo_url']}")
    print(f"🏷️  Service Name: {deployment_config['service_name']}")
    print(f"🌿 Branch: {deployment_config['branch']}")
    print(f"🔌 Port: {deployment_config['port']}")
    if env_vars:
        print(f"🔐 Environment Variables: {len(env_vars)} variable(s) will be injected")
        for key in env_vars.keys():
            # Don't print the actual key value for security
            print(f"   - {key}: {'*' * 20}")
    print()
    
    try:
        # Make the deployment request
        response = requests.post(
            endpoint,
            headers=headers,
            json=deployment_config,
            timeout=30
        )
        
        # Check response
        if response.status_code == 202:
            print("✅ Deployment queued successfully!")
            print()
            
            result = response.json()
            print("📋 Deployment Details:")
            print(f"   Service Name: {result.get('service_name', 'N/A')}")
            print(f"   Status: {result.get('status', 'N/A')}")
            print(f"   Message: {result.get('message', 'N/A')}")
            
            if result.get('public_url'):
                print(f"   🌐 Public URL: {result.get('public_url')}")
            else:
                print(f"   🌐 Public URL: https://{deployment_config['service_name']}.ai-builders.space")
            
            print()
            print("⏳ Next Steps:")
            print("   1. Wait 5-10 minutes for provisioning")
            print("   2. Check deployment status with:")
            print(f"      GET {base_url}/v1/deployments/{deployment_config['service_name']}")
            print("   3. Monitor the deployment until status changes from 'deploying' to 'HEALTHY'")
            print()
            print("💡 Tip: The deployment is asynchronous. Poll the status endpoint to check progress.")
            
            return True
            
        elif response.status_code == 422:
            print("❌ Validation Error:")
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
            return False
            
        else:
            print(f"❌ Deployment failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making deployment request: {e}")
        return False

if __name__ == "__main__":
    success = deploy_service()
    sys.exit(0 if success else 1)

