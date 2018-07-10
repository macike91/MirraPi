#!/bin/bash

curl -v -X POST "https://api.projectoxford.ai/emotion/v1.0/recognize" -H "Content-Type: application/octet-stream" -H "Ocp-Apim-Subscription-Key: 9808623678d14ae58e5bb82975c4c14b" --data-binary unused/female.jpg
