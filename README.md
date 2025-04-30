# BrightSec API Security Automation Template

![BrightSec Logo](https://brightsec.com/wp-content/uploads/2021/03/bright-logo-dark.svg)

A template repository for automating API security testing with BrightSec, featuring:
- Schema upload automation
- Discovery scan triggering
- Security scan execution

> **Example Implementation**: The `brokencrystals.swagger.json` file demonstrates a real-world API schema that can be scanned for vulnerabilities.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- BrightSec API credentials
- Azure DevOps (for CI/CD pipeline)

### Installation
```bash
pip install -r requirements.txt
```
### Repository Structure
.
├── azure-pipelines.yml       # Azure DevOps pipeline configuration
├── brokencrystals.swagger.json  # Example API schema (OpenAPI 3.0)
├── uploadAPI.py              # Schema upload + discovery script
├── run_ep_scan.py            # Entry point scanning script
├── requirements.txt          # Python dependencies
└── README.md                 # This file


### Configuration Environment Variables 
#### Variable Description Example
- BRIGHT_API_TOKEN BrightSec API key  28n2yhr.nexa... 
- BRIGHT_PROJECT_IDBrightSec project ID uLy59Y1DfVSZj... 
- BRIGHT_HOSTNAME BrightSec API host example:eu.brightsec.com Pipeline Variables

#### Set these in Azure DevOps: yaml
```bash
variables: BRIGHTSEC_API_KEY: \$(BRIGHTSEC_API_KEY) \# Secret variable
BRIGHTSEC_PROJECT_ID: $(BRIGHTSEC_PROJECT_ID)  
SCAN_NAME: 'Automated-Scan-$(Build.BuildId)'
```
### Manual execution

#### Upload schema + start discovery

python uploadAPI.py

####  Run security scan

python run_ep_scan.py\
--api_key \$BRIGHT_API_TOKEN\
--scan_name "Manual-Scan-1"\
--project_name "BrokenCrystals"\
--project_id \$BRIGHT_PROJECT_ID

###  CI/CD Pipeline (Azure DevOps)

Triggered automatically when:

    API schema files change (*.json/*.yaml)

    On manual pipeline runs

### 🛡️ Security Tests Included

The template scans for: yaml

-   OWASP Top 10 vulnerabilities
-   API-specific risks (SSRF, BOLA, etc.)
-   50+ preconfigured test cases


